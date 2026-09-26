import SceneKit
import SwiftUI

#if canImport(UIKit)
private typealias StreetColor = UIColor
private typealias StreetScalar = Float
#else
private typealias StreetColor = NSColor
private typealias StreetScalar = CGFloat
#endif

/// SceneKit sends contacts on its physics thread. Copy only the contact data we need;
/// querying the Bullet world from the UI thread can race its next simulation step.
private final class StreetContacts: NSObject, SCNPhysicsContactDelegate, @unchecked Sendable {
    struct Sample {
        let a: ObjectIdentifier
        let b: ObjectIdentifier
        let aName: String?
        let bName: String?
        let x: Double
        let y: Double
        let z: Double
        let normalY: Double
    }
    private let lock = NSLock()
    private var active: [Set<ObjectIdentifier>: Sample] = [:]

    nonisolated func physicsWorld(_ world: SCNPhysicsWorld, didBegin contact: SCNPhysicsContact) { record(contact) }
    nonisolated func physicsWorld(_ world: SCNPhysicsWorld, didUpdate contact: SCNPhysicsContact) { record(contact) }
    nonisolated func physicsWorld(_ world: SCNPhysicsWorld, didEnd contact: SCNPhysicsContact) {
        let key: Set<ObjectIdentifier> = [ObjectIdentifier(contact.nodeA), ObjectIdentifier(contact.nodeB)]
        lock.lock(); active.removeValue(forKey: key); lock.unlock()
    }
    private nonisolated func record(_ contact: SCNPhysicsContact) {
        let a = ObjectIdentifier(contact.nodeA), b = ObjectIdentifier(contact.nodeB)
        let p = contact.contactPoint
        let sample = Sample(a: a,b: b,aName: contact.nodeA.name,bName: contact.nodeB.name,
                            x: Double(p.x),y: Double(p.y),z: Double(p.z),normalY: Double(contact.contactNormal.y))
        lock.lock(); active[[a,b]] = sample; lock.unlock()
    }
    func snapshot() -> [Sample] { lock.lock(); defer { lock.unlock() }; return Array(active.values) }
    func clear() { lock.lock(); active.removeAll(); lock.unlock() }
}

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
    private let playerFacingRoot = SCNNode()
    private(set) var cover = SCNNode()
    private(set) var generation: UInt64 = 0
    private(set) var simulationTime: TimeInterval = 0
    private(set) var supportDwell: TimeInterval = 0
    private(set) var grounded = false
    private(set) var lastSupportCount = 0
    private let contacts = StreetContacts()
    private let objects = SCNNode()
    private var burstDirection: StreetScalar = 0
    private var burstRemaining: TimeInterval = 0
    private let crossingSpeed: StreetScalar = 2
    private let crossingBurst: TimeInterval = 0.65
    private var dashUsed = false
    private var elapsedSinceDrop: TimeInterval = 0
    private var coverageTimer: TimeInterval = 0
    private var previousRenderTime: TimeInterval?
    private var currentDelta: TimeInterval = 0
    private var facingRight = true
    private var lastPlayerPosition: SCNVector3?
    private var playerVelocity = SCNVector3Zero
    private enum CharacterPose: Int { case idle, walkA, walkB, jump, fall, celebrate }
    private var characterMaterial: SCNMaterial?
    private var characterPose: CharacterPose = .idle
    private var characterAnimationTime: TimeInterval = 0
    private var lastCoverPosition: SCNVector3?
    private var lastCoverOrientation: simd_quatf?
    private var outsidePresentation = false
    private var outsideLandingView = false
    private var impactShown = false
    private let landingPulse = SCNNode()
    private let characterScale: StreetScalar = 1.18
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
        scene.background.contents = StreetColor(red: 0.09,green: 0.16,blue: 0.18,alpha: 1)
        scene.physicsWorld.gravity = SCNVector3(0,-9.81,0)
        scene.physicsWorld.timeStep = 1.0/120
        scene.physicsWorld.contactDelegate = contacts
        scene.rootNode.addChildNode(objects)
        camera.name = "street-camera"; camera.camera = SCNCamera(); camera.camera?.usesOrthographicProjection = true; camera.camera?.projectionDirection = .horizontal; camera.camera?.orthographicScale = 4.1; camera.camera?.zNear = 0.05; camera.camera?.zFar = 100
        camera.position = SCNVector3(0,6.8,10.5); camera.look(at: SCNVector3(0,0.7,0)); scene.rootNode.addChildNode(camera)
        let ambient = SCNNode(); ambient.light = SCNLight(); ambient.light?.type = .ambient; ambient.light?.intensity = 460; ambient.light?.color = StreetColor(red: 0.61,green: 0.78,blue: 0.82,alpha: 1); scene.rootNode.addChildNode(ambient)
        let sunlight = SCNNode(); sunlight.light = SCNLight(); sunlight.light?.type = .directional; sunlight.light?.intensity = 1150; sunlight.light?.color = StreetColor(red: 1,green: 0.89,blue: 0.73,alpha: 1); sunlight.light?.castsShadow = true; sunlight.light?.shadowSampleCount = 16; sunlight.light?.shadowRadius = 3; sunlight.eulerAngles = SCNVector3(-0.8,-0.5,0); scene.rootNode.addChildNode(sunlight)
        let fill = SCNNode(); fill.light = SCNLight(); fill.light?.type = .directional; fill.light?.intensity = 220; fill.light?.color = StreetColor(red: 0.50,green: 0.82,blue: 0.84,alpha: 1); fill.eulerAngles = SCNVector3(-0.65,2.25,0); scene.rootNode.addChildNode(fill)
        player.name = "player"; player.addChildNode(playerVisualRoot); playerVisualRoot.addChildNode(playerFacingRoot); playerVisualRoot.position.y = -0.25
        // Enlarge the selected pose cards around their feet pivot. The collision
        // sphere and jump/crossing measurements remain unchanged.
        playerFacingRoot.scale = SCNVector3(characterScale,characterScale,characterScale)
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
        if let url = Bundle.main.url(forResource: "kaprao-sprite",withExtension: "scn"),let model = try? SCNScene(url: url),let root = model.rootNode.childNode(withName: "KapraoSpriteRoot",recursively: true) {
            root.removeFromParentNode(); playerFacingRoot.addChildNode(root)
            // The handoff's six pose cards share the idle plane's size and pivot.
            // Only its material changes; the player node retains its physics body.
            if let atlasURL = Bundle.main.url(forResource: "kaprao-poses",withExtension: "png"),
               let atlas = Self.poseAtlas(at: atlasURL),
               let visual = root.childNode(withName: "KapraoSpriteVisual",recursively: true),
               let material = visual.geometry?.firstMaterial {
                material.diffuse.contents = atlas
                characterMaterial = material
                setCharacterPose(.idle)
            }
        }
        else { playerFacingRoot.addChildNode(spriteNode) }
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
        outsidePresentation = outside
        #if canImport(UIKit)
        updateCameraScale(for: activeView?.bounds.size)
        #else
        camera.camera?.orthographicScale = outside ? 4.9 : 4.1
        #endif
        if outside {
            // A brief oblique view makes the real cover's fall legible on the
            // outer display. The route returns overhead after impact.
            outsideLandingView = phase == .waiting || phase == .dropping
            if outsideLandingView {
                camera.position = SCNVector3(0,8.2,7.6)
                camera.look(at: SCNVector3(0,0.65,0))
            } else {
                camera.position = SCNVector3(0,13,0)
                camera.eulerAngles = SCNVector3(StreetScalar(-Double.pi/2),0,0)
            }
        } else {
            outsideLandingView = false
            camera.position = SCNVector3(0,6.8,10.5)
            camera.look(at: SCNVector3(0,0.7,0))
        }
        // The sprite's plane is vertical in the inner view. After rotating it
        // flat for the overhead view, lift only the visual pivot above the road
        // surface; the player body stays at its real physics position.
        playerVisualRoot.position.y = outside ? 0.10 : -0.25
        // Keep the card upright on the active display even if the physics body
        // acquires a small rotation during a collision. This changes only art.
        playerVisualRoot.simdWorldOrientation = camera.simdWorldOrientation
        SCNTransaction.commit()
    }
    private func material(_ color: StreetColor,metal: Double = 0) -> SCNMaterial {
        let m = SCNMaterial(); m.diffuse.contents = color; m.metalness.contents = metal; m.roughness.contents = 0.72; return m
    }
    private func box(_ name: String,width: Double,height: Double,depth: Double,at p: SCNVector3,color: StreetColor) -> SCNNode {
        let n = SCNNode(geometry: SCNBox(width: width,height: height,length: depth,chamferRadius: 0)); n.name = name; n.position = p; n.geometry?.materials = [material(color)]; objects.addChildNode(n); return n
    }
    /// A workshop asset is visual dressing only. Normalize its authoring scale and
    /// remove embedded physics, lights and cameras so it cannot change the street.
    private func streetProp(_ name: String,width: Double,at p: SCNVector3) -> SCNNode? {
        guard let url = Bundle.main.url(forResource: name,withExtension: "scn"),
              let source = try? SCNScene(url: url,options: nil) else { return nil }
        let art = source.rootNode.clone()
        let (low,high) = art.boundingBox
        let span = max(Double(high.x-low.x),Double(high.y-low.y),Double(high.z-low.z))
        guard span > 0.001 else { return nil }
        let scale = width/span
        art.scale = SCNVector3(StreetScalar(scale),StreetScalar(scale),StreetScalar(scale))
        art.position = SCNVector3(StreetScalar(-Double(low.x+high.x)*0.5*scale),
                                  StreetScalar(-Double(low.y)*scale),
                                  StreetScalar(-Double(low.z+high.z)*0.5*scale))
        art.physicsBody = nil; art.light = nil; art.camera = nil
        art.enumerateChildNodes { node,_ in node.physicsBody = nil; node.light = nil; node.camera = nil }
        let anchor = SCNNode(); anchor.name = "street-prop-\(name)"; anchor.position = p
        anchor.addChildNode(art); objects.addChildNode(anchor)
        return anchor
    }
    /// These workshop files are full street-width groups authored in meters,
    /// so preserve their individual geometry scale and positions.
    private func streetSet(_ name: String,turnAround: Bool = false) -> Bool {
        guard let url = Bundle.main.url(forResource: name,withExtension: "scn"),
              let source = try? SCNScene(url: url,options: nil) else { return false }
        let art = source.rootNode.clone()
        art.name = "street-set-\(name)"
        art.physicsBody = nil; art.light = nil; art.camera = nil
        art.enumerateChildNodes { node,_ in node.physicsBody = nil; node.light = nil; node.camera = nil }
        if turnAround { art.eulerAngles.y = StreetScalar(Double.pi) }
        objects.addChildNode(art)
        return true
    }
    private func lampGlow(at p: SCNVector3) {
        let lamp = SCNNode(); lamp.position = p; lamp.light = SCNLight()
        lamp.light?.type = .omni; lamp.light?.intensity = 180
        lamp.light?.color = StreetColor(red: 1,green: 0.74,blue: 0.53,alpha: 1)
        lamp.light?.attenuationStartDistance = 0.6; lamp.light?.attenuationEndDistance = 4.4
        objects.addChildNode(lamp)
    }
    private func neonMaterial(_ color: StreetColor) -> SCNMaterial {
        let sign = SCNMaterial()
        sign.lightingModel = .constant
        sign.diffuse.contents = color
        sign.emission.contents = color
        sign.isDoubleSided = true
        return sign
    }
    /// Sidewalk lettering also reads from the outer overhead camera. These
    /// signs and their lights do not participate in street physics.
    private func neonSign(_ legend: String,x: Double,z: Double,color: StreetColor) {
        let base = box("neon-sign-\(legend)",width: 0.94,height: 0.045,depth: 0.46,
                       at: SCNVector3(x,0.075,z),color: StreetColor(red: 0.025,green: 0.055,blue: 0.085,alpha: 1))
        base.geometry?.firstMaterial?.metalness.contents = 0.42
        for dz in [-0.205,0.205] {
            let edge = box("neon-edge",width: 0.89,height: 0.008,depth: 0.012,
                           at: SCNVector3(x,0.102,z+dz),color: color)
            edge.geometry?.materials = [neonMaterial(color)]
        }
        let text = SCNText(string: legend,extrusionDepth: 0.002)
        #if canImport(UIKit)
        text.font = UIFont.systemFont(ofSize: 0.34,weight: .bold)
        #else
        text.font = NSFont.systemFont(ofSize: 0.34,weight: .bold)
        #endif
        text.flatness = 0.008
        text.materials = [neonMaterial(color)]
        let letters = SCNNode(geometry: text)
        let (low,high) = letters.boundingBox
        let width = max(0.001,Double(high.x-low.x)), height = max(0.001,Double(high.y-low.y))
        let size = min(0.67/width,0.30/height)
        letters.scale = SCNVector3(StreetScalar(size),StreetScalar(size),StreetScalar(size))
        letters.position = SCNVector3(StreetScalar(-Double(low.x+high.x)*0.5*size),
                                      StreetScalar(-Double(low.y+high.y)*0.5*size),0)
        let face = SCNNode(); face.eulerAngles.x = StreetScalar(-Double.pi/2)
        face.position = SCNVector3(x,0.103,z); face.addChildNode(letters); objects.addChildNode(face)
        let glow = SCNNode(); glow.position = SCNVector3(x,0.35,z); glow.light = SCNLight()
        glow.light?.type = .omni; glow.light?.color = color; glow.light?.intensity = 95
        glow.light?.attenuationStartDistance = 0.12; glow.light?.attenuationEndDistance = 1.35
        objects.addChildNode(glow)
    }
    private func cityBackdrop() {
        // The north side of the miniature street is a shallow city silhouette.
        // It sits beyond the curb, so both the oblique fold view and the outer
        // map gain depth without placing obstacles in Kaprao's route.
        let block = box("city-ground",width: 10.2,height: 0.06,depth: 2.2,
                        at: SCNVector3(0,-0.10,-3.65),
                        color: StreetColor(red: 0.035,green: 0.075,blue: 0.105,alpha: 1))
        block.castsShadow = false
        let towers: [(Double,Double,Double,Double)] = [
            (-4.20,0.66,0.88,-3.47),(-3.12,0.92,1.28,-3.64),
            (-1.90,0.78,0.80,-3.52),(-0.82,0.98,1.43,-3.70),
            (0.38,0.86,1.04,-3.48),(1.48,0.96,1.60,-3.75),
            (2.78,0.94,1.02,-3.52),(4.00,0.78,1.34,-3.64)
        ]
        for (index,tower) in towers.enumerated() {
            let (x,width,height,z) = tower
            let facade = box("city-tower-\(index)",width: width,height: height,depth: 0.60,
                             at: SCNVector3(x,height*0.5-0.08,z),
                             color: StreetColor(red: index.isMultiple(of: 2) ? 0.075 : 0.10,
                                                green: 0.13,blue: index.isMultiple(of: 2) ? 0.19 : 0.22,alpha: 1))
            facade.castsShadow = false
            let roof = box("city-roof",width: width+0.06,height: 0.025,depth: 0.64,
                           at: SCNVector3(x,height-0.05,z),
                           color: StreetColor(red: 0.15,green: 0.24,blue: 0.28,alpha: 1))
            roof.castsShadow = false
            let lightColor = index.isMultiple(of: 2)
                ? StreetColor(red: 0.34,green: 0.85,blue: 0.89,alpha: 1)
                : StreetColor(red: 0.94,green: 0.36,blue: 0.62,alpha: 1)
            for level in 0..<3 where Double(level)*0.29+0.30 < height {
                let window = box("city-window",width: width*0.54,height: 0.055,depth: 0.008,
                                 at: SCNVector3(x,Double(level)*0.29+0.30,z+0.306),color: lightColor)
                window.geometry?.materials = [neonMaterial(lightColor)]
                window.castsShadow = false
            }
            let roofLine = box("city-roof-light",width: width*0.78,height: 0.008,depth: 0.015,
                               at: SCNVector3(x,height-0.032,z+0.12),color: lightColor)
            roofLine.geometry?.materials = [neonMaterial(lightColor)]
            roofLine.castsShadow = false
        }
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
        contacts.clear()
        player.removeFromParentNode()
        for node in objects.childNodes { node.removeFromParentNode() }
        phase = .waiting; coverage = 0; hint = "Guide the cover, then close Duo."
        supportDwell = 0; grounded = false; lastSupportCount = 0; dashUsed = false; burstRemaining = 0; burstDirection = 0; elapsedSinceDrop = 0; coverageTimer = 0; previousRenderTime = nil; currentDelta = 0; lastPlayerPosition = nil; playerVelocity = SCNVector3Zero; lastCoverPosition = nil; lastCoverOrientation = nil; characterAnimationTime = 0; facingRight = true; playerFacingRoot.scale.x = characterScale; impactShown = false; landingPulse.removeAllActions(); setCharacterPose(.idle)
        for i in 0..<16 {
            _ = sector(inner: 1.15,outer: Self.recessVertexRadius,bottom: -0.55,top: -0.14,index: i,name: "rim-\(i)",color: StreetColor(red: 0.38,green: 0.46,blue: 0.45,alpha: 1))
            _ = sector(inner: Self.recessVertexRadius,outer: 6,bottom: -0.55,top: 0,index: i,name: "road-\(i)",color: StreetColor(red: 0.13,green: 0.20,blue: 0.22,alpha: 1))
        }
        // All street markings are visual only. The segmented road and rim above
        // remain the sole physical support under the falling cover and Kaprao.
        let well = SCNNode(geometry: SCNCylinder(radius: Self.openingRadius,height: 0.01))
        well.name = "dark-well-visual"; well.position.y = -1.3
        well.geometry?.materials = [material(StreetColor(red: 0.035,green: 0.085,blue: 0.10,alpha: 1))]
        objects.addChildNode(well)
        let collar = SCNNode(geometry: SCNTorus(ringRadius: Self.recessVertexRadius,pipeRadius: 0.023))
        collar.name = "manhole-collar-visual"; collar.position.y = 0.012
        collar.geometry?.materials = [material(StreetColor(red: 0.71,green: 0.50,blue: 0.35,alpha: 1),metal: 0.65)]
        objects.addChildNode(collar)
        landingPulse.geometry = SCNTorus(ringRadius: Self.recessVertexRadius+0.07,pipeRadius: 0.017)
        landingPulse.geometry?.materials = [neonMaterial(StreetColor(red: 0.47,green: 0.96,blue: 0.89,alpha: 1))]
        landingPulse.position = SCNVector3(0,0.042,0); landingPulse.opacity = 0
        objects.addChildNode(landingPulse)
        for z in [-1.65,1.65] {
            _ = box("edge-line",width: 9.2,height: 0.004,depth: 0.025,at: SCNVector3(0,0.004,z),color: StreetColor(red: 0.74,green: 0.53,blue: 0.35,alpha: 1))
        }
        for x in stride(from: -3.8,through: 3.8,by: 0.75) where abs(x) > 1.7 {
            _ = box("center-dash",width: 0.28,height: 0.004,depth: 0.022,at: SCNVector3(x,0.005,0),color: StreetColor(red: 0.75,green: 0.55,blue: 0.38,alpha: 1))
        }
        for x in [-3.8,-3.3,-2.8,2.8,3.3,3.8] {
            let stripe = box("crosswalk",width: 0.23,height: 0.006,depth: 1.06,at: SCNVector3(x,0.007,0),color: StreetColor(red: 0.87,green: 0.84,blue: 0.72,alpha: 1))
            stripe.geometry?.firstMaterial?.roughness.contents = 0.91
        }
        for x in [-3.5,-2.7,2.7,3.5] { for z in [-0.9,0.9] {
            let bollard = SCNNode(geometry: SCNCylinder(radius: 0.055,height: 0.31))
            bollard.name = "copper-bollard-visual"; bollard.position = SCNVector3(x,0.155,z)
            bollard.geometry?.materials = [material(StreetColor(red: 0.70,green: 0.47,blue: 0.32,alpha: 1),metal: 0.6)]
            objects.addChildNode(bollard)
            _ = box("bollard-cap",width: 0.15,height: 0.05,depth: 0.15,at: SCNVector3(x,0.32,z),color: StreetColor(red: 0.94,green: 0.85,blue: 0.70,alpha: 1))
        } }
        for z in [-1.9,1.9] {
            let curb = box("curb",width: 9.3,height: 0.17,depth: 0.20,at: SCNVector3(0,0.085,z),color: StreetColor(red: 0.66,green: 0.58,blue: 0.45,alpha: 1))
            curb.geometry?.firstMaterial?.roughness.contents = 0.62
            _ = box("sidewalk",width: 9.3,height: 0.08,depth: 0.66,at: SCNVector3(0,-0.01,z < 0 ? -2.3 : 2.3),color: StreetColor(red: 0.68,green: 0.66,blue: 0.56,alpha: 1))
            for x in stride(from: -4.4,through: 4.4,by: 0.55) {
                _ = box("paving-joint",width: 0.008,height: 0.002,depth: 0.62,at: SCNVector3(x,0.031,z < 0 ? -2.3 : 2.3),color: StreetColor(red: 0.44,green: 0.48,blue: 0.44,alpha: 1))
            }
            _ = box("sidewalk-edge",width: 9.3,height: 0.02,depth: 0.024,at: SCNVector3(0,0.04,z < 0 ? -2.62 : 2.62),color: StreetColor(red: 0.35,green: 0.56,blue: 0.53,alpha: 1))
        }
        neonSign("夜市",x: -2.15,z: -2.32,color: StreetColor(red: 1,green: 0.27,blue: 0.59,alpha: 1))
        neonSign("出口",x: 2.15,z: 2.32,color: StreetColor(red: 0.25,green: 0.95,blue: 0.88,alpha: 1))
        cityBackdrop()
        for x in [-4.05,4.05] {
            let strip = box("neon-sidewalk-strip",width: 0.015,height: 0.012,depth: 0.88,
                            at: SCNVector3(x,0.037,-2.31),color: StreetColor(red: 0.40,green: 0.78,blue: 0.86,alpha: 1))
            strip.geometry?.materials = [neonMaterial(StreetColor(red: 0.40,green: 0.78,blue: 0.86,alpha: 1))]
        }
        // Small bundled workshop models give this road its miniature-world
        // character. Their anchors stay outside the player's physics lane.
        if streetSet("planters") { _ = streetSet("planters",turnAround: true) }
        else { for x in [-3.9,3.9] { for z in [-2.35,2.35] {
            let pot = SCNNode(geometry: SCNCylinder(radius: 0.15,height: 0.20)); pot.position = SCNVector3(x,0.14,z)
            pot.geometry?.materials = [material(StreetColor(red: 0.27,green: 0.47,blue: 0.44,alpha: 1))]; objects.addChildNode(pot)
        } } }
        _ = streetSet("workshop_lamps")
        for x in [-3.5,3.5] { lampGlow(at: SCNVector3(x,2.2,-2.1)) }
        let toy = streetProp("goal_toy",width: 0.40,at: SCNVector3(3.35,0.015,0))
        if toy == nil {
            let fallback = SCNNode(geometry: SCNSphere(radius: 0.20)); fallback.name = "goal-toy"; fallback.position = SCNVector3(3.35,0.20,0)
            fallback.geometry?.materials = [material(StreetColor(red: 0.84,green: 0.58,blue: 0.36,alpha: 1))]; objects.addChildNode(fallback)
        }
        let g = SCNCylinder(radius: Self.coverRadius,height: 0.14); g.radialSegmentCount = 64
        let coverMaterial = material(StreetColor(red: 0.24,green: 0.42,blue: 0.43,alpha: 1),metal: 0.68)
        coverMaterial.roughness.contents = 0.48
        cover = SCNNode(geometry: g); cover.name = "cover"; g.materials = [coverMaterial]; cover.position = SCNVector3(0,2.7,0); cover.isHidden = true; objects.addChildNode(cover)
        for radius in [0.58,1.08] {
            let ring = SCNNode(geometry: SCNTorus(ringRadius: radius,pipeRadius: 0.024))
            ring.position.y = 0.081
            ring.geometry?.materials = [material(StreetColor(red: 0.63,green: 0.78,blue: 0.77,alpha: 1),metal: 0.82)]
            cover.addChildNode(ring)
        }
        for x in [-0.36,0,0.36] {
            let line = SCNNode(geometry: SCNBox(width: 0.040,height: 0.009,length: 0.72,chamferRadius: 0.014))
            line.position = SCNVector3(x,0.079,0)
            line.geometry?.materials = [material(StreetColor(red: 0.10,green: 0.25,blue: 0.29,alpha: 1),metal: 0.55)]
            cover.addChildNode(line)
        }
        for (x,z) in [(1.21,0.0),(-1.21,0.0),(0.0,1.21),(0.0,-1.21)] {
            let bolt = SCNNode(geometry: SCNSphere(radius: 0.055))
            bolt.position = SCNVector3(x,0.086,z)
            bolt.geometry?.materials = [material(StreetColor(red: 0.85,green: 0.91,blue: 0.83,alpha: 1),metal: 0.85)]
            cover.addChildNode(bolt)
        }
        player.physicsBody = SCNPhysicsBody(type: .dynamic,shape: SCNPhysicsShape(geometry: SCNSphere(radius: 0.25),options: [.collisionMargin: 0.0])); player.physicsBody?.mass = 1; player.physicsBody?.friction = 0.7; player.physicsBody?.restitution = 0; player.physicsBody?.damping = 0; player.physicsBody?.angularVelocityFactor = SCNVector3Zero; player.physicsBody?.velocityFactor = SCNVector3(1,1,0); player.physicsBody?.categoryBitMask = 1; player.physicsBody?.contactTestBitMask = -1
        objects.addChildNode(player); recoverPlayer()
        if outsidePresentation { setOutsidePresentation(true) }
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
    private func move(direction: StreetScalar) {
        guard phase != .won else { return }
        burstDirection = direction
        burstRemaining = crossingBurst
        facingRight = direction > 0
        playerFacingRoot.scale.x = facingRight ? characterScale : -characterScale
        // Start the physical burst on the swipe itself. The renderer callback
        // continues to regulate speed from measured motion in later frames.
        if !scene.isPaused,let body = player.physicsBody {
            let desiredX = direction*crossingSpeed
            body.applyForce(SCNVector3((desiredX-playerVelocity.x)*StreetScalar(body.mass),0,0),asImpulse: true)
            playerVelocity.x = desiredX
        }
        if grounded { setCharacterPose(characterPose == .walkA ? .walkB : .walkA) }
    }
    func jump() { guard grounded,phase != .won else { return }; player.physicsBody?.applyForce(SCNVector3(0,2.8,0),asImpulse: true); grounded = false }
    func dash() { guard !grounded,!dashUsed,phase != .won else { return }; dashUsed = true; player.physicsBody?.applyForce(SCNVector3(0,min(0,-3.5-playerVelocity.y),0),asImpulse: true) }
    private func recoverPlayer() { player.position = SCNVector3(-3.2,0.255,0); player.physicsBody?.clearAllForces(); player.physicsBody?.velocity = SCNVector3Zero; player.physicsBody?.angularVelocity = SCNVector4(0,0,0,0); player.physicsBody?.resetTransform(); burstRemaining = 0; dashUsed = false; grounded = false; lastPlayerPosition = nil; playerVelocity = SCNVector3Zero }

    // Invoked by the one active SCNView's delegate. SCNView alone advances SceneKit physics.
    func beforePhysics(at time: TimeInterval) {
        currentDelta = scene.isPaused ? 0 : min(1.0/15,max(0,time-(previousRenderTime ?? time))); previousRenderTime = time
        simulationTime += currentDelta
        burstRemaining = max(0,burstRemaining-currentDelta)
        guard currentDelta > 0 else { return }
        let desiredX: StreetScalar = burstRemaining > 0 ? burstDirection*crossingSpeed : 0
        // SceneKit reports zero for body.velocity in its macOS renderer even while
        // the presentation node is moving. Use measured displacement to avoid
        // stacking an impulse every frame and launching Kaprao off the street.
        if let body = player.physicsBody {
            body.applyForce(SCNVector3((desiredX-playerVelocity.x)*StreetScalar(body.mass),0,0),asImpulse: true)
        }
    }
    func afterPhysics() {
        guard !scene.isPaused else { return }
        let pp = player.presentation.worldPosition
        playerVisualRoot.simdWorldOrientation = camera.simdWorldOrientation
        if let last = lastPlayerPosition,currentDelta > 0 { let dt = StreetScalar(currentDelta); playerVelocity = SCNVector3((pp.x-last.x)/dt,(pp.y-last.y)/dt,(pp.z-last.z)/dt) }; lastPlayerPosition = pp
        let pv = playerVelocity
        let playerID = ObjectIdentifier(player)
        grounded = pv.y < 0.4 && contacts.snapshot().contains {
            ($0.a == playerID || $0.b == playerID) && abs($0.normalY)>0.7 && $0.y < Double(pp.y)-0.10
        }
        if grounded { dashUsed = false }
        if pp.y < -2 || abs(pp.x)>4.5 { recoverPlayer(); if phase == .safe { hint = "Try again: swipe right to reach the toy." } }
        if phase == .dropping || phase == .safe { checkCover() }
        if phase == .safe,pp.x > 3.10,grounded { phase = .won; hint = "Street repaired! Kaprao found the toy."; burstRemaining = 0 }
        if outsidePresentation && outsideLandingView && elapsedSinceDrop >= 1.35 {
            outsideLandingView = false
            SCNTransaction.begin(); SCNTransaction.animationDuration = 0.55
            camera.position = SCNVector3(0,13,0)
            camera.eulerAngles = SCNVector3(StreetScalar(-Double.pi/2),0,0)
            SCNTransaction.commit()
        }
        updateCharacterPose()
    }
    private func setCharacterPose(_ pose: CharacterPose) {
        guard let material = characterMaterial else { return }
        guard pose != characterPose || material.diffuse.contentsTransform.m11 != 1.0/3.0 else { return }
        characterPose = pose
        let column = pose.rawValue % 3, row = pose.rawValue / 3
        var transform = SCNMatrix4Identity
        transform.m11 = 1.0/3.0; transform.m22 = 1.0/2.0
        transform.m41 = StreetScalar(column)/3.0; transform.m42 = StreetScalar(row)/2.0
        material.diffuse.contentsTransform = transform
    }
    private static func poseAtlas(at url: URL) -> Any? {
        #if canImport(UIKit)
        return UIImage(contentsOfFile: url.path)
        #else
        return NSImage(contentsOfFile: url.path)
        #endif
    }
    private func updateCharacterPose() {
        characterAnimationTime += currentDelta
        let pose: CharacterPose
        if phase == .won { pose = .celebrate }
        else if !grounded && playerVelocity.y > 0.25 { pose = .jump }
        else if !grounded && playerVelocity.y < -0.25 { pose = .fall }
        else if grounded && (abs(playerVelocity.x) > 0.25 || burstRemaining > 0) {
            pose = Int(characterAnimationTime * 6) % 2 == 0 ? .walkA : .walkB
        } else { pose = .idle }
        setCharacterPose(pose)
    }
    private func checkCover() {
        guard cover.physicsBody != nil else { return }
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
        let coverID = ObjectIdentifier(cover)
        var ids = Set<String>(),points: [CGPoint] = []
        for contact in contacts.snapshot() {
            let name = contact.a == coverID ? contact.bName : contact.b == coverID ? contact.aName : nil
            guard let name,name.hasPrefix("rim-"),abs(contact.normalY)>0.7,contact.y < Double(p.y)+0.01,abs(contact.y+0.14)<0.04 else { continue }
            if ids.insert(name).inserted { points.append(CGPoint(x: contact.x,y: contact.z)) }
        }
        lastSupportCount = ids.count
        if !impactShown && !ids.isEmpty && p.y < 0.10 {
            impactShown = true
            landingPulse.opacity = 0.8
            landingPulse.runAction(.fadeOut(duration: 0.65))
        }
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
    private func updateCameraScale(for size: CGSize?) {
        guard outsidePresentation else { camera.camera?.orthographicScale = 4.1; return }
        guard let size,size.width > 1,size.height > 1 else {
            camera.camera?.orthographicScale = 4.9
            return
        }
        // Projection is horizontal: fit the 9.3 m street and also preserve
        // its 5.3 m height when the outer display becomes especially wide.
        let aspect = Double(size.width/size.height)
        camera.camera?.orthographicScale = max(4.9,2.8*aspect)
    }
    fileprivate func attach(_ view: SCNView) {
        if let old = activeView,old !== view { old.isPlaying = false; old.delegate = nil; old.scene = nil }
        clockToken += 1; previousRenderTime = nil; rendererReady = false
        let delegate = StreetClock(world: self,token: clockToken); clock = delegate; activeView = view
        view.scene = scene; view.pointOfView = camera; view.delegate = delegate; view.isPlaying = true
        updateCameraScale(for: view.bounds.size)
    }
    fileprivate func resize(_ view: SCNView) {
        guard activeView === view,view.bounds.width > 1,view.bounds.height > 1 else { return }
        updateCameraScale(for: view.bounds.size)
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
// The renderer callback reads only immutable fields and protects its pending flag
// with a lock; all world access is dispatched to the main actor.
private final class StreetClock: NSObject, SCNSceneRendererDelegate, @unchecked Sendable {
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
