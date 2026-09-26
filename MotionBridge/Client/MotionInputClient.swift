import Foundation
import Combine
#if os(iOS)
import CoreMotion
#endif

/// Main-actor motion input. Units are g, axes are the source device's fixed hardware axes.
/// Simulator/macOS polls the relay; physical iOS uses native Core Motion directly.
@MainActor final class MotionInputClient: ObservableObject {
    @Published private(set) var sample: MotionSample?
    @Published private(set) var status = "Stopped"
    @Published private var freshState = false
    /// Evaluated at the consumer's frame, so input expires even between watchdog ticks.
    var isFresh: Bool { freshState && ProcessInfo.processInfo.systemUptime <= usableUntil }
    private var pollTask: Task<Void, Never>?
    private var freshnessTimer: Timer?
    private var usableUntil: TimeInterval = 0
    private var generation: UInt64 = 0
    private var network: URLSession?
    #if os(iOS) && !targetEnvironment(simulator)
    private let motion = CMMotionManager()
    private var gravity: MotionVector?
    private var gravityTimestamp: TimeInterval = 0
    private var nativeSession = UUID().uuidString.lowercased()
    private var nativeSequence: UInt64 = 0
    #endif

    func start(host: String = "127.0.0.1", token: String = "") {
        stop()
        generation &+= 1
        let run = generation
        freshnessTimer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { [weak self] _ in
            Task { @MainActor [weak self] in self?.expireIfNeeded() }
        }
        #if targetEnvironment(simulator) || os(macOS)
        guard let url = Self.endpoint(host: host, path: "/latest"), !token.isEmpty else {
            status = "Enter the Mac IPv4 and pairing token"; return
        }
        status = "Connecting to motion relay…"
        let configuration = URLSessionConfiguration.ephemeral
        configuration.timeoutIntervalForRequest = 0.4
        configuration.timeoutIntervalForResource = 0.5
        configuration.requestCachePolicy = .reloadIgnoringLocalCacheData
        let network = URLSession(configuration: configuration)
        self.network = network
        pollTask = Task { @MainActor [weak self] in
            while !Task.isCancelled {
                guard let self, self.generation == run else { return }
                var request = URLRequest(url: url)
                request.setValue("Bearer " + token, forHTTPHeaderField: "Authorization")
                let requestStarted = ProcessInfo.processInfo.systemUptime
                do {
                    let (data,response) = try await network.data(for: request)
                    guard !Task.isCancelled, self.generation == run else { return }
                    guard let http = response as? HTTPURLResponse, http.statusCode == 200 else {
                        self.invalidate((response as? HTTPURLResponse)?.statusCode == 401 ? "Pairing token rejected" : "Relay request failed")
                        try await Task.sleep(nanoseconds: 250_000_000)
                        continue
                    }
                    guard data.count <= 8192 else { self.invalidate("Invalid relay response"); continue }
                    let envelope = try JSONDecoder().decode(MotionEnvelope.self, from: data)
                    let now = ProcessInfo.processInfo.systemUptime
                    let remaining = 0.5 - (envelope.ageSeconds ?? 0.5) - (now - requestStarted)
                    if envelope.isUsable, remaining > 0, let sample = envelope.sample {
                        self.sample = sample
                        self.usableUntil = now + remaining
                        self.freshState = true
                        self.status = sample.gravity == nil ? "Receiving acceleration; waiting for gravity" : "Live iPad motion via Wi-Fi"
                    } else { self.invalidate(envelope.available ? "Motion stale — paused" : "Waiting for iPad motion") }
                } catch {
                    guard !Task.isCancelled, self.generation == run else { return }
                    self.invalidate("Relay unavailable — paused")
                }
                try? await Task.sleep(nanoseconds: 33_333_333)
            }
        }
        #else
        guard motion.isAccelerometerAvailable else { status = "Accelerometer unavailable — paused"; return }
        nativeSession = UUID().uuidString.lowercased(); nativeSequence = 0
        gravity = nil; gravityTimestamp = 0
        motion.accelerometerUpdateInterval = 1.0 / 30.0
        motion.deviceMotionUpdateInterval = 1.0 / 30.0
        if motion.isDeviceMotionAvailable {
            motion.startDeviceMotionUpdates(to: .main) { [weak self] value, error in
                guard let self, self.generation == run, let value else { return }
                self.gravity = MotionVector(x: value.gravity.x, y: value.gravity.y, z: value.gravity.z)
                self.gravityTimestamp = value.timestamp
            }
        }
        status = "Starting native Core Motion…"
        motion.startAccelerometerUpdates(to: .main) { [weak self] value, error in
            guard let self, self.generation == run else { return }
            guard let value else { self.invalidate("Core Motion unavailable — paused"); return }
            self.nativeSequence &+= 1
            let gravity = abs(value.timestamp - self.gravityTimestamp) <= 0.2 ? self.gravity : nil
            let sample = MotionSample(version: 1, sessionID: self.nativeSession, seq: self.nativeSequence,
                timestamp: value.timestamp,
                accelerometer: MotionVector(x: value.acceleration.x, y: value.acceleration.y, z: value.acceleration.z), gravity: gravity)
            guard sample.isFresh(at: ProcessInfo.processInfo.systemUptime) else {
                self.invalidate("Invalid or stale native motion — paused"); return
            }
            self.sample = sample; self.freshState = true
            self.usableUntil = sample.timestamp + 0.5
            self.status = gravity == nil ? "Native acceleration; waiting for gravity" : "Live native Core Motion"
        }
        #endif
    }

    func stop() {
        generation &+= 1
        pollTask?.cancel(); pollTask = nil
        network?.invalidateAndCancel(); network = nil
        freshnessTimer?.invalidate(); freshnessTimer = nil
        #if os(iOS) && !targetEnvironment(simulator)
        motion.stopAccelerometerUpdates(); motion.stopDeviceMotionUpdates()
        #endif
        invalidate("Stopped")
    }
    private func expireIfNeeded() {
        if freshState && ProcessInfo.processInfo.systemUptime > usableUntil { invalidate("Motion stale — paused") }
    }
    private func invalidate(_ reason: String) {
        sample = nil; freshState = false; usableUntil = 0; status = reason
    }
    static func endpoint(host: String, path: String) -> URL? {
        let value = host.trimmingCharacters(in: .whitespacesAndNewlines)
        let components = value.split(separator: ".", omittingEmptySubsequences: false)
        let ipv4 = components.count == 4 && components.allSatisfy { !$0.isEmpty && $0.allSatisfy(\.isNumber) && (Int($0).map { (0...255).contains($0) } ?? false) }
        guard value == "localhost" || ipv4 else { return nil }
        var url = URLComponents()
        url.scheme = "http"; url.host = value; url.port = 8765; url.path = path
        return url.url
    }
}
