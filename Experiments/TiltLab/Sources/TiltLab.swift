import SwiftUI
import SpriteKit
import CoreMotion

// Feasibility prototype only. Keep separate from the submitted game's session.
final class TiltInput: ObservableObject {
    enum Mode: String, CaseIterable { case manual = "Manual tilt", device = "Device motion" }
    let manager = CMMotionManager()
    @Published var mode: Mode = .manual
    @Published var status = "Manual input — not sensor data"
    @Published var tilt = CGVector.zero
    private var neutral = CGVector.zero
    var available: Bool { manager.isDeviceMotionAvailable }
    init() {
        if available { mode = .device; start() }
        print("TILT_CAPABILITY motion=\(available) accelerometer=\(manager.isAccelerometerAvailable)")
    }
    func start() {
        guard mode == .device, available else { return }
        manager.deviceMotionUpdateInterval = 1.0 / 60
        manager.startDeviceMotionUpdates()
    }
    func stop() { manager.stopDeviceMotionUpdates(); tilt = .zero }
    func calibrate() {
        guard let g = manager.deviceMotion?.gravity else { return }
        neutral = CGVector(dx: g.x, dy: g.y)
    }
    func sample() -> CGVector? {
        guard mode == .device else { return tilt }
        guard available else { return nil }
        guard let data = manager.deviceMotion,
              ProcessInfo.processInfo.systemUptime - data.timestamp < 0.35 else { return nil }
        // Portrait: device +x points right; +y points up. SpriteKit uses the same axes.
        return CGVector(dx: max(-0.6, min(0.6, data.gravity.x - neutral.dx)),
                        dy: max(-0.6, min(0.6, data.gravity.y - neutral.dy)))
    }
    func switchMode() { stop(); if mode == .device { start() } }
}

