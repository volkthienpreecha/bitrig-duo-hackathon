import Foundation

@main enum MotionTypeChecks {
    static func main() throws {
        let json = """
        {"version":1,"sessionID":"11111111-1111-4111-8111-111111111111","seq":1,"timestamp":123.456,"accelerometer":{"x":0.1,"y":-0.2,"z":-1},"gravity":{"x":0,"y":0,"z":-1}}
        """
        let decoder = JSONDecoder()
        let sample = try decoder.decode(MotionSample.self, from: Data(json.utf8))
        precondition(sample.isValid, "Valid sender sample must be accepted")
        precondition(sample.gravity?.z == -1)
        precondition(sample.isFresh(at: 123.5), "Recent native callback should be live")
        precondition(!sample.isFresh(at: 124.0), "Delayed native callback must stay stale")
        precondition(!sample.isFresh(at: 123.0), "Future timestamp must be rejected")
        let noGravity = MotionSample(version: 1, sessionID: sample.sessionID, seq: 2, timestamp: 124,
            accelerometer: sample.accelerometer, gravity: nil)
        let encoded = try JSONSerialization.jsonObject(with: JSONEncoder().encode(noGravity)) as! [String: Any]
        precondition(encoded["gravity"] is NSNull, "Protocol requires explicit gravity:null before gravity is ready")
        let valid = MotionEnvelope(version: 1, available: true, fresh: true, ageSeconds: 0.1, sample: sample)
        precondition(valid.isUsable, "Fresh receiver response must be usable")
        for envelope in [
            MotionEnvelope(version: 1, available: true, fresh: false, ageSeconds: 0.6, sample: sample),
            MotionEnvelope(version: 1, available: true, fresh: true, ageSeconds: 0.6, sample: sample),
            MotionEnvelope(version: 1, available: false, fresh: true, ageSeconds: 0.1, sample: sample),
            MotionEnvelope(version: 1, available: true, fresh: true, ageSeconds: nil, sample: sample),
            MotionEnvelope(version: 2, available: true, fresh: true, ageSeconds: 0.1, sample: sample)] {
            precondition(!envelope.isUsable, "Invalid/stale envelope must pause input")
        }
        for vector in [MotionVector(x: .nan, y: 0, z: 0), MotionVector(x: 33, y: 0, z: 0), MotionVector(x: 0, y: .infinity, z: 0)] {
            precondition(!vector.isValid(limit: 32))
        }
        let malformed = json.replacingOccurrences(of: "123.456", with: "-1")
        let badSample = try decoder.decode(MotionSample.self, from: Data(malformed.utf8))
        precondition(!badSample.isValid)
        print("PASS: Swift protocol decoding, finite bounds and freshness checks")
    }
}
