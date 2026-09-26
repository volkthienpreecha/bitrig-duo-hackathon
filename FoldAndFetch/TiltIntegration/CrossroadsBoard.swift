import SpriteKit
import Combine

/// The cover, crate, barriers and gate share one SpriteKit physics clock.
final class CrossroadsBoard: SKScene, ObservableObject, SKPhysicsContactDelegate {
    private enum Body {
        static let cover: UInt32 = 1 << 0
        static let crate: UInt32 = 1 << 1
        static let wall: UInt32 = 1 << 2
        static let gate: UInt32 = 1 << 3
    }
    @Published var hint = "Guide the cover over the curb."
    @Published var held = false {
        didSet { if held { disk.physicsBody?.isDynamic = false; physicsWorld.speed = 0 } }
    }
    var sampleProvider: (() -> CGVector?)?
    var onPark: ((CGPoint) -> Bool)?

    private let disk = SKShapeNode(circleOfRadius: 17)
    private let crate = SKShapeNode(rectOf: CGSize(width: 22, height: 22), cornerRadius: 2)
    private let gate = SKShapeNode(rectOf: CGSize(width: 18, height: 82), cornerRadius: 3)
    private let cable = SKShapeNode()
    private let pulleyWheel = SKShapeNode(circleOfRadius: 10)
    private let latch = SKShapeNode(rectOf: CGSize(width: 7, height: 12), cornerRadius: 2)
    private let target = CGPoint(x: 426, y: 23)
    private let crateStart = CGPoint(x: 309, y: 241)
    private let gateStart = CGPoint(x: 284, y: 70)
    private let cream = UIColor(red: 0.95, green: 0.90, blue: 0.79, alpha: 1)
    private let copper = UIColor(red: 0.88, green: 0.43, blue: 0.24, alpha: 1)
    private let teal = UIColor(red: 0.18, green: 0.51, blue: 0.72, alpha: 1)
    private let asphalt = UIColor(red: 0.075, green: 0.14, blue: 0.18, alpha: 1)
    private var configured = false
    private var previous: TimeInterval?
    private var delta: TimeInterval = 0
    private var dwell = ParkDwell()
    private var fresh = false
    private var notified = false
    private var lastReport: TimeInterval = 0
    private var gateLift: CGFloat = 0
    private var boxDropped = false
    private var curbPassed = false
    private var touchingCrate = false
    private var latestTilt = CGVector.zero

    override init(size: CGSize) {
        super.init(size: size)
        scaleMode = .aspectFit
        backgroundColor = asphalt
    }
    required init?(coder: NSCoder) { fatalError("init(coder:) unavailable") }

    override func didMove(to view: SKView) {
        guard !configured else { return }
        configured = true
        physicsWorld.contactDelegate = self
        buildStreet()
        buildRoute()
        buildMechanism()
        buildCover()
        reset()
    }

    private func label(_ text: String, x: CGFloat, y: CGFloat, size: CGFloat, color: UIColor) {
        let node = SKLabelNode(text: text)
        node.fontName = "AvenirNext-DemiBold"
        node.fontSize = size
        node.fontColor = color
        node.horizontalAlignmentMode = .left
        node.position = CGPoint(x: x, y: y)
        node.zPosition = -2
        addChild(node)
    }

