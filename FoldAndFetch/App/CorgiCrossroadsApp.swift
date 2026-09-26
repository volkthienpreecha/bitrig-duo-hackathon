import SwiftUI

@main struct CorgiCrossroadsApp: App {
    @State private var session = GameSession()
    var body: some Scene {
        WindowGroup {
            ZStack {
                GameSurface(session: session)
                GameHUD(snapshot: session.snapshot, device: session.device, onAction: session.send, onMute: session.toggleMute)
            }.preferredColorScheme(.dark)
        }
    }
}
