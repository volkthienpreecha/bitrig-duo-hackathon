import SceneKit
import SwiftUI

#if canImport(UIKit)
private typealias StreetColor = UIColor
private typealias StreetScalar = Float
#else
private typealias StreetColor = NSColor
private typealias StreetScalar = CGFloat
#endif

/// A persistent physical street. Mount at most one TiltStreetView; moving between displays keeps this object.
@MainActor final class TiltStreetWorld: NSObject, ObservableObject {
    enum Phase: String { case waiting, dropping, safe, failed, won }
    @Published private(set) var phase: Phase = .waiting
    @Published private(set) var coverage: Double = 0
    @Published private(set) var rendererReady = false
    @Published private(set) var hint = "Guide the cover, then close Duo."
    let scene = SCNScene()
    let camera = SCNNode()
    let player = SCNNode()
    let playerVisualRoot = SCNNode()
    private(set) var cover = SCNNode()
    private(set) var generation: UInt64 = 0
    private(set) var simulationTime: TimeInterval = 0
    private(set) var supportDwell: TimeInterval = 0
    private(set) var grounded = false
    private(set) var lastSupportCount = 0
    private let objects = SCNNode()
    private var burstDirection: StreetScalar = 0
    private var burstRemaining: TimeInterval = 0
    private var dashUsed = false
    private var elapsedSinceDrop: TimeInterval = 0
    private var coverageTimer: TimeInterval = 0
    private var previousRenderTime: TimeInterval?
    private var currentDelta: TimeInterval = 0
    private var facingRight = true
    private var lastPlayerPosition: SCNVector3?
    private var playerVelocity = SCNVector3Zero
    private var lastCoverPosition: SCNVector3?
    private var lastCoverOrientation: simd_quatf?
    #if canImport(UIKit)
    private weak var activeView: SCNView?
    private var clock: StreetClock?
    private var clockToken: UInt64 = 0
    #endif

    static let openingRadius = 1.15
    static let coverRadius = 1.375
    // Sixteen-sided recess: 2.81m flat-to-flat, retaining the intended 3cm minimum radial gap.
    static let recessVertexRadius = 1.405 / cos(Double.pi / 16)
    static let maximumJumpReach = 2.0 * (2 * 2.8 / 9.81) + 0.58