    private func buildStreet() {
        let ground = SKShapeNode(rect: CGRect(x: 5, y: 5, width: 470, height: 350), cornerRadius: 8)
        ground.fillColor = asphalt
        ground.strokeColor = cream.withAlphaComponent(0.55)
        ground.lineWidth = 4
        ground.physicsBody = SKPhysicsBody(edgeLoopFrom: CGRect(x: 5, y: 5, width: 470, height: 350))
        ground.physicsBody?.friction = 0.3
        ground.physicsBody?.categoryBitMask = Body.wall
        ground.zPosition = -10
        addChild(ground)

        // The socket is inset into one continuous lower pavement strip.
        let pavement = SKShapeNode(rect: CGRect(x: 8, y: 8, width: 464, height: 39))
        pavement.fillColor = UIColor(red: 0.12, green: 0.24, blue: 0.27, alpha: 1)
        pavement.strokeColor = .clear
        pavement.zPosition = -8
        addChild(pavement)
        let lip = SKShapeNode(rect: CGRect(x: 8, y: 46, width: 464, height: 3))
        lip.fillColor = copper.withAlphaComponent(0.7)
        lip.strokeColor = .clear
        lip.zPosition = -7
        addChild(lip)
        let socket = SKShapeNode(ellipseOf: CGSize(width: 58, height: 34))
        socket.position = target
        socket.fillColor = UIColor(red: 0.025, green: 0.065, blue: 0.08, alpha: 1)
        socket.strokeColor = copper
        socket.lineWidth = 3
        socket.zPosition = -6
        addChild(socket)
        let socketInner = SKShapeNode(ellipseOf: CGSize(width: 45, height: 24))
        socketInner.strokeColor = cream.withAlphaComponent(0.5)
        socketInner.lineWidth = 1
        socket.addChild(socketInner)
        for x in [403.0, 449.0] {
            let bolt = SKShapeNode(circleOfRadius: 1.6)
            bolt.position = CGPoint(x: x, y: 23)
            bolt.fillColor = cream
            bolt.strokeColor = .clear
            addChild(bolt)
        }
        for y in [178.0, 294.0] {
            for x in stride(from: 35.0, through: 450.0, by: 55.0) {
                let dash = SKShapeNode(rectOf: CGSize(width: 16, height: 1.5))
                dash.position = CGPoint(x: x, y: y)
                dash.fillColor = cream.withAlphaComponent(0.11)
                dash.strokeColor = .clear
                dash.zPosition = -7
                addChild(dash)
            }
        }
        label("横断路", x: 23, y: 166, size: 19, color: teal.withAlphaComponent(0.85))
        label("出口 →", x: 394, y: 111, size: 11, color: copper.withAlphaComponent(0.9))
        let neon = SKShapeNode(rectOf: CGSize(width: 68, height: 2))
        neon.position = CGPoint(x: 57, y: 155)
        neon.fillColor = teal
        neon.strokeColor = .clear
        neon.glowWidth = 5
        neon.zPosition = -3
        addChild(neon)
    }

    private func barrier(_ rect: CGRect, color: UIColor) {
        let shadow = SKShapeNode(rectOf: CGSize(width: rect.width + 3, height: rect.height + 3), cornerRadius: 3)
        shadow.position = CGPoint(x: rect.midX + 3, y: rect.midY - 4)
        shadow.fillColor = .black.withAlphaComponent(0.3)
        shadow.strokeColor = .clear
        shadow.zPosition = -1
        addChild(shadow)
        let node = SKShapeNode(rectOf: rect.size, cornerRadius: 2)
        node.position = CGPoint(x: rect.midX, y: rect.midY)
        node.fillColor = color
        node.strokeColor = cream.withAlphaComponent(0.7)
        node.lineWidth = 1.3
        node.physicsBody = SKPhysicsBody(rectangleOf: rect.size)
        node.physicsBody?.isDynamic = false
        node.physicsBody?.friction = 0.3
        node.physicsBody?.restitution = 0.05
        node.physicsBody?.categoryBitMask = Body.wall
        node.zPosition = 2
        addChild(node)
        let blue = color.isEqual(teal)
        let edge = SKShapeNode(rectOf: CGSize(width: max(1, rect.width - 4), height: min(3, rect.height / 4)))
        edge.position.y = rect.height / 2 - 3
        edge.fillColor = blue ? cream.withAlphaComponent(0.48) : UIColor(red: 1, green: 0.71, blue: 0.42, alpha: 1)
        edge.strokeColor = .clear
        node.addChild(edge)
        if rect.width > rect.height * 2 {
            let seamCount = Int(rect.width / 36)
            for index in 1...max(1, seamCount) {
                let x = -rect.width / 2 + CGFloat(index) * rect.width / CGFloat(seamCount + 1)
                let seam = SKShapeNode(rectOf: CGSize(width: 1.5, height: rect.height - 5))
                seam.position = CGPoint(x: x, y: -1)
                seam.fillColor = blue ? asphalt.withAlphaComponent(0.38) : UIColor(red: 0.35, green: 0.18, blue: 0.10, alpha: 0.6)
                seam.strokeColor = .clear
                node.addChild(seam)
                let grain = SKShapeNode(rectOf: CGSize(width: min(12, rect.width / CGFloat(seamCount + 1) - 5), height: 1.3))
                grain.position = CGPoint(x: x - 13, y: -rect.height / 4)
                grain.fillColor = blue ? cream.withAlphaComponent(0.22) : UIColor(red: 0.34, green: 0.15, blue: 0.08, alpha: 0.5)
                grain.strokeColor = .clear
                node.addChild(grain)
            }
        } else if rect.height > 24 {
            for y in stride(from: -rect.height / 2 + 11, to: rect.height / 2 - 4, by: 20) {
                let notch = SKShapeNode(rectOf: CGSize(width: max(2, rect.width - 4), height: 2))
                notch.position.y = y
                notch.fillColor = blue ? asphalt.withAlphaComponent(0.35) : cream.withAlphaComponent(0.2)
                notch.strokeColor = .clear
                node.addChild(notch)
            }
        }
    }

