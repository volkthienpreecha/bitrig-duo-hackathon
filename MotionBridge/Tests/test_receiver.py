"""Behavior tests: reject invalid/replayed data; freshness uses receiver time; authenticate real HTTP routes."""
import copy
import http.client
import importlib.util
import json
from pathlib import Path
import threading
import unittest
import uuid

spec = importlib.util.spec_from_file_location('receiver', Path(__file__).parents[1] / 'Receiver/receiver.py')
receiver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(receiver)

def sample(seq=1, timestamp=10.0, session='11111111-1111-4111-8111-111111111111'):
    return dict(version=1, sessionID=session, seq=seq, timestamp=timestamp,
                accelerometer=dict(x=0.1, y=-0.2, z=-1.0), gravity=dict(x=0.0, y=0.0, z=-1.0))

class StoreTests(unittest.TestCase):
    def setUp(self):
        self.now = 100.0
        self.store = receiver.SampleStore(clock=lambda: self.now)
    def test_empty_is_not_fresh(self):
        self.assertFalse(self.store.latest().get('available', True))
    def test_freshness_uses_receiver_clock_not_phone_clock(self):
        self.store.accept(sample(timestamp=999999))
        self.assertTrue(self.store.latest().get('fresh', False))
        self.now = 100.51
        self.assertFalse(self.store.latest().get('fresh', True))
        self.assertAlmostEqual(self.store.latest().get('ageSeconds', -1), 0.51)
    def test_repeated_sequence_and_reversed_time_rejected(self):
        self.store.accept(sample())
        for bad in [sample(), sample(seq=2, timestamp=9), sample(seq=0, timestamp=11)]:
            with self.subTest(bad=bad), self.assertRaises(receiver.ProtocolError): self.store.accept(bad)
    def test_reconnect_new_session_then_reject_old_session(self):
        self.store.accept(sample())
        newer = sample(timestamp=1, session='22222222-2222-4222-8222-222222222222')
        self.store.accept(newer)
        self.assertEqual(self.store.latest().get('sample'), newer)
        with self.assertRaises(receiver.ProtocolError): self.store.accept(sample(seq=2, timestamp=11))
    def test_malformed_and_unbounded_numbers_rejected(self):
        bads = [None, [], {}, dict(sample(), seq=True), dict(sample(), seq=-1), dict(sample(), seq=2**53),
                dict(sample(), version=2), dict(sample(), timestamp=10**500), dict(sample(), timestamp=float('nan')), dict(sample(), sessionID='bad'),
                dict(sample(), accelerometer=dict(x=33,y=0,z=0)), dict(sample(), gravity=dict(x=0,y=0,z=float('inf')))]
        for bad in bads:
            with self.subTest(bad=bad), self.assertRaises(receiver.ProtocolError): self.store.accept(bad)
    def test_session_history_is_bounded_without_reaccepting_retired_ids(self):
        first = sample()
        self.store.accept(first)
        for index in range(128):
            self.store.accept(sample(session=str(uuid.UUID(int=index + 100))))
        with self.assertRaises(receiver.ProtocolError):
            self.store.accept(sample(session=str(uuid.UUID(int=999))))
        with self.assertRaises(receiver.ProtocolError):
            self.store.accept(sample(seq=99,timestamp=99))
    def test_gravity_not_ready_and_input_copy(self):
        payload = dict(sample(), gravity=None)
        self.store.accept(payload)
        payload['accelerometer']['x'] = 99
        self.assertEqual(self.store.latest().get('sample', {}).get('accelerometer', {}).get('x'), 0.1)

class HTTPTests(unittest.TestCase):
    def setUp(self):
        self.now = 100.0
        self.server = receiver.create_server('127.0.0.1', 0, 'test-pairing-token', receiver.SampleStore(clock=lambda: self.now))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
    def tearDown(self):
        self.server.shutdown(); self.server.server_close(); self.thread.join()
    def request(self, method, path, payload=None, token='test-pairing-token', raw=None):
        connection = http.client.HTTPConnection(*self.server.server_address, timeout=2)
        body = raw if raw is not None else (json.dumps(payload).encode() if payload is not None else None)
        headers = {'Content-Type':'application/json'}
        if token is not None: headers['Authorization'] = 'Bearer ' + token
        connection.request(method, path, body=body, headers=headers)
        response = connection.getresponse(); data = response.read(); status = response.status
        connection.close()
        try: result = json.loads(data)
        except ValueError: result = {}
        return status, result
    def test_auth_required_on_both_routes(self):
        for method,path in [('GET','/latest'),('POST','/sample')]:
            for token in [None,'wrong']:
                self.assertEqual(self.request(method,path,sample() if method=='POST' else None,token)[0],401)
    def test_post_get_stale_and_reconnect_over_http(self):
        self.assertEqual(self.request('GET','/latest')[0],200)
        self.assertEqual(self.request('POST','/sample',sample())[0],200)
        status, body = self.request('GET','/latest')
        self.assertEqual(status,200); self.assertTrue(body['fresh']); self.assertEqual(body['sample']['seq'],1)
        self.now += 1
        self.assertFalse(self.request('GET','/latest')[1]['fresh'])
        self.assertEqual(self.request('POST','/sample',sample(timestamp=1,session='22222222-2222-4222-8222-222222222222'))[0],200)
        self.assertEqual(self.request('POST','/sample',sample(seq=2,timestamp=11))[0],409)
    def test_bad_json_oversize_nan_and_duplicate_keys(self):
        for raw in [b'{', b'{"version":NaN}', b'{"version":1,"version":1}']:
            self.assertEqual(self.request('POST','/sample',raw=raw)[0],400)
        self.assertEqual(self.request('POST','/sample',raw=b' ' * 4097)[0],413)
    def test_unknown_route_is_not_latest(self):
        self.assertEqual(self.request('GET','/other')[0],404)

if __name__ == '__main__': unittest.main(verbosity=2)