    override init() {
        super.init()
        scene.background.contents = StreetColor(red: 0.10,green: 0.16,blue: 0.20,alpha: 1)
        scene.physicsWorld.gravity = SCNVector3(0,-9.81,0)
        scene.physicsWorld.timeStep = 1.0/120
        scene.rootNode.addChildNode(objects)
        camera.name = "street-camera"; camera.camera = SCNCamera(); camera.camera?.usesOrthographicProjection = true; camera.camera?.projectionDirection = .horizontal; camera.camera?.orthographicScale = 4.1; camera.camera?.zNear = 0.05; camera.camera?.zFar = 100
        camera.position = SCNVector3(0,6.8,10.5); camera.look(at: SCNVector3(0,0.7,0)); scene.rootNode.addChildNode(camera)
        let ambient = SCNNode(); ambient.light = SCNLight(); ambient.light?.type = .ambient; ambient.light?.intensity = 800; scene.rootNode.addChildNode(ambient)
        let sunlight = SCNNode(); sunlight.light = SCNLight(); sunlight.light?.type = .directional; sunlight.light?.intensity = 1200; sunlight.eulerAngles = SCNVector3(-0.8,-0.5,0); scene.rootNode.addChildNode(sunlight)
        player.name = "player"; player.addChildNode(playerVisualRoot); playerVisualRoot.position.y = -0.25
        let sprite = SCNPlane(width: 0.80,height: 0.80)
        let m = SCNMaterial(); m.lightingModel = .constant; m.isDoubleSided = true
        #if canImport(UIKit)
        if let url = Bundle.main.url(forResource: "kaprao-idle",withExtension: "png"),let image = UIImage(contentsOfFile: url.path) { m.diffuse.contents = image }
        else { m.diffuse.contents = StreetColor.systemOrange }
        #else
        m.diffuse.contents = StreetColor.systemOrange
        #endif
        m.transparencyMode = .aOne; sprite.materials = [m]
        let spriteNode = SCNNode(geometry: sprite); spriteNode.position.y = 0.38
        if let url = Bundle.main.url(forResource: "kaprao-sprite",withExtension: "scn"),let model = try? SCNScene(url: url),let root = model.rootNode.childNode(withName: "KapraoSpriteRoot",recursively: true) { root.removeFromParentNode(); playerVisualRoot.addChildNode(root) }
        else { playerVisualRoot.addChildNode(spriteNode) }
        // One explicit camera-facing visual pivot keeps the selected model at scale 1.
        playerVisualRoot.enumerateChildNodes { node,_ in
            node.constraints = node.constraints?.filter { !($0 is SCNBillboardConstraint) }
        }
        reset()
        setOutsidePresentation(false)
    }
    /// Presentation only: the outside cover uses an overhead view of the same physical scene.
    func setOutsidePresentation(_ outside: Bool) {
        SCNTransaction.begin(); SCNTransaction.disableActions = true
        camera.position = outside ? SCNVector3(0,10,4) : SCNVector3(0,6.8,10.5)
        camera.look(at: SCNVector3(0,0.7,0))
        // Rotate around the feet, keeping their position and the existing horizontal mirror.
        // Orthographic projection means this orientation faces the camera everywhere on the lane.
        playerVisualRoot.simdOrientation = camera.simdOrientation
        SCNTransaction.commit()
    }
    private func material(_ color: StreetColor,metal: Double = 0) -> SCNMaterial {
        let m = SCNMaterial(); m.diffuse.contents = color; m.metalness.contents = metal; m.roughness.contents = 0.72; return m
    }
    private func box(_ name: String,width: Double,height: Double,depth: Double,at p: SCNVector3,color: StreetColor) -> SCNNode {
        let n = SCNNode(geometry: SCNBox(width: width,height: height,length: depth,chamferRadius: 0)); n.name = name; n.position = p; n.geometry?.materials = [material(color)]; objects.addChildNode(n); return n
    }
    private func sector(inner: Double,outer: Double,bottom: Double,top: Double,index: Int,name: String,color: StreetColor) -> SCNNode {
        let a = Double(index)*2 * .pi/16,b = Double(index+1)*2 * .pi/16
        var vertices: [SCNVector3] = []
        for y in [bottom,top] { for (r,t) in [(inner,a),(outer,a),(outer,b),(inner,b)] { vertices.append(SCNVector3(r*cos(t),y,r*sin(t))) } }
        let indices: [Int32] = [0,1,2,0,2,3,4,6,5,4,7,6,0,5,1,0,4,5,1,6,2,1,5,6,2,7,3,2,6,7,3,4,0,3,7,4]
        let g = SCNGeometry(sources: [SCNGeometrySource(vertices: vertices)],elements: [SCNGeometryElement(indices: indices,primitiveType: .triangles)]); g.materials = [material(color)]
        let n = SCNNode(geometry: g); n.name = name
        n.physicsBody = SCNPhysicsBody(type: .static,shape: SCNPhysicsShape(geometry: g,options: [.type: SCNPhysicsShape.ShapeType.concavePolyhedron,.collisionMargin: 0.0])); n.physicsBody?.friction = 0.95; n.physicsBody?.restitution = 0; n.physicsBody?.contactTestBitMask = -1
        objects.addChildNode(n); return n
    }
    func reset() {
        generation += 1
        player.removeFromParentNode()
        for node in objects.childNodes { node.removeFromParentNode() }
        phase = .waiting; coverage = 0; hint = "Guide the cover, then close Duo."
        supportDwell = 0; grounded = false; lastSupportCount = 0; dashUsed = false; burstRemaining = 0; burstDirection = 0; elapsedSinceDrop = 0; coverageTimer = 0; previousRenderTime = nil; currentDelta = 0; lastPlayerPosition = nil; playerVelocity = SCNVector3Zero; lastCoverPosition = nil; lastCoverOrientation = nil
        for i in 0..<16 {
            _ = sector(inner: 1.15,outer: Self.recessVertexRadius,bottom: -0.55,top: -0.14,index: i,name: "rim-\(i)",color: StreetColor(red: 0.38,green: 0.46,blue: 0.48,alpha: 1))
            _ = sector(inner: Self.recessVertexRadius,outer: 6,bottom: -0.55,top: 0,index: i,name: "road-\(i)",color: StreetColor(red: 0.20,green: 0.27,blue: 0.30,alpha: 1))
        }
        for x in [-3.8,-3.3,-2.8,2.8,3.3,3.8] { _ = box("crosswalk",width: 0.24,height: 0.006,depth: 1.1,at: SCNVector3(x,0.004,0),color: .white) }
        for x in [-3.5,-2.7,2.7,3.5] { for z in [-0.9,0.9] { _ = box("lane-barrier",width: 0.5,height: 0.34,depth: 0.10,at: SCNVector3(x,0.17,z),color: .systemYellow) } }
        _ = box("curb",width: 9,height: 0.15,depth: 0.18,at: SCNVector3(0,0.075,-1.9),color: .lightGray)
        _ = box("checkpoint",width: 0.70,height: 0.006,depth: 0.55,at: SCNVector3(-3.2,0.006,0),color: .systemMint)
        let toy = SCNNode(geometry: SCNSphere(radius: 0.20)); toy.name = "goal-toy"; toy.position = SCNVector3(3.35,0.20,0); toy.geometry?.materials = [material(.systemPink)]; objects.addChildNode(toy)
        let g = SCNCylinder(radius: Self.coverRadius,height: 0.14); g.radialSegmentCount = 64
        cover = SCNNode(geometry: g); cover.name = "cover"; g.materials = [material(.systemTeal,metal: 0.7)]; cover.position = SCNVector3(0,2.7,0); cover.isHidden = true; objects.addChildNode(cover)
        for x in [-0.7,-0.35,0,0.35,0.7] { let line = SCNNode(geometry: SCNBox(width: 0.035,height: 0.006,length: 1.65,chamferRadius: 0)); line.position = SCNVector3(x,0.073,0); line.geometry?.materials = [material(.darkGray)]; cover.addChildNode(line) }
        player.physicsBody = SCNPhysicsBody(type: .dynamic,shape: SCNPhysicsShape(geometry: SCNSphere(radius: 0.25),options: [.collisionMargin: 0.0])); player.physicsBody?.mass = 1; player.physicsBody?.friction = 0.7; player.physicsBody?.restitution = 0; player.physicsBody?.damping = 0; player.physicsBody?.angularVelocityFactor = SCNVector3Zero; player.physicsBody?.velocityFactor = SCNVector3(1,1,0); player.physicsBody?.categoryBitMask = 1; player.physicsBody?.contactTestBitMask = -1
        objects.addChildNode(player); recoverPlayer()
    }
    /// Board target offsets map directly to 0.018m per normalized unit. This exact pose becomes dynamic once.
    /// Values beyond the target remain meaningful physical errors (clamped only to the street extent).
    func drop(offset: CGPoint) {
        guard phase == .waiting else { return }
        let x = min(2,max(-2,Double(offset.x)*0.018)),z = min(2,max(-2,Double(offset.y)*0.018))
        cover.isHidden = false; cover.position = SCNVector3(x,2.7,z); cover.eulerAngles = SCNVector3Zero
        let shape = SCNPhysicsShape(geometry: cover.geometry!,options: [.collisionMargin: 0.0])
        cover.physicsBody = SCNPhysicsBody(type: .dynamic,shape: shape); cover.physicsBody?.mass = 60; cover.physicsBody?.friction = 0.95; cover.physicsBody?.restitution = 0.02; cover.physicsBody?.damping = 0.1; cover.physicsBody?.angularDamping = 0.5; cover.physicsBody?.categoryBitMask = 4; cover.physicsBody?.contactTestBitMask = -1; cover.physicsBody?.velocity = SCNVector3Zero; cover.physicsBody?.angularVelocity = SCNVector4(0,0,0,0); cover.physicsBody?.resetTransform()
        phase = .dropping; hint = "Landing…"; elapsedSinceDrop = 0; supportDwell = 0
    }
    func moveRight() { move(direction: 1) }
    func moveLeft() { move(direction: -1) }
    private func move(direction: StreetScalar) { guard phase != .won else { return }; burstDirection = direction; burstRemaining = 0.35; facingRight = direction > 0; playerVisualRoot.scale.x = facingRight ? 1 : -1 }
    func jump() { guard grounded,phase != .won else { return }; player.physicsBody?.applyForce(SCNVector3(0,2.8,0),asImpulse: true); grounded = false }
    func dash() { guard !grounded,!dashUsed,phase != .won else { return }; dashUsed = true; player.physicsBody?.applyForce(SCNVector3(0,min(0,-3.5-playerVelocity.y),0),asImpulse: true) }
    private func recoverPlayer() { player.position = SCNVector3(-3.2,0.255,0); player.physicsBody?.clearAllForces(); player.physicsBody?.velocity = SCNVector3Zero; player.physicsBody?.angularVelocity = SCNVector4(0,0,0,0); player.physicsBody?.resetTransform(); burstRemaining = 0; dashUsed = false; grounded = false; lastPlayerPosition = nil; playerVelocity = SCNVector3Zero }