    private func buildRoute() {
        // Below the curb there is less than a cover diameter above the shelf.
        barrier(CGRect(x: 142, y: 277, width: 64, height: 13), color: copper)
        // The left shelf end stays open for the cover's return route.
        // The crate fits this 32-point slot; the cover's 34-point body does not.
        barrier(CGRect(x: 91, y: 215, width: 247, height: 13), color: teal)
        barrier(CGRect(x: 370, y: 215, width: 105, height: 13), color: teal)
        // The far lip is a real stop: a pushed crate cannot skip over the
        // narrow opening and continue across the right shelf.
        barrier(CGRect(x: 363, y: 228, width: 12, height: 43), color: teal)
        // The crate descends inside a real walled shaft and lands on its
        // counterweight stop; later tilts cannot drag the cable across the road.
        barrier(CGRect(x: 334, y: 92, width: 5, height: 120), color: copper)
        barrier(CGRect(x: 371, y: 92, width: 5, height: 120), color: copper)
        barrier(CGRect(x: 340, y: 84, width: 32, height: 7), color: copper)
        // The final route runs below the beam, once the gate has risen.
        barrier(CGRect(x: 326, y: 128, width: 126, height: 16), color: copper)
        label("DROP THE CRATE", x: 281, y: 286, size: 8, color: cream.withAlphaComponent(0.8))
        label("GO UNDER", x: 362, y: 150, size: 8, color: cream.withAlphaComponent(0.65))
        label("SEAT THE COVER", x: 381, y: 68, size: 8, color: cream.withAlphaComponent(0.76))
    }

