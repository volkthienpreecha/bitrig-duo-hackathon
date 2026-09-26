#if os(macOS)
import SceneKit
import SwiftUI
import Metal

@main struct TiltStreetPhysicsCheck {
    @MainActor static func main() {
        _ = NSApplication.shared
        let world = TiltStreetWorld()
        let renderer = SCNRenderer(device: MTLCreateSystemDefaultDevice(),options: nil)
        renderer.scene = world.scene; renderer.pointOfView = world.camera; renderer.isPlaying = true
        var time = 0.0
        func step(_ count: Int) {
            for _ in 0..<count {
                time += 1.0/120
                world.beforePhysics(at: time)
                // A real render initializes and advances native SceneKit/Bullet. update(atTime:) alone is insufficient here.
                _ = renderer.snapshot(atTime: time,with: CGSize(width: 64,height: 64),antialiasingMode: .none)
                world.afterPhysics()
            }
        }
        func require(_ value: @autoclosure () -> Bool,_ message: String) { if !value() { fatalError(message) } }
        step(10)
        let root = ObjectIdentifier(world.playerVisualRoot),player = ObjectIdentifier(world.player),children = world.playerVisualRoot.childNodes.count
        world.drop(offset: .zero)
        let firstBody = world.cover.physicsBody
        world.drop(offset: CGPoint(x: 80,y: 0))
        require(world.cover.physicsBody === firstBody,"Drop must be one-shot")
        step(240)
        print("CENTER",world.phase.rawValue,"position",world.cover.presentation.position,"contacts",world.lastSupportCount,"dwell",world.supportDwell)
        require(world.phase == .safe,"Centered physical drop must seat")
        require(world.lastSupportCount >= 3 && world.supportDwell >= 0.40,"Safety needs real surrounding contacts and dwell")
        for _ in 0..<20 { world.moveRight(); step(38); if world.phase == .won { break } }
        print("CROSS",world.phase.rawValue,"player",world.player.presentation.position)
        require(world.phase == .won,"Manual bursts must cross actual cover and reach toy")
        world.reset(); step(5)
        require(ObjectIdentifier(world.playerVisualRoot) == root && ObjectIdentifier(world.player) == player && world.playerVisualRoot.childNodes.count == children,"Reset preserves player and attached visuals")
        require(world.phase == .waiting,"Reset clears phase")
        require(world.scene.rootNode.childNodes(passingTest: { node,_ in node.name == "cover" }).count == 1,"Exactly one cover after reset")
        for offset in [CGPoint(x: 1,y: 1),CGPoint(x: -1,y: -1),CGPoint(x: 1,y: -1),CGPoint(x: -1,y: 1)] {
            world.reset(); step(5); world.drop(offset: offset); step(360)
            print("TARGET CORNER",offset,"phase",world.phase.rawValue,"pose",world.cover.presentation.position)
            require(world.phase == .safe,"Every lawful target corner must physically seat")
        }
        world.reset(); step(5); world.drop(offset: CGPoint(x: 60,y: 0)); step(630)
        print("MISS",world.phase.rawValue,"coverage",world.coverage,"cover",world.cover.presentation.position)
        require(world.phase == .failed && world.coverage < 0.99,"Large actual offset must fail")
        require(!TiltStreetWorld.supportsSurround(center: .zero,contacts: [CGPoint(x: 1,y: 0),CGPoint(x: 1,y: 0.3),CGPoint(x: 1,y: -0.3)]),"Three neighboring contacts cannot declare safety")
        require(TiltStreetWorld.maximumJumpReach < 2*1.15*cos(.pi/16),"Jump bound including body extent cannot span unsupported chord")
        world.reset(); step(5)
        world.player.position = SCNVector3(0,0.5,0); world.player.physicsBody?.resetTransform(); step(150)
        require(world.player.presentation.position.x < -3 && world.phase == .waiting,"Uncovered opening must physically drop the dog into checkpoint recovery")
        world.moveRight(); world.jump(); step(12)
        let beforePause = world.player.presentation.position
        world.scene.isPaused = true; step(120)
        let afterPause = world.player.presentation.position
        require(abs(beforePause.x-afterPause.x)<0.001 && abs(beforePause.y-afterPause.y)<0.001,"Coordinator pause freezes physics")
        world.scene.isPaused = false
        print("PASS: center seating, one-shot release, physical crossing, reset identity/count, four target corners, genuine miss, unsafe support rejection, jump gap, real open-hole fall/recovery, coordinator pause")
    }
}
#endif
