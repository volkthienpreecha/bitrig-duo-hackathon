import SwiftUI
import SceneKit

struct GameSurface: View {
    let session: GameSession
    var body: some View {
        SceneView(scene: session.world.scene, options: [.autoenablesDefaultLighting])
            .onAppear { var frame = DeviceFrame(); frame.size = CGSize(width: 800,height: 1200); frame.usableRect = CGRect(origin: .zero,size: frame.size); session.updateDevice(frame) }
    }
}
