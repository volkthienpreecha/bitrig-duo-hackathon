#!/usr/bin/env python3
"""Authenticated, bounded local motion relay. Python 3 standard library only."""
import argparse
from collections import deque
import copy
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import math
import secrets
import time
import uuid

MAX_BODY = 4096
STALE_AFTER = 0.5

class ProtocolError(ValueError):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status

def finite_number(value, minimum, maximum):
    return type(value) in (int, float) and minimum <= value <= maximum and math.isfinite(value)

def validate_sample(value):
    keys = {'version','sessionID','seq','timestamp','accelerometer','gravity'}
    if not isinstance(value, dict) or set(value) != keys:
        raise ProtocolError('Expected exactly the v1 sample fields')
    if type(value['version']) is not int or value['version'] != 1:
        raise ProtocolError('Unsupported protocol version')
    session = value['sessionID']
    try:
        if not isinstance(session, str) or str(uuid.UUID(session)) != session.lower(): raise ValueError()
    except (ValueError, AttributeError): raise ProtocolError('sessionID must be a UUID')
    if type(value['seq']) is not int or not 0 <= value['seq'] <= 2**53 - 1:
        raise ProtocolError('seq must be a nonnegative safe integer')
    if not finite_number(value['timestamp'], 0, 1e12): raise ProtocolError('Invalid monotonic timestamp')
    for name,limit in [('accelerometer',32),('gravity',1.5)]:
        vector = value[name]
        if name == 'gravity' and vector is None: continue
        if not isinstance(vector,dict) or set(vector) != {'x','y','z'}:
            raise ProtocolError(name + ' must have x/y/z')
        if any(not finite_number(vector[axis],-limit,limit) for axis in ('x','y','z')):
            raise ProtocolError(name + ' must contain bounded finite g values')
    return copy.deepcopy(value)

class SampleStore:
    def __init__(self, clock=None, stale_after=STALE_AFTER):
        self.clock = clock or time.monotonic
        self.stale_after = stale_after
        self.sample = None
        self.received = None
        self.retired = deque(maxlen=128)
    def accept(self, sample):
        value = validate_sample(sample)
        session = value['sessionID'].lower()
        value['sessionID'] = session
        if session in self.retired: raise ProtocolError('Retired sender session',409)
        if self.sample is not None:
            if session == self.sample['sessionID']:
                if value['seq'] <= self.sample['seq'] or value['timestamp'] <= self.sample['timestamp']:
                    raise ProtocolError('Sequence and timestamp must increase',409)
            else:
                if len(self.retired) >= 128:
                    raise ProtocolError('Sender session limit reached; restart the relay',409)
                self.retired.append(self.sample['sessionID'])
        self.sample = value
        self.received = self.clock()
    def latest(self):
        age = None if self.received is None else max(0,self.clock() - self.received)
        return dict(version=1, available=self.sample is not None,
                    fresh=age is not None and age <= self.stale_after,
                    ageSeconds=age, sample=copy.deepcopy(self.sample))

def strict_object(pairs):
    result = {}
    for key,value in pairs:
        if key in result: raise ProtocolError('Duplicate JSON key')
        result[key] = value
    return result

def create_server(host, port, token, store=None):
    store = store if store is not None else SampleStore()
    class Handler(BaseHTTPRequestHandler):
        protocol_version = 'HTTP/1.0'
        def setup(self):
            super().setup()
            self.connection.settimeout(1.0)
        def log_message(self, format, *args): pass  # No payload or token logging.
        def reply(self,status,value):
            data = json.dumps(value,allow_nan=False,separators=(',',':')).encode()
            self.send_response(status)
            self.send_header('Content-Type','application/json')
            self.send_header('Content-Length',str(len(data)))
            self.send_header('Cache-Control','no-store')
            self.send_header('Connection','close')
            self.end_headers()
            self.wfile.write(data)
        def authorized(self):
            supplied = self.headers.get('Authorization','')
            if not secrets.compare_digest(supplied.encode(), ('Bearer ' + token).encode()):
                self.reply(401,dict(error='Pairing token required'))
                return False
            return True
        def do_GET(self):
            if not self.authorized(): return
            if self.path != '/latest': self.reply(404,dict(error='Unknown route')); return
            self.reply(200,store.latest())
        def do_POST(self):
            if not self.authorized(): return
            if self.path != '/sample': self.reply(404,dict(error='Unknown route')); return
            try:
                if self.headers.get('Transfer-Encoding'): raise ProtocolError('Chunked requests unsupported')
                lengths = self.headers.get_all('Content-Length',[])
                if len(lengths) != 1: raise ProtocolError('One Content-Length required')
                try: length = int(lengths[0])
                except ValueError: raise ProtocolError('Invalid Content-Length')
                if not 0 < length <= MAX_BODY: raise ProtocolError('Payload too large or empty',413)
                if self.headers.get_content_type() != 'application/json': raise ProtocolError('application/json required',415)
                raw = self.rfile.read(length)
                if len(raw) != length: raise ProtocolError('Incomplete body')
                value = json.loads(raw,object_pairs_hook=strict_object,
                    parse_constant=lambda constant: (_ for _ in ()).throw(ProtocolError('Nonfinite JSON number')))
                store.accept(value)
                self.reply(200,dict(accepted=True,sessionID=value['sessionID'],seq=value['seq']))
            except ProtocolError as error: self.reply(error.status,dict(error=str(error)))
            except (ValueError,UnicodeError,RecursionError): self.reply(400,dict(error='Malformed JSON'))
            except TimeoutError: self.reply(408,dict(error='Body read timed out'))
    # Serial server bounds concurrent work/memory; short requests need no worker pool.
    server = HTTPServer((host,port),Handler)
    return server

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host',default='0.0.0.0')
    parser.add_argument('--port',type=int,default=8765)
    args = parser.parse_args()
    token = secrets.token_urlsafe(24)
    server = create_server(args.host,args.port,token)
    print('Motion Bridge listening on %s:%d' % server.server_address,flush=True)
    print('Pairing token: ' + token,flush=True)
    print('Enter this Mac’s Wi-Fi IPv4 and token in the iPhone sender. Simulator host: 127.0.0.1',flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()

if __name__ == '__main__': main()
