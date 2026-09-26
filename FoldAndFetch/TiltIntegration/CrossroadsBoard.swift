import SpriteKit
import Combine

/// The board owns the cover until the steady target hold captures it for transfer.
final class CrossroadsBoard: SKScene, ObservableObject {
    @Published var hint = "Tilt right, then weave around the barriers."
    @Published var held = false {
        didSet { if held { disk.physicsBody?.isDynamic = false; physicsWorld.speed = 0 } }
    }
    var sampleProvider: (() -> CGVector?)?
    var onPark: ((CGPoint) -> Void)?
    private let disk = SKShapeNode(circleOfRadius:17)
    private let target = CGPoint(x:420,y:55)
    private var configured = false
    private var previous:TimeInterval?
    private var delta:TimeInterval = 0
    private var dwell = ParkDwell()
    private var fresh = false
    private var notified = false
    private var lastReport:TimeInterval = 0

    override init(size:CGSize) {
        super.init(size:size); scaleMode = .aspectFit
        backgroundColor = UIColor(red:0.035,green:0.075,blue:0.12,alpha:1)
    }
    required init?(coder:NSCoder) { fatalError("init(coder:) unavailable") }
    override func didMove(to view:SKView) {
        guard !configured else { return }; configured = true
        let cyan = UIColor(red:0.2,green:0.93,blue:0.82,alpha:1)
        for x in stride(from: CGFloat(25),through:475,by:25) {
            let path = CGMutablePath(); path.move(to:CGPoint(x:x,y:5)); path.addLine(to:CGPoint(x:x,y:355))
            let line = SKShapeNode(path:path); line.strokeColor = cyan.withAlphaComponent(0.06); addChild(line)
        }
        for y in stride(from: CGFloat(5),through:355,by:25) {
            let path = CGMutablePath(); path.move(to:CGPoint(x:5,y:y)); path.addLine(to:CGPoint(x:475,y:y))
            let line = SKShapeNode(path:path); line.strokeColor = cyan.withAlphaComponent(0.06); addChild(line)
        }
        let border = SKShapeNode(rect:CGRect(x:5,y:5,width:470,height:350),cornerRadius:9)
        border.strokeColor = cyan; border.lineWidth = 3
        border.physicsBody = SKPhysicsBody(edgeLoopFrom:CGRect(x:5,y:5,width:470,height:350))
        border.physicsBody?.friction = 0.2; addChild(border)
        for rect in [CGRect(x:5,y:232,width:330,height:20),CGRect(x:145,y:112,width:330,height:20)] {
            let barrier = SKShapeNode(rectOf:rect.size,cornerRadius:6)
            barrier.position = CGPoint(x:rect.midX,y:rect.midY)
            barrier.fillColor = UIColor(red:0.1,green:0.28,blue:0.33,alpha:1); barrier.strokeColor = cyan
            barrier.lineWidth = 2
            barrier.physicsBody = SKPhysicsBody(rectangleOf:rect.size)
            barrier.physicsBody?.isDynamic = false; barrier.physicsBody?.friction = 0.2; barrier.physicsBody?.restitution = 0.1
            addChild(barrier)
            let sign = SKLabelNode(text:"工事中  •  CROSSROADS"); sign.fontName = "Menlo-Bold"; sign.fontSize = 9
            sign.fontColor = cyan; sign.position = CGPoint(x:rect.midX,y:rect.midY-3); addChild(sign)
        }
        let goal = SKShapeNode(circleOfRadius:37); goal.position = target; goal.strokeColor = .systemYellow; goal.lineWidth = 3; addChild(goal)
        let cross = SKLabelNode(text:"＋"); cross.position = CGPoint(x:target.x,y:target.y-8); cross.fontSize = 25; cross.fontColor = .systemYellow; addChild(cross)
        let label = SKLabelNode(text:"HOLD HERE"); label.fontName = "Menlo-Bold"; label.fontSize = 9; label.position = CGPoint(x:target.x,y:13); label.fontColor = .systemYellow; addChild(label)
        let start = SKLabelNode(text:"START →"); start.fontName = "Menlo-Bold"; start.fontSize = 10; start.position = CGPoint(x:80,y:330); start.fontColor = cyan; addChild(start)
        disk.fillColor = UIColor(red:0.55,green:0.62,blue:0.7,alpha:1); disk.strokeColor = .white; disk.lineWidth = 2
        let ring = SKShapeNode(circleOfRadius:12); ring.strokeColor = .darkGray; ring.lineWidth = 2; disk.addChild(ring)
        for x in [-6.0,0,6] {
            let rib = SKShapeNode(rectOf:CGSize(width:2,height:15),cornerRadius:1); rib.position.x = x; rib.fillColor = .darkGray; rib.strokeColor = .clear; disk.addChild(rib)
        }
        disk.physicsBody = SKPhysicsBody(circleOfRadius:17)
        disk.physicsBody?.allowsRotation = false; disk.physicsBody?.restitution = 0.1
        disk.physicsBody?.friction = 0.25; disk.physicsBody?.linearDamping = 0.7; disk.physicsBody?.usesPreciseCollisionDetection = true
        disk.zPosition = 2; addChild(disk); reset()
    }
    func reset() {
        disk.childNode(withName:"hold-ring")?.removeFromParent()
        held = false; notified = false; dwell = ParkDwell(); previous = nil
        disk.physicsBody?.isDynamic = true; disk.physicsBody?.velocity = .zero; disk.physicsBody?.angularVelocity = 0
        disk.position = CGPoint(x:60,y:300); hint = "Tilt right, down, left, down, then right."
    }
    override func update(_ time:TimeInterval) {
        delta = min(1.0/30,max(0,time-(previous ?? time))); previous = time
        guard !held else { physicsWorld.speed = 0; return }
        let sample = sampleProvider?(); fresh = sample != nil
        physicsWorld.speed = fresh ? 1 : 0
        let g = sample ?? .zero; physicsWorld.gravity = CGVector(dx:g.dx*7,dy:g.dy*7)
        if time-lastReport > 0.25 {
            lastReport = time
            let speed = hypot(disk.physicsBody?.velocity.dx ?? 0,disk.physicsBody?.velocity.dy ?? 0)
            let text = !fresh ? "Motion paused · connect your iPad or choose Manual" : dwell.elapsed > 0 ? "Hold steady…" : speed > 110 ? "Counter-tilt gently to brake" : "Guide the cover to the yellow target"
            if hint != text { hint = text }
        }
    }
    override func didSimulatePhysics() {
        guard !held, !notified else { return }
        let velocity = disk.physicsBody?.velocity ?? .zero
        if dwell.step(distance:hypot(disk.position.x-target.x,disk.position.y-target.y),speed:hypot(velocity.dx,velocity.dy),delta:delta,fresh:fresh) {
            notified = true
            let offset = CGPoint(x:(disk.position.x-target.x)/20,y:(disk.position.y-target.y)/20)
            // A visible hold is applied only after real travel and the target dwell.
            held = true; hint = "Placement held · close Duo to drop"
            let clamp = SKShapeNode(circleOfRadius:21); clamp.name = "hold-ring"; clamp.strokeColor = .systemYellow; clamp.lineWidth = 3; disk.addChild(clamp)
            onPark?(offset)
        }
    }
}
