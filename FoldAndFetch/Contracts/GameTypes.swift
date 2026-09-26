import Foundation
import SwiftUI
import SceneKit
import simd

enum DisplayMode: String { case inner, outer, unsupported }
enum DragPhase { case began, changed, ended, cancelled }
enum GamePhase: String { case staging, locked, dropping, settling, safe, crossing, won, failed }

struct DeviceFrame {
    var timestamp: TimeInterval = 0
    var hingeRadians: Double? = nil
    var foldRadians: Double = 0
    var isClosed = false
    var mode: DisplayMode = .inner
    var isActive = true
    var isPortrait = true
    var size: CGSize = .zero
    var usableRect: CGRect = .zero
    var upperRect: CGRect = .zero
    var lowerRect: CGRect = .zero
    var layoutVersion: UInt64 = 0
    var source = "unavailable"
    var hasValidLayout: Bool { size.width > 1 && size.height > 1 && mode != .unsupported && isPortrait }
}

enum GameAction {
    // Normalized coordinates in the visible staging rail control, x right/y down.
    case railDrag(CGPoint, DragPhase)
    case lockPlacement, adjustPlacement, release
    case moveLeft, moveRight, jump, dash
    case retry, replay, next, resume
}
struct GameCommand {
    let sequence: UInt64
    let generation: UInt64
    let timestamp: TimeInterval
    let layoutVersion: UInt64
    let action: GameAction
}
struct PlacementLock {
    let generation: UInt64
    let worldTransform: simd_float4x4
    let railProgress: Float
    let aimAngle: Double
}
struct WorldFraming {
    var center = SCNVector3(0, 1.4, 0)
    var minimum = SCNVector3(-4.4, -1.0, -2.8)
    var maximum = SCNVector3(4.4, 4.8, 2.8)
    var target = SCNVector3(0, 0.0, 0)
}
struct GameSnapshot {
    var step: UInt64 = 0
    var generation: UInt64 = 1
    var phase: GamePhase = .staging
    var repairIndex = 0
    var enabledRepairCount = 1
    var repairTitle = "Utility Corner"
    var hint = "Preparing your street…"
    var coverage: Double? = nil
    var safety = "Unrepaired"
    var canLock = false
    var canRelease = false
    var canAdjust = false
    var isPaused = false
    var pauseReason: String? = nil
    var grounded = true
    var moving = false
    var facingRight = true
    var verticalVelocity: Float = 0
    var playerPosition = SCNVector3(-3.2, 0, 0)
    var coverPosition = SCNVector3(0, 3.0, 0)
    var carriageUV = CGPoint(x: 0.16, y: 0.2)
    var railPoints = [CGPoint(x: 0.16, y: 0.2),CGPoint(x: 0.16, y: 0.65),CGPoint(x: 0.72, y: 0.65),CGPoint(x: 0.72, y: 0.35),CGPoint(x: 0.45, y: 0.35)]
    var blockerRect = CGRect(x: 0.34, y: 0.18, width: 0.20, height: 0.28)
    var framing = WorldFraming()
    var diagnostic = "Baseline"
}
struct GameEvent: Identifiable {
    enum Kind: String { case step, jump, land, dash, release, coverImpact, success, retry }
    let id: UInt64
    let generation: UInt64
    let simulationTime: TimeInterval
    let kind: Kind
    var intensity: Float = 1
}