    // Invoked by the one active SCNView's delegate. SCNView alone advances SceneKit physics.
    func beforePhysics(at time: TimeInterval) {
        currentDelta = scene.isPaused ? 0 : min(1.0/15,max(0,time-(previousRenderTime ?? time))); previousRenderTime = time
        simulationTime += currentDelta
        burstRemaining = max(0,burstRemaining-currentDelta)
        guard currentDelta > 0 else { return }
        let desiredX: StreetScalar = burstRemaining > 0 ? burstDirection*2 : 0
        player.physicsBody?.applyForce(SCNVector3(desiredX-playerVelocity.x,0,0),asImpulse: true)
    }
    func afterPhysics() {
        guard !scene.isPaused else { return }
        let pp = player.presentation.worldPosition
        if let last = lastPlayerPosition,currentDelta > 0 { let dt = StreetScalar(currentDelta); playerVelocity = SCNVector3((pp.x-last.x)/dt,(pp.y-last.y)/dt,(pp.z-last.z)/dt) }; lastPlayerPosition = pp
        let pv = playerVelocity
        let contacts = player.physicsBody.map { scene.physicsWorld.contactTest(with: $0,options: nil) } ?? []
        grounded = pv.y < 0.4 && contacts.contains { abs($0.contactNormal.y)>0.7 && $0.contactPoint.y < pp.y-0.10 }
        if grounded { dashUsed = false }
        if pp.y < -2 || abs(pp.x)>4.5 { recoverPlayer(); if phase == .safe { hint = "Try again: swipe right to reach the toy." } }
        if phase == .dropping || phase == .safe { checkCover() }
        if phase == .safe,pp.x > 3.10,grounded { phase = .won; hint = "Street repaired! Kaprao found the toy."; burstRemaining = 0 }
    }
    private func checkCover() {
        guard let body = cover.physicsBody else { return }
        elapsedSinceDrop += currentDelta; coverageTimer += currentDelta
        let p = cover.presentation.worldPosition,t = cover.presentation.simdWorldTransform
        let tilt = acos(Double(min(1,max(-1,t.columns.1.y))))
        var speed = Double.infinity,spin = Double.infinity
        let orientation = simd_quatf(t)
        if let last = lastCoverPosition,let lastOrientation = lastCoverOrientation,currentDelta > 0 {
            speed = sqrt(pow(Double(p.x-last.x),2)+pow(Double(p.y-last.y),2)+pow(Double(p.z-last.z),2))/currentDelta
            spin = 2*acos(min(1,Double(abs(simd_dot(orientation.vector,lastOrientation.vector)))))/currentDelta
        }
        lastCoverPosition = p; lastCoverOrientation = orientation
        if coverageTimer >= 0.10 {
            coverage = Self.projectedCoverage(center: CGPoint(x: Double(p.x),y: Double(p.z)),axisA: CGPoint(x: Double(t.columns.0.x)*Self.coverRadius,y: Double(t.columns.0.z)*Self.coverRadius),axisB: CGPoint(x: Double(t.columns.2.x)*Self.coverRadius,y: Double(t.columns.2.z)*Self.coverRadius)); coverageTimer = 0
        }
        let contacts = scene.physicsWorld.contactTest(with: body,options: nil)
        var ids = Set<String>(),points: [CGPoint] = []
        for contact in contacts {
            let other = contact.nodeA === cover ? contact.nodeB : contact.nodeA
            guard let name = other.name,name.hasPrefix("rim-"),abs(contact.contactNormal.y)>0.7,contact.contactPoint.y < p.y+0.01,abs(contact.contactPoint.y+0.14)<0.04 else { continue }
            if ids.insert(name).inserted { points.append(CGPoint(x: Double(contact.contactPoint.x),y: Double(contact.contactPoint.z))) }
        }
        lastSupportCount = ids.count
        let containsOpening = hypot(Double(p.x),Double(p.z))+Self.openingRadius+0.03 <= Self.coverRadius*cos(tilt)
        let topDifference = abs(Double(p.y)+0.07*cos(tilt))+Self.coverRadius*sin(tilt)
        let valid = containsOpening && topDifference <= 0.03 && tilt <= 5 * .pi/180 && speed <= 0.05 && spin <= 0.1 && Self.supportsSurround(center: CGPoint(x: Double(p.x),y: Double(p.z)),contacts: points)
        supportDwell = valid ? supportDwell+currentDelta : 0
        if supportDwell >= 0.40 { phase = .safe; hint = "Safe to cross · Swipe right toward the toy." }
        else if elapsedSinceDrop >= 5 || p.y < -2 { phase = .failed; hint = "Coverage ~\(Int(coverage*100))% · Unsafe. Retry to guide again." }
        else { phase = .dropping; hint = speed > 0.08 ? "Landing…" : "Coverage ~\(Int(coverage*100))% · Checking support…" }
    }
    static func supportsSurround(center: CGPoint,contacts: [CGPoint]) -> Bool {
        guard contacts.count >= 3 else { return false }
        let angles = contacts.map { atan2(Double($0.y-center.y),Double($0.x-center.x)) }.sorted()
        var maximumGap = angles[0]+2 * .pi-angles[angles.count-1]
        for i in 1..<angles.count { maximumGap = max(maximumGap,angles[i]-angles[i-1]) }
        return maximumGap < .pi-0.02
    }
    static func projectedCoverage(center: CGPoint,axisA: CGPoint,axisB: CGPoint) -> Double {
        let det = axisA.x*axisB.y-axisA.y*axisB.x
        guard abs(det)>0.0001 else { return 0 }
        var total = 0,covered = 0
        let apothem = openingRadius*cos(.pi/16)
        for ix in 0..<41 { for iz in 0..<41 {
            let x = (Double(ix)+0.5)/41*2.3-1.15,z = (Double(iz)+0.5)/41*2.3-1.15
            guard (0..<16).allSatisfy({ i in let a = (Double(i)+0.5)*2 * .pi/16; return x*cos(a)+z*sin(a) <= apothem }) else { continue }
            total += 1
            let dx = x-Double(center.x),dz = z-Double(center.y)
            let u = (dx*Double(axisB.y)-dz*Double(axisB.x))/Double(det),v = (Double(axisA.x)*dz-Double(axisA.y)*dx)/Double(det)
            if u*u+v*v <= 1 { covered += 1 }
        } }
        return total == 0 ? 0 : Double(covered)/Double(total)
    }
    #if canImport(UIKit)
    fileprivate func attach(_ view: SCNView) {
        if let old = activeView,old !== view { old.isPlaying = false; old.delegate = nil; old.scene = nil }
        clockToken += 1; previousRenderTime = nil; rendererReady = false
        let delegate = StreetClock(world: self,token: clockToken); clock = delegate; activeView = view
        view.scene = scene; view.pointOfView = camera; view.delegate = delegate; view.isPlaying = true
    }
    fileprivate func resize(_ view: SCNView) {
        guard activeView === view,view.bounds.width > 1,view.bounds.height > 1 else { return }
        // Fit the route horizontally; SceneKit derives vertical extent from the actual viewport.
        // This also avoids retaining a huge scale from a transient narrow layout pass.
        camera.camera?.orthographicScale = 4.1
    }
    fileprivate func windowChanged(_ view: SCNView) {
        guard activeView === view else { return }
        if view.window == nil { rendererReady = false }
        view.isPlaying = view.window != nil; previousRenderTime = nil; resize(view)
    }
    fileprivate func detach(_ view: SCNView) {
        guard activeView === view else { return }; rendererReady = false; view.isPlaying = false; view.delegate = nil; view.scene = nil; activeView = nil; clock = nil; previousRenderTime = nil
    }
    fileprivate func tickBefore(_ token: UInt64,time: TimeInterval) { guard token == clockToken,activeView != nil else { return }; beforePhysics(at: time) }
    fileprivate func tickAfter(_ token: UInt64) { guard token == clockToken,activeView != nil else { return }; afterPhysics() }
    fileprivate func frameRendered(_ token: UInt64) {
        guard token == clockToken,let view = activeView,view.window != nil else { return }
        if !rendererReady { rendererReady = true }
    }
    #endif
}