    private func buildMechanism() {
        crate.fillColor = copper
        crate.strokeColor = cream
        crate.lineWidth = 2
        // The visible timber overhangs a compact 18-point hitbox. At the
        // slot's right stop caps its center near x354, clear of both the
        // shelf at x370 and the shaft wall at x371.
        crate.physicsBody = SKPhysicsBody(rectangleOf: CGSize(width: 18, height: 18))
        crate.physicsBody?.allowsRotation = false
        crate.physicsBody?.mass = 0.08
        crate.physicsBody?.categoryBitMask = Body.crate
        crate.physicsBody?.collisionBitMask = Body.cover | Body.wall
        crate.physicsBody?.contactTestBitMask = Body.cover
        crate.physicsBody?.friction = 0.22
        crate.physicsBody?.restitution = 0.03
        crate.physicsBody?.linearDamping = 1.7
        // The crate is not driven by the board's horizontal gravity. Its
        // horizontal motion comes from a physical cover/crate collision.
        crate.physicsBody?.affectedByGravity = false
        crate.physicsBody?.usesPreciseCollisionDetection = true
        crate.zPosition = 5
        addChild(crate)
        let inset = SKShapeNode(rectOf: CGSize(width: 16, height: 16), cornerRadius: 1)
        inset.fillColor = UIColor(red: 0.59, green: 0.30, blue: 0.15, alpha: 1)
        inset.strokeColor = cream.withAlphaComponent(0.52)
        inset.lineWidth = 1
        crate.addChild(inset)
        let crateCross = SKShapeNode(rectOf: CGSize(width: 16, height: 2))
        crateCross.fillColor = cream.withAlphaComponent(0.75)
        crateCross.strokeColor = .clear
        crateCross.zRotation = .pi / 4
        crate.addChild(crateCross)
        let otherBrace = SKShapeNode(rectOf: CGSize(width: 16, height: 2))
        otherBrace.fillColor = cream.withAlphaComponent(0.75)
        otherBrace.strokeColor = .clear
        otherBrace.zRotation = -.pi / 4
        crate.addChild(otherBrace)
        for x in [-7.0, 7.0] {
            let nail = SKShapeNode(circleOfRadius: 1)
            nail.position = CGPoint(x: x, y: 7)
            nail.fillColor = cream
            nail.strokeColor = .clear
            crate.addChild(nail)
        }
        latch.position = CGPoint(x: 296, y: 233)
        latch.fillColor = cream
        latch.strokeColor = copper
        latch.lineWidth = 1
        latch.zPosition = 6
        addChild(latch)

        let track = SKShapeNode(rect: CGRect(x: 270, y: 24, width: 28, height: 166), cornerRadius: 3)
        track.fillColor = .black.withAlphaComponent(0.28)
        track.strokeColor = copper.withAlphaComponent(0.7)
        track.lineWidth = 2
        track.zPosition = 0
        addChild(track)
        gate.fillColor = teal
        gate.strokeColor = cream
        gate.lineWidth = 2
        gate.physicsBody = SKPhysicsBody(rectangleOf: CGSize(width: 18, height: 82))
        gate.physicsBody?.isDynamic = false
        gate.physicsBody?.friction = 0.35
        gate.physicsBody?.categoryBitMask = Body.gate
        gate.zPosition = 4
        addChild(gate)
        for y in [-27.0, -11.0, 5.0, 21.0] {
            let slot = SKShapeNode(rectOf: CGSize(width: 9, height: 2))
            slot.position.y = y
            slot.fillColor = asphalt.withAlphaComponent(0.8)
            slot.strokeColor = .clear
            gate.addChild(slot)
        }
        cable.strokeColor = cream.withAlphaComponent(0.85)
        cable.lineWidth = 1.5
        cable.zPosition = 1
        addChild(cable)
        pulleyWheel.position = CGPoint(x: 354, y: 308)
        pulleyWheel.fillColor = asphalt
        pulleyWheel.strokeColor = copper
        pulleyWheel.lineWidth = 3
        pulleyWheel.zPosition = 3
        addChild(pulleyWheel)
        let axle = SKShapeNode(circleOfRadius: 2.5)
        axle.fillColor = cream
        axle.strokeColor = .clear
        pulleyWheel.addChild(axle)
        let spoke = SKShapeNode(rectOf: CGSize(width: 14, height: 1.5))
        spoke.fillColor = cream.withAlphaComponent(0.76)
        spoke.strokeColor = .clear
        pulleyWheel.addChild(spoke)
        label("PULLEY / GATE", x: 273, y: 194, size: 8, color: cream.withAlphaComponent(0.72))
    }

