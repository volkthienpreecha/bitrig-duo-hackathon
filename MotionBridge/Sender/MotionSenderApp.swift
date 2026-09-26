import SwiftUI
import Combine

@main struct MotionSenderApp: App {
    var body: some Scene { WindowGroup { SenderView() } }
}

@MainActor final class SenderModel: ObservableObject {
    @Published var host = ""
    @Published var token = ""
    @Published private(set) var status = "Enter your Mac’s Wi-Fi IPv4 and pairing token."
    @Published private(set) var sample: MotionSample?
    @Published private(set) var running = false
    @Published private(set) var sent: UInt64 = 0
    private let input = MotionInputClient()
    private var subscription: AnyCancellable?
    private var statusSubscription: AnyCancellable?
    private var task: Task<Void, Never>?
    private var network: URLSession?
    private var endpoint: URL?
    private var runToken = ""
    private var generation: UInt64 = 0
    private var nextAttempt: TimeInterval = 0

    init() {
        statusSubscription = input.$status.sink { [weak self] status in
            guard let self, self.running, !self.input.isFresh else { return }
            if status.contains("unavailable") || status.contains("stale") { self.status = status }
        }
        subscription = input.$sample.sink { [weak self] sample in
            guard let self else { return }
            self.sample = sample
            if let sample { self.send(sample) }
        }
    }
    func start() {
        stop()
        #if targetEnvironment(simulator)
        status = "Install this sender on a physical iPhone to capture motion."
        #else
        guard let endpoint = MotionInputClient.endpoint(host: host, path: "/sample"), !token.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else {
            status = "Enter a valid Mac IPv4 and the pairing token."; return
        }
        self.endpoint = endpoint; runToken = token.trimmingCharacters(in: .whitespacesAndNewlines)
        let configuration = URLSessionConfiguration.ephemeral
        configuration.timeoutIntervalForRequest = 0.4; configuration.timeoutIntervalForResource = 0.6
        network = URLSession(configuration: configuration)
        sent = 0; nextAttempt = 0; running = true
        status = "Capturing 30 Hz; connecting to Mac…"
        input.start()
        #endif
    }
    func stop() {
        generation &+= 1; running = false
        task?.cancel(); task = nil
        input.stop(); network?.invalidateAndCancel(); network = nil
        sample = nil; status = "Stopped"
    }
    private func send(_ sample: MotionSample) {
        guard running, task == nil, ProcessInfo.processInfo.systemUptime >= nextAttempt,
              let endpoint, let network else { return }
        let run = generation
        var request = URLRequest(url: endpoint)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer " + runToken, forHTTPHeaderField: "Authorization")
        request.httpBody = try? JSONEncoder().encode(sample)
        // At most one request exists. Intermediate readings are dropped, never queued.
        task = Task { @MainActor [weak self] in
            guard let self else { return }
            defer { if self.generation == run { self.task = nil } }
            do {
                let (_, response) = try await network.data(for: request)
                guard !Task.isCancelled, self.generation == run else { return }
                let code = (response as? HTTPURLResponse)?.statusCode ?? 0
                if code == 200 { self.sent &+= 1; self.status = "Sending live motion to Mac" }
                else {
                    self.status = code == 401 ? "Pairing token rejected — check the Mac token" : "Receiver rejected sample (HTTP \(code))"
                    self.nextAttempt = ProcessInfo.processInfo.systemUptime + 1
                }
            } catch {
                guard !Task.isCancelled, self.generation == run else { return }
                self.status = "Mac unreachable — check Wi-Fi, address and Local Network permission"
                self.nextAttempt = ProcessInfo.processInfo.systemUptime + 0.5
            }
        }
    }
}

private struct SenderView: View {
    @StateObject private var model = SenderModel()
    @Environment(\.scenePhase) private var scenePhase
    var body: some View {
        NavigationStack {
            Form {
                Section("Mac receiver") {
                    TextField("Mac Wi-Fi IPv4, e.g. 192.168.1.12", text: $model.host).keyboardType(.decimalPad).textInputAutocapitalization(.never).autocorrectionDisabled()
                    SecureField("Pairing token", text: $model.token).textInputAutocapitalization(.never).autocorrectionDisabled()
                    Button(model.running ? "Stop sending" : "Start sending") { model.running ? model.stop() : model.start() }
                        .frame(minHeight: 44)
                }.disabled(false)
                Section("Connection") {
                    Text(model.status)
                    Text("Samples accepted: \(model.sent)").monospacedDigit()
                }
                Section("Live readings · g") {
                    if let sample = model.sample {
                        vector("Raw acceleration", sample.accelerometer)
                        if let gravity = sample.gravity { vector("Gravity for stable tilt", gravity) }
                        else { Text("Waiting for gravity…") }
                        Text("Sequence \(sample.seq) · t \(sample.timestamp, specifier: "%.3f") s").font(.caption).monospacedDigit()
                    } else { Text("No active motion input") }
                }
                Section {
                    Text("Keep this app open. Both devices must use the same Wi-Fi. Start receiver.py on the Mac first; enter the token printed there. Backgrounding stops capture and transmission.")
                }
            }.navigationTitle("Motion Sender")
        }
        .onChange(of: scenePhase) { phase in if phase == .background { model.stop() } }
    }
    private func vector(_ title: String, _ value: MotionVector) -> some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(title).font(.headline)
            Text("x \(value.x, specifier: "%.3f")   y \(value.y, specifier: "%.3f")   z \(value.z, specifier: "%.3f")").monospacedDigit().font(.system(.body, design: .monospaced))
        }
    }
}
