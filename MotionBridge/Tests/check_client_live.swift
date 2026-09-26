import Foundation

@main enum LiveClientChecks {
    @MainActor static func main() async throws {
        let client = MotionInputClient()
        client.start(token: "wrong")
        try await Task.sleep(nanoseconds: 400_000_000)
        precondition(!client.isFresh && client.status.contains("token"), "401 must invalidate input")
        client.stop()
        client.start(token: "live-client-test-token")
        try await Task.sleep(nanoseconds: 150_000_000)
        precondition(!client.isFresh, "Empty receiver cannot drive the simulator")
        let first = UUID().uuidString.lowercased()
        try await post(session: first, sequence: 1)
        try await Task.sleep(nanoseconds: 160_000_000)
        precondition(client.isFresh && client.sample?.gravity?.y == 0.25, "Client must read actual HTTP gravity")
        // POST at ~150ms after start places its 500ms deadline between watchdog ticks.
        try await Task.sleep(nanoseconds: 355_000_000)
        precondition(!client.isFresh, "Board input must expire between watchdog ticks")
        try await Task.sleep(nanoseconds: 150_000_000)
        precondition(!client.isFresh && client.sample == nil, "Stale stream must clear usable input")
        let second = UUID().uuidString.lowercased()
        try await post(session: second, sequence: 1)
        try await Task.sleep(nanoseconds: 160_000_000)
        precondition(client.isFresh && client.sample?.sessionID == second, "New session must reconnect")
        client.stop()
        precondition(!client.isFresh && client.sample == nil && client.status == "Stopped")
        print("PASS: actual Swift client HTTP auth, empty input, live gravity, stale pause, reconnect and stop")
    }
    static func post(session: String, sequence: UInt64) async throws {
        let sample = MotionSample(version: 1, sessionID: session, seq: sequence, timestamp: 10,
            accelerometer: MotionVector(x: 0.1,y: 0.2,z: -1), gravity: MotionVector(x: 0,y: 0.25,z: -0.9))
        var request = URLRequest(url: URL(string: "http://127.0.0.1:8765/sample")!)
        request.httpMethod = "POST"; request.httpBody = try JSONEncoder().encode(sample)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer live-client-test-token", forHTTPHeaderField: "Authorization")
        let (_, response) = try await URLSession.shared.data(for: request)
        precondition((response as? HTTPURLResponse)?.statusCode == 200)
    }
}
