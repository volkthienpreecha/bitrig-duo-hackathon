import Foundation
import SceneKit

@MainActor final class GameWorld {
    let scene = SCNScene()
    let playerVisualRoot = SCNNode()
    private(set) var snapshot = GameSnapshot()
    init() {
        scene.background.contents = UIColor(red: 0.07, green: 0.12, blue: 0.14, alpha: 1)
        scene.rootNode.addChildNode(playerVisualRoot)
        playerVisualRoot.position = SCNVector3(-3.2,0,0)
        let light = SCNNode(); light.light = SCNLight(); light.light?.type = .ambient; light.light?.intensity = 700
        scene.rootNode.addChildNode(light)
        let road = SCNNode(geometry: SCNBox(width: 8,height: 0.2,length: 3,chamferRadius: 0.08))
        road.position.y = -0.1; road.geometry?.firstMaterial?.diffuse.contents = UIColor.darkGray
        scene.rootNode.addChildNode(road)
    }
    func handle(_ command: GameCommand, device: DeviceFrame) {}
    func preStep(deltaTime: TimeInterval, simulationTime: TimeInterval, device: DeviceFrame) {}
    func postStep(deltaTime: TimeInterval, simulationTime: TimeInterval, device: DeviceFrame) { snapshot.step += 1 }
    func drainEvents() -> [GameEvent] { [] }
}