final class TiltBoard: SKScene, ObservableObject {
    @Published var telemetry = "Tilt to move the cover around both barriers."
    @Published var parked = false
    var input: TiltInput!
    private let disk = SKShapeNode(circleOfRadius: 17)
    let target = CGPoint(x: 420, y: 55)
    private var previous: TimeInterval?
    private var dwell: TimeInterval = 0
    private var lastReport: TimeInterval = 0
    private var configured = false
    private var validInput = false
    private var contacts = 0
    var diskPosition: CGPoint { disk.position }
    var sampleOverride: (() -> CGVector?)?
    private let smoke = ProcessInfo.processInfo.arguments.contains("--tilt-smoke")
    private var smokeStart: TimeInterval?
    private var smokePhase = 0
    private var smokePassed = false
    private var smokeBlockPass = false
    private let route = [CGPoint(x:410,y:300),CGPoint(x:410,y:180),CGPoint(x:60,y:180),CGPoint(x:60,y:55),CGPoint(x:420,y:55)]
    override init(size: CGSize) { super.init(size:size); scaleMode = .aspectFit; backgroundColor = UIColor(red:0.045,green:0.09,blue:0.13,alpha:1) }
    required init?(coder: NSCoder) { fatalError("init(coder:) has not been implemented") }
    override func didMove(to view: SKView) {
        guard !configured else { return }; configured = true
        let border = SKShapeNode(rect: CGRect(x: 5,y: 5,width: 470,height: 350),cornerRadius: 8)
        border.strokeColor = .cyan; border.lineWidth = 4
        border.physicsBody = SKPhysicsBody(edgeLoopFrom: CGRect(x:5,y:5,width:470,height:350))
        border.physicsBody?.friction = 0.2; addChild(border)
        for rect in [CGRect(x:5,y:232,width:330,height:20),CGRect(x:145,y:112,width:330,height:20)] {
            let barrier = SKShapeNode(rectOf:rect.size,cornerRadius:8)
            barrier.position = CGPoint(x:rect.midX,y:rect.midY)
            barrier.fillColor = .systemTeal; barrier.strokeColor = .cyan
            barrier.physicsBody = SKPhysicsBody(rectangleOf:rect.size); barrier.physicsBody?.isDynamic = false
            barrier.physicsBody?.restitution = 0.1; barrier.physicsBody?.friction = 0.2
            addChild(barrier)
        }
        let goal = SKShapeNode(circleOfRadius: 37); goal.position = target
        goal.strokeColor = .systemYellow; goal.lineWidth = 3; addChild(goal)
        let label = SKLabelNode(text:"PARK"); label.fontSize = 12; label.position = target.applying(CGAffineTransform(translationX:0,y:-4)); addChild(label)
        let start = SKLabelNode(text:"START →"); start.fontSize = 13; start.position = CGPoint(x:92,y:335); addChild(start)
        disk.fillColor = .lightGray; disk.strokeColor = .white; disk.lineWidth = 3
        disk.physicsBody = SKPhysicsBody(circleOfRadius:17)
        disk.physicsBody?.allowsRotation = false; disk.physicsBody?.restitution = 0.1
        disk.physicsBody?.friction = 0.25; disk.physicsBody?.linearDamping = 0.7
        disk.physicsBody?.usesPreciseCollisionDetection = true
        addChild(disk); reset()
    }
    func reset() {
        disk.position = CGPoint(x:60,y:300); disk.physicsBody?.velocity = .zero
        disk.physicsBody?.angularVelocity = 0
        dwell = 0; previous = nil; parked = false; contacts = 0
        telemetry = "Tilt right, down, left, down, right. Counter-tilt to brake."
    }
    func suspend(_ paused: Bool) {
        isPaused = paused; previous = nil; dwell = 0; parked = false
        if paused { input.stop() } else { input.start() }
    }
    override func update(_ currentTime: TimeInterval) {
        let dt = min(1.0/30,max(0,currentTime - (previous ?? currentTime))); previous = currentTime
        if smoke && !smokePassed {
            smokeStart = smokeStart ?? currentTime
            if currentTime - smokeStart! < 2 {
                input.tilt = CGVector(dx:0,dy:-0.6)
            } else {
                if !smokeBlockPass {
                    smokeBlockPass = disk.position.y >= 267 && disk.position.y < 280
                    print("TILT_BARRIER_PASS \(smokeBlockPass) x=\(disk.position.x) y=\(disk.position.y)")
                    guard smokeBlockPass else { fatalError("Cover crossed the blocking rail") }
                }
                let destination = route[min(smokePhase,route.count-1)]
                let v = disk.physicsBody?.velocity ?? .zero
                input.tilt = CGVector(dx:max(-0.6,min(0.6,(destination.x-disk.position.x)*0.015-v.dx*0.025)),dy:max(-0.6,min(0.6,(destination.y-disk.position.y)*0.015-v.dy*0.025)))
                if hypot(destination.x-disk.position.x,destination.y-disk.position.y)<8 && hypot(v.dx,v.dy)<12 && smokePhase<route.count-1 {
                    smokePhase += 1; print("TILT_WAYPOINT \(smokePhase)")
                }
            }
        }
        let sample = sampleOverride.map { $0() } ?? input.sample(); validInput = sample != nil
        // No fabricated readings: unavailable/stale device motion freezes physics.
        physicsWorld.speed = validInput ? 1 : 0
        let g = sample ?? .zero
        physicsWorld.gravity = CGVector(dx:g.dx * 7,dy:g.dy * 7)
        if !validInput { dwell = 0; parked = false }
        if currentTime - lastReport > 0.2 {
            lastReport = currentTime
            let v = disk.physicsBody?.velocity ?? .zero
            let speed = hypot(v.dx,v.dy)
            telemetry = (smoke ? "SCRIPTED TEST · " : "") + String(format:"x %.0f · y %.0f · speed %.1f pt/s · steady %.1f/0.6s",disk.position.x,disk.position.y,speed,dwell)
            input.status = input.mode == .manual ? "MANUAL — simulated tilt, not accelerometer" : (validInput ? "LIVE — Core Motion gravity" : "NO SENSOR SAMPLE — physics paused")
        }
        // Dwell is evaluated after the physics step, with elapsed simulation time only.
        userData = userData ?? NSMutableDictionary(); userData?["dt"] = dt
    }
    override func didSimulatePhysics() {
        let v = disk.physicsBody?.velocity ?? .zero
        let inside = hypot(disk.position.x-target.x,disk.position.y-target.y) <= 20
        let dt = userData?["dt"] as? Double ?? 0
        if validInput && inside && hypot(v.dx,v.dy) < 8 { dwell += dt } else { dwell = 0 }
        let nowParked = dwell >= 0.6
        if nowParked != parked {
            parked = nowParked
            print("TILT_PARKED \(parked) position=\(disk.position) speed=\(hypot(v.dx,v.dy))")
        }
        if smoke && parked && !smokePassed {
            smokePassed = true; input.tilt = .zero
            let report: [String:Any] = ["barrierBlocked":smokeBlockPass,"waypoints":smokePhase+1,"parked":true,"position":[disk.position.x,disk.position.y],"speed":hypot(v.dx,v.dy),"dwell":dwell,"source":"scripted gravity only, not sensor data","sensorAvailable":input.available]
            let url = FileManager.default.urls(for:.documentDirectory,in:.userDomainMask)[0].appendingPathComponent("tilt-smoke.json")
            try? JSONSerialization.data(withJSONObject:report,options:.prettyPrinted).write(to:url)
            print("TILT_SMOKE_PASS \(url.path)")
        }
        // No snap, magnet, automatic brake or location changes at success.
    }
}