    private func buildCover() {
        let shadow = SKShapeNode(circleOfRadius: 19)
        shadow.position = CGPoint(x: 3, y: -5)
        shadow.fillColor = .black.withAlphaComponent(0.48)
        shadow.strokeColor = .clear
        shadow.zPosition = -1
        disk.addChild(shadow)
        disk.fillColor = copper
        disk.strokeColor = cream
        disk.lineWidth = 2.5
        let plate = SKShapeNode(circleOfRadius: 14)
        plate.fillColor = teal
        plate.strokeColor = asphalt
        plate.lineWidth = 1.5
        disk.addChild(plate)
        let ring = SKShapeNode(circleOfRadius: 11)
        ring.strokeColor = cream.withAlphaComponent(0.85)
        ring.lineWidth = 1.5
        disk.addChild(ring)
        for x in [-6.0, 0, 6] {
            let rib = SKShapeNode(rectOf: CGSize(width: 2, height: 15), cornerRadius: 1)
            rib.position.x = x
            rib.fillColor = asphalt
            rib.strokeColor = .clear
            disk.addChild(rib)
        }
        disk.physicsBody = SKPhysicsBody(circleOfRadius: 17)
        disk.physicsBody?.allowsRotation = false
        disk.physicsBody?.mass = 0.13
        disk.physicsBody?.categoryBitMask = Body.cover
        disk.physicsBody?.collisionBitMask = Body.crate | Body.wall | Body.gate
        disk.physicsBody?.contactTestBitMask = Body.crate
        disk.physicsBody?.restitution = 0.04
        disk.physicsBody?.friction = 0.28
        disk.physicsBody?.linearDamping = 2.1
        disk.physicsBody?.usesPreciseCollisionDetection = true
        disk.zPosition = 6
        addChild(disk)
    }

    func reset() {
        disk.childNode(withName: "hold-ring")?.removeFromParent()
        held = false
        notified = false
        boxDropped = false
        curbPassed = false
        touchingCrate = false
        latestTilt = .zero
        gateLift = 0
        dwell = ParkDwell()
        previous = nil
        physicsWorld.speed = 0
        disk.physicsBody?.isDynamic = true
        disk.physicsBody?.velocity = .zero
        disk.physicsBody?.angularVelocity = 0
        disk.position = CGPoint(x: 112, y: 286)
        // The small retaining pin releases only when the cover gets over
        // the curb. This keeps the crate from solving itself on the first tilt.
        crate.physicsBody?.isDynamic = false
        crate.physicsBody?.velocity = .zero
        crate.physicsBody?.angularVelocity = 0
        crate.position = crateStart
        latch.isHidden = false
        gate.position = gateStart
        pulleyWheel.zRotation = 0
        updateCable()
        hint = "Tilt up over the curb, then roll the crate into the slot."
    }

    override func update(_ time: TimeInterval) {
        delta = min(1.0 / 30, max(0, time - (previous ?? time)))
        previous = time
        guard !held else { physicsWorld.speed = 0; return }
        let sample = sampleProvider?()
        fresh = sample != nil
        physicsWorld.speed = fresh ? 1 : 0
        let g = sample ?? .zero
        latestTilt = g
        physicsWorld.gravity = CGVector(dx: g.dx * 3.2, dy: g.dy * 3.2 - 0.5)
        // A small constant downward load lets the crate fall through its slot.
        // There is intentionally no horizontal force from tilt on the crate.
        if curbPassed, let body = crate.physicsBody {
            // A sustained horizontal push exists only during an actual
            // SpriteKit body contact, and only when the cover is to the left.
            let pushing = touchingCrate && disk.position.x < crate.position.x &&
                abs(disk.position.y - crate.position.y) < 31
            let push = pushing ? max(0, g.dx) * 52 * body.mass : 0
            let drop = crate.position.x > 345 ? -42 * body.mass : -22 * body.mass
            body.applyForce(CGVector(dx: push, dy: drop))
        }
        guard time - lastReport > 0.25 else { return }
        lastReport = time
        let speed = hypot(disk.physicsBody?.velocity.dx ?? 0, disk.physicsBody?.velocity.dy ?? 0)
        let text: String
        if !fresh { text = "Motion paused · connect your iPad or choose Manual" }
        else if dwell.elapsed > 0 { text = "Hold steady over the socket…" }
        else if !boxDropped && crate.position.x > 345 { text = "Ease left to let the crate fall" }
        else if !boxDropped { text = touchingCrate ? "Push the crate toward the slot" : "Touch the wooden crate to push it" }
        else if gateLift < 60 { text = "Counterweight lowering the gate…" }
        else if speed > 48 { text = "Counter-tilt to slow the cover" }
        else { text = "Return left, pass the raised gate, then go under" }
        if hint != text { hint = text }
    }