#if canImport(UIKit)
private final class StreetClock: NSObject, SCNSceneRendererDelegate {
    weak var world: TiltStreetWorld?
    let token: UInt64
    private let pendingLock = NSLock()
    private var pending = false
    init(world: TiltStreetWorld,token: UInt64) { self.world = world; self.token = token }
    nonisolated func renderer(_ renderer: any SCNSceneRenderer,didRenderScene scene: SCNScene,atTime time: TimeInterval) {
        // SceneKit holds its scene lock during callbacks. Never wait for main here:
        // SwiftUI may already be waiting for that same lock to commit a camera change.
        pendingLock.lock()
        guard !pending else { pendingLock.unlock(); return }
        pending = true; pendingLock.unlock()
        DispatchQueue.main.async { [weak self] in
            guard let self else { return }
            // Observe the completed simulation and prepare forces for its next frame.
            // SCNView remains the sole physics clock; coalesce while main is busy.
            self.world?.tickBefore(self.token,time: time)
            self.world?.tickAfter(self.token)
            self.world?.frameRendered(self.token)
            self.pendingLock.lock(); self.pending = false; self.pendingLock.unlock()
        }
    }
}
private final class StreetSCNView: SCNView {
    weak var streetWorld: TiltStreetWorld?
    override func didMoveToWindow() { super.didMoveToWindow(); streetWorld?.windowChanged(self) }
    override func layoutSubviews() { super.layoutSubviews(); streetWorld?.resize(self) }
}
struct TiltStreetView: UIViewRepresentable {
    @ObservedObject var world: TiltStreetWorld
    func makeUIView(context: Context) -> SCNView {
        let view = StreetSCNView(frame: .zero); view.streetWorld = world; view.backgroundColor = .clear; view.antialiasingMode = .multisampling4X; view.preferredFramesPerSecond = 60; view.autoenablesDefaultLighting = false; view.allowsCameraControl = false
        world.attach(view); return view
    }
    func updateUIView(_ view: SCNView,context: Context) { view.pointOfView = world.camera }
    func makeCoordinator() -> Coordinator { Coordinator(world: world) }
    static func dismantleUIView(_ view: SCNView,coordinator: Coordinator) { coordinator.world.detach(view) }
    final class Coordinator { let world: TiltStreetWorld; init(world: TiltStreetWorld) { self.world = world } }
}
#endif
