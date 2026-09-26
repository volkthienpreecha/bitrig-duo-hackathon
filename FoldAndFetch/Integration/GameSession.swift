import Foundation
import Observation
import SceneKit
import Metal

@MainActor @Observable final class GameSession {
    let world: GameWorld
    let renderer: SCNRenderer
    let presentation: GamePresentation
    var snapshot = GameSnapshot()
    var device = DeviceFrame()
    var muted = false
    var requiresResume = false
    var simulationTime: TimeInterval = 1
    var frameCount: UInt64 = 0
    var simulationSteps: UInt64 = 0
    private var lastTimestamp: TimeInterval?
    private var pending: [GameCommand] = []
    private var sequence: UInt64 = 0
    private var accumulator: TimeInterval = 0
    init() {
        world = GameWorld()
        renderer = SCNRenderer(device: MTLCreateSystemDefaultDevice(), options: nil)
        renderer.scene = world.scene
        renderer.isPlaying = true
        presentation = GamePresentation()
        world.playerVisualRoot.addChildNode(presentation.makeCharacterNode())
        snapshot = world.snapshot
    }
    func updateDevice(_ frame: DeviceFrame) {
        if device.layoutVersion != frame.layoutVersion { pending.removeAll() }
        let interrupted = (device.isActive && !frame.isActive)
            || (device.hasValidLayout && !frame.hasValidLayout)
        if interrupted {
            requiresResume = true
            pending.removeAll()
            lastTimestamp = nil
            accumulator = 0
        }
        device = frame
    }
    func send(_ action: GameAction) {
        if case .resume = action { requiresResume = false; lastTimestamp = nil; accumulator = 0; return }
        sequence += 1
        pending.append(GameCommand(sequence: sequence, generation: snapshot.generation, timestamp: ProcessInfo.processInfo.systemUptime, layoutVersion: device.layoutVersion, action: action))
    }
    func toggleMute() { muted.toggle(); presentation.setMuted(muted) }
    // Called once by A's single main-thread display driver, never by individual render passes.
    func advanceFrame(at timestamp: TimeInterval) {
        frameCount += 1
        let dt = min(max(timestamp - (lastTimestamp ?? timestamp),0), 0.05)
        lastTimestamp = timestamp
        let paused = requiresResume || !device.isActive || !device.hasValidLayout
        if paused { accumulator = 0; pending.removeAll() }
        else {
            let commands = pending; pending.removeAll()
            for command in commands where command.generation == snapshot.generation && command.layoutVersion == device.layoutVersion { world.handle(command, device: device) }
            accumulator += dt
            let fixed: TimeInterval = 1.0 / 120.0
            var steps = 0
            while accumulator >= fixed && steps < 6 {
                simulationTime += fixed
                world.preStep(deltaTime: fixed, simulationTime: simulationTime, device: device)
                renderer.update(atTime: simulationTime)
                world.postStep(deltaTime: fixed, simulationTime: simulationTime, device: device)
                accumulator -= fixed; steps += 1; simulationSteps += 1
            }
        }
        snapshot = world.snapshot
        snapshot.isPaused = paused
        snapshot.pauseReason = requiresResume ? "Ready when you are" : (!device.hasValidLayout ? "Hold Duo vertically" : (!device.isActive ? "Paused" : nil))
        presentation.update(snapshot: snapshot, events: world.drainEvents(), deltaTime: paused ? 0 : dt)
    }
}
