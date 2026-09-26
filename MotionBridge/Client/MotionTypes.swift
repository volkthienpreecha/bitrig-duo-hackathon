import Foundation
struct MotionVector: Codable, Equatable {
    let x: Double
    let y: Double
    let z: Double
    func isValid(limit: Double) -> Bool { [x, y, z].allSatisfy { $0.isFinite && abs($0) <= limit } }
}
struct MotionSample: Codable, Equatable {
    let version: Int
    let sessionID: String
    let seq: UInt64
    let timestamp: Double
    let accelerometer: MotionVector
    let gravity: MotionVector?
    /// Only for native readings sharing this device's monotonic clock.
    func isFresh(at uptime: TimeInterval) -> Bool {
        isValid && uptime.isFinite && (0...0.5).contains(uptime - timestamp)
    }
    enum CodingKeys: String, CodingKey { case version, sessionID, seq, timestamp, accelerometer, gravity }
    func encode(to encoder: Encoder) throws {
        var values = encoder.container(keyedBy: CodingKeys.self)
        try values.encode(version, forKey: .version)
        try values.encode(sessionID, forKey: .sessionID)
        try values.encode(seq, forKey: .seq)
        try values.encode(timestamp, forKey: .timestamp)
        try values.encode(accelerometer, forKey: .accelerometer)
        try values.encode(gravity, forKey: .gravity)
    }
    var isValid: Bool {
        version == 1 && UUID(uuidString: sessionID) != nil && seq <= 9_007_199_254_740_991 &&
        timestamp.isFinite && (0...1e12).contains(timestamp) && accelerometer.isValid(limit: 32) &&
        (gravity?.isValid(limit: 1.5) ?? true)
    }
}
struct MotionEnvelope: Codable {
    let version: Int
    let available: Bool
    let fresh: Bool
    let ageSeconds: Double?
    let sample: MotionSample?
    var isUsable: Bool {
        guard version == 1, available, fresh, let ageSeconds, ageSeconds.isFinite,
              (0...0.5).contains(ageSeconds), let sample else { return false }
        return sample.isValid
    }
}