struct TiltLabView: View {
    @StateObject private var input: TiltInput
    @StateObject private var board: TiltBoard
    @Environment(\.scenePhase) private var phase
    @State private var hinge: Double?
    init() {
        let input = TiltInput(); let board = TiltBoard(size:CGSize(width:480,height:360)); board.input = input
        _input = StateObject(wrappedValue:input); _board = StateObject(wrappedValue:board)
    }
    var body: some View {
        GeometryReader { geo in
            let division = geo.reservedRegions(kind:.division,options:.includeInactive)
                .first(where: { $0.frame.width > geo.size.width * 0.6 && $0.frame.midY > 50 && $0.frame.midY < geo.size.height - 50 })?.frame
            let upperHeight = division?.minY ?? geo.size.height * 0.52
            let lowerY = division?.maxY ?? upperHeight + 2
            ZStack(alignment:.top) {
                Color(red:0.045,green:0.07,blue:0.1).ignoresSafeArea()
                VStack(spacing:6) {
                    Text("COVER RUN · TILT PROBE").font(.headline)
                    SpriteView(scene:board).frame(maxWidth:.infinity,maxHeight:.infinity)
                    Text(board.parked ? "Parked ✓ · fold/drop is the next experiment" : "Reach PARK and stay under 8 pt/s for 0.6 seconds")
                        .font(.caption).foregroundStyle(board.parked ? .green : .white)
                }.padding(12).frame(height:max(80,upperHeight))
                Rectangle().fill(.cyan.opacity(0.5)).frame(height:2).offset(y:upperHeight)
                controls.frame(height:max(100,geo.size.height-lowerY)).offset(y:lowerY)
            }
        }
        .onHingeChange { _, context in hinge = context.hinge?.angle.degrees }
        .onChange(of:input.mode) { _,_ in input.switchMode() }
        .onChange(of:phase) { _,new in board.suspend(new != .active) }
        .preferredColorScheme(.dark)
    }
    private var controls: some View {
        VStack(spacing:10) {
            Text(input.status).font(.caption.bold()).foregroundStyle(.cyan)
            Picker("Input",selection:$input.mode) {
                Text("Manual tilt").tag(TiltInput.Mode.manual)
                Text("Device motion").tag(TiltInput.Mode.device)
            }.pickerStyle(.segmented)
            if input.mode == .manual {
                GeometryReader { g in
                    ZStack {
                        RoundedRectangle(cornerRadius:14).fill(.white.opacity(0.06))
                        Path { p in p.move(to:CGPoint(x:g.size.width/2,y:0));p.addLine(to:CGPoint(x:g.size.width/2,y:g.size.height));p.move(to:CGPoint(x:0,y:g.size.height/2));p.addLine(to:CGPoint(x:g.size.width,y:g.size.height/2)) }.stroke(.white.opacity(0.2))
                        Text("Drag to tilt · release to level").font(.caption).offset(y:-g.size.height*0.35)
                        Circle().fill(.cyan).frame(width:20,height:20).offset(x:input.tilt.dx/0.6*g.size.width/2,y:-input.tilt.dy/0.6*g.size.height/2)
                    }.contentShape(Rectangle()).gesture(DragGesture(minimumDistance:0).onChanged { value in
                        input.tilt = CGVector(dx:max(-0.6,min(0.6,(value.location.x/g.size.width*2-1)*0.6)),dy:max(-0.6,min(0.6,(1-value.location.y/g.size.height*2)*0.6)))
                    }.onEnded { _ in input.tilt = .zero })
                }.frame(maxHeight:100)
                HStack { Text("X"); Slider(value:Binding(get:{input.tilt.dx},set:{input.tilt.dx=$0}),in:-0.6...0.6).accessibilityLabel("Horizontal test tilt") }
                HStack { Text("Y"); Slider(value:Binding(get:{input.tilt.dy},set:{input.tilt.dy=$0}),in:-0.6...0.6).accessibilityLabel("Vertical test tilt") }
                Button("Level manual tilt") { input.tilt = .zero }
            } else {
                Text(input.available ? "Hold in portrait. Calibrate at a comfortable neutral angle, then gently tilt." : "No device motion available. Connect a physical iPhone or use Manual tilt.").font(.callout)
            }
            HStack {
                Button("Reset cover") { board.reset() }.buttonStyle(.borderedProminent)
                Button("Calibrate") { input.calibrate() }.buttonStyle(.bordered).disabled(input.mode != .device || !input.available)
            }
            Text(board.telemetry).font(.system(size:11,design:.monospaced))
            Text(hinge.map { String(format:"Live hinge %.1f° · independently observed",$0) } ?? "Hinge unavailable · not substituted with tilt").font(.caption2)
        }.padding(16)
    }
}

@main struct TiltLabApp: App {
    var body: some Scene { WindowGroup { TiltLabView() } }
}
