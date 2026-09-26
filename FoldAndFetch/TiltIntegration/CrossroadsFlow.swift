import Foundation
import CoreGraphics

/// No UI lifecycle callback can independently create a second release.
struct CrossroadsFlow {
    enum Display { case inside, outside, unknown }
    static func display(size: CGSize, horizontalDivision: Bool, activeDivision: Bool,
                        hingeKnown: Bool, hingeClosed: Bool, sawDivision: Bool) -> Display {
        guard size.width.isFinite, size.height.isFinite, size.width > 1, size.height > 1 else { return .unknown }
        if horizontalDivision { return .inside }
        if activeDivision { return .unknown }
        if hingeKnown && hingeClosed { return .outside }
        if !sawDivision && !hingeKnown { return .inside }
        return .unknown
    }
    private(set) var display: Display = .unknown
    private(set) var active = false
    private(set) var placement: CGPoint?
    private(set) var released = false

    mutating func park(offset: CGPoint) {
        guard display == .inside, active, placement == nil, !released,
              offset.x.isFinite, offset.y.isFinite else { return }
        placement = offset
    }
    @discardableResult mutating func updateDisplay(_ display: Display, active: Bool, renderReady: Bool = false) -> Bool {
        self.display = display; self.active = active
        guard display == .outside, active, renderReady, placement != nil, !released else { return false }
        released = true
        return true
    }
    mutating func reset() { placement = nil; released = false }
}

struct ParkDwell {
    private(set) var elapsed: TimeInterval = 0
    var ready: Bool { elapsed >= 0.6 }
    @discardableResult mutating func step(distance: Double, speed: Double, delta: TimeInterval, fresh: Bool) -> Bool {
        if fresh && distance.isFinite && speed.isFinite && distance <= 20 && speed < 8 {
            elapsed += min(1.0/30, max(0,delta))
        } else { elapsed = 0 }
        return ready
    }
}
