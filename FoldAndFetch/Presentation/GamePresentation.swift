import SceneKit
import Foundation

@MainActor final class GamePresentation {
    private let visual = SCNNode()
    init() {}
    func makeCharacterNode() -> SCNNode {
        if let url = Bundle.main.url(forResource: "kaprao-sprite", withExtension: "scn"), let scene = try? SCNScene(url: url), let child = scene.rootNode.childNode(withName: "KapraoSpriteRoot", recursively: true) { child.removeFromParentNode(); visual.addChildNode(child) }
        else { let sphere = SCNNode(geometry: SCNSphere(radius: 0.35)); sphere.position.y = 0.35; sphere.geometry?.firstMaterial?.diffuse.contents = UIColor.orange; visual.addChildNode(sphere) }
        return visual
    }
    func update(snapshot: GameSnapshot, events: [GameEvent], deltaTime: TimeInterval) {}
    func setMuted(_ muted: Bool) {}
}