    override func didSimulatePhysics() {
        guard !held else { return }
        if !curbPassed && disk.position.x > 225 && disk.position.y > 280 { releaseLatch() }
        if crate.position.y < 210 && crate.position.x >= 338 && crate.position.x <= 370 { boxDropped = true }
        // The dynamic crate supplies the displacement for the colliding gate.
        // No timer, tap or goal proximity opens it.
        let fall = max(0, crateStart.y - crate.position.y)
        gateLift = boxDropped ? min(94, max(0, fall * 0.72)) : 0
        gate.position = CGPoint(x: gateStart.x, y: gateStart.y + gateLift)
        pulleyWheel.zRotation = -gateLift / 10
        updateCable()
        limitSpeed(disk, to: 62)
        limitSpeed(crate, to: 55)
        guard !notified else { return }
        let velocity = disk.physicsBody?.velocity ?? .zero
        let distance = hypot(disk.position.x - target.x, disk.position.y - target.y)
        let ready = dwell.step(distance: boxDropped && gateLift > 60 ? distance : .infinity,
                               speed: hypot(velocity.dx, velocity.dy), delta: delta, fresh: fresh)
        guard ready else { return }
        let offset = CGPoint(x: (disk.position.x - target.x) / 20, y: (disk.position.y - target.y) / 20)
        guard onPark?(offset) == true else { dwell = ParkDwell(); return }
        notified = true
        held = true
        hint = "Cover seated · close Duo to release it"
        let clamp = SKShapeNode(circleOfRadius: 21)
        clamp.name = "hold-ring"
        clamp.strokeColor = cream
        clamp.lineWidth = 3
        disk.addChild(clamp)
    }

    private func limitSpeed(_ node: SKNode, to maximum: CGFloat) {
        guard let body = node.physicsBody else { return }
        let v = body.velocity
        let speed = hypot(v.dx, v.dy)
        if speed > maximum {
            body.velocity = CGVector(dx: v.dx * maximum / speed, dy: v.dy * maximum / speed)
        }
    }

    func didBegin(_ contact: SKPhysicsContact) {
        if (contact.bodyA.categoryBitMask | contact.bodyB.categoryBitMask) == (Body.cover | Body.crate) {
            releaseLatch()
            touchingCrate = true
            if disk.position.x < crate.position.x, let body = crate.physicsBody {
                body.applyImpulse(CGVector(dx: max(0, latestTilt.dx) * 9 * body.mass, dy: 0))
            }
        }
    }

    func didEnd(_ contact: SKPhysicsContact) {
        if (contact.bodyA.categoryBitMask | contact.bodyB.categoryBitMask) == (Body.cover | Body.crate) {
            touchingCrate = false
        }
    }

    private func releaseLatch() {
        guard !curbPassed else { return }
        curbPassed = true
        crate.physicsBody?.isDynamic = true
        latch.isHidden = true
    }

    private func updateCable() {
        let path = CGMutablePath()
        path.move(to: CGPoint(x: crate.position.x, y: crate.position.y + 12))
        path.addLine(to: CGPoint(x: crate.position.x, y: 308))
        path.addLine(to: CGPoint(x: 354, y: 318))
        path.addLine(to: CGPoint(x: 284, y: 318))
        path.addLine(to: CGPoint(x: 284, y: gate.position.y + 42))
        cable.path = path
    }
}
