import AVFoundation
import Combine
import Foundation

/// Sound effects driven by accepted game events. No gameplay clock or scene ownership.
@MainActor final class CrossroadsAudio: ObservableObject {
    @Published private(set) var muted = false

    private static let soundNames = [
        "step_soft", "jump", "land_soft", "dash_down",
        "mechanism_release", "bridge_land", "success", "retry"
    ]
    private let cooldowns: [String: TimeInterval] = [
        "step_soft": 0.16,
        "jump": 0.10,
        "land_soft": 0.20,
        "dash_down": 0.12,
        "mechanism_release": 0.25,
        "bridge_land": 0.35,
        "success": 0.50,
        "retry": 0.10
    ]
    private var players: [String: AVAudioPlayer] = [:]
    private var lastPlayed: [String: TimeInterval] = [:]

    init(bundle: Bundle = .main) {
        for name in Self.soundNames {
            guard let url = bundle.url(forResource: name, withExtension: "wav"),
                  let player = try? AVAudioPlayer(contentsOf: url) else { continue }
            player.prepareToPlay()
            players[name] = player
        }
    }

    func play(_ name: String) {
        guard !muted, let player = players[name] else { return }
        let now = ProcessInfo.processInfo.systemUptime
        if let last = lastPlayed[name], now - last < (cooldowns[name] ?? 0) { return }
        lastPlayed[name] = now
        player.stop()
        player.currentTime = 0
        player.play()
    }

    func toggleMute() {
        muted.toggle()
        if muted { stopAll() }
    }

    func stopAll() {
        for player in players.values {
            player.stop()
            player.currentTime = 0
        }
        lastPlayed.removeAll()
    }
}
