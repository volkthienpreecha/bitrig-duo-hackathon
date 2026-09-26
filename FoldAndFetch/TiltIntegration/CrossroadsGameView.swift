import SwiftUI
import SpriteKit
import SceneKit

struct CrossroadsGameView: View {
    @StateObject private var board = CrossroadsBoard(size: CGSize(width:480,height:360))
    @StateObject private var street = TiltStreetWorld()
    @StateObject private var motion = MotionInputClient()
    @StateObject private var audio = CrossroadsAudio()
    @Environment(\.scenePhase) private var lifecycle
    @State private var flow = CrossroadsFlow()
    @State private var hingeClosed = false
    @State private var hingeKnown = false
    @State private var sawDivision = false
    @State private var outerStable = false
    @State private var transitionTask: Task<Void,Never>?
    @State private var settings = false
    @State private var showLevelRoute = false
    @State private var showMainMenu = true
    @State private var manual = false
    @State private var manualTilt = CGVector.zero
    @State private var neutral = CGVector.zero
    @AppStorage("motionBridgeHost") private var host = "127.0.0.1"
    @State private var token = ""
    private let ink = Color(red:0.025,green:0.055,blue:0.09)
    private let mint = Color(red:0.26,green:0.96,blue:0.79)
    private let amber = Color(red:1,green:0.73,blue:0.24)
    private let cream = Color(red:0.96,green:0.93,blue:0.85)

    var body: some View {
        GeometryReader { geometry in
            let regions = geometry.reservedRegions(kind:.division,options:.includeInactive,layoutDirectionBehavior:.fixed)
            let activeDivision = regions.contains { $0.isActive }
            let divider = regions.filter { $0.isActive || !hingeClosed }
                .map(\.frame).first { $0.width > geometry.size.width * 0.5 && $0.height < geometry.size.height * 0.2 && $0.midY > 40 && $0.midY < geometry.size.height-40 }
            let upperHeight = divider?.minY ?? geometry.size.height * 0.50
            let lowerY = divider?.maxY ?? upperHeight
            let key = "\(geometry.size)-\(String(describing:divider))-\(activeDivision)-\(hingeClosed)-\(hingeKnown)-\(lifecycle == .active)"
            ZStack(alignment:.top) {
                LinearGradient(colors:[ink,Color(red:0.045,green:0.13,blue:0.17),ink],startPoint:.topLeading,endPoint:.bottomTrailing)
                    .ignoresSafeArea()
                if flow.display == .outside {
                    outsideStreetPanel(size:geometry.size)
                        .frame(width:geometry.size.width,height:geometry.size.height)
                        .overlay { if showMainMenu { mainMenuPanel(compact:true) } }
                } else {
                    Group {
                        if showMainMenu { mainMenuPanel(compact:false) }
                        else { insideBoardPanel }
                    }
                    .frame(width:geometry.size.width,height:max(100,upperHeight))
                    insideStreetPanel
                        .frame(width:geometry.size.width,height:max(100,geometry.size.height-lowerY))
                        .offset(y:lowerY)
                }
            }
            .onChange(of:key,initial:true) { _,_ in updateLayout(size:geometry.size,divider:divider,activeDivision:activeDivision) }
        }
        .ignoresSafeArea(.container,edges:.all)
        .statusBarHidden()
        .persistentSystemOverlays(.hidden)
        .onHingeChange { _,context in
            if let hinge = context.hinge {
                hingeKnown = true; hingeClosed = hinge.status == .closed
                NSLog("[CrossroadsHinge] angle=%.3f closed=%@",hinge.angle.radians,String(hingeClosed))
            }
        }
        .sheet(isPresented:$settings) { inputSettings }
        .onChange(of:settings) { _,_ in manualTilt = .zero; configureInput(); updatePause(); attemptDrop() }
        .onChange(of:street.phase) { _,phase in
            switch phase {
            case .dropping: audio.play("mechanism_release")
            case .safe: audio.play("bridge_land")
            case .won: audio.play("success"); showLevelRoute = true
            default: break
            }
        }
        .onChange(of:street.rendererReady) { _,_ in attemptDrop() }
        .onChange(of:lifecycle) { _,value in
            if value == .active { connect() } else { motion.stop(); audio.stopAll(); manualTilt = .zero }
            configureInput()
            updatePause()
        }
        .onAppear {
            board.onPark = { offset in
                flow.park(offset:offset)
            }
            connect(); configureInput()
        }
        .preferredColorScheme(.dark)
    }

    private var insideBoardPanel: some View {
        SpriteView(scene:board)
            .onAppear { board.scaleMode = .fill }
            .frame(maxWidth:.infinity,maxHeight:.infinity)
            .overlay(alignment:.top) { titleBar(outside:false) }
            .overlay(alignment:.bottomLeading) {
                Text(board.held ? "Close Duo to drop the cover" : board.hint)
                    .font(.system(size:12,weight:.semibold,design:.rounded))
                    .foregroundStyle(board.held ? amber : .white)
                    .lineLimit(2)
                    .padding(.horizontal,12).padding(.vertical,8)
                    .background(ink.opacity(0.8),in:Capsule())
                    .padding(10)
                    .allowsHitTesting(false)
            }
            .overlay(alignment:.bottom) {
                if manual && !board.held {
                    tiltPad.frame(width:260,height:80)
                        .padding(.bottom,44)
                }
            }
    }

    private func mainMenuPanel(compact:Bool) -> some View {
        GeometryReader { proxy in
            ZStack(alignment:.bottomLeading) {
                ink
                citySilhouette
                    .frame(height:proxy.size.height * 0.58)
                    .opacity(0.38)
                if let path = Bundle.main.path(forResource:"kaprao-idle",ofType:"png"),
                   let image = UIImage(contentsOfFile:path) {
                    Image(uiImage:image)
                        .resizable()
                        .scaledToFit()
                        .frame(width:min(245,proxy.size.width * 0.39))
                        .position(x:proxy.size.width * 0.77,y:proxy.size.height * 0.47)
                        .accessibilityHidden(true)
                }
                VStack(alignment:.leading,spacing:0) {
                    HStack {
                        Text("NIGHT MARKET  •  LEVEL 01")
                            .font(.system(size:11,weight:.bold,design:.rounded))
                            .tracking(1.1)
                            .foregroundStyle(amber)
                        Spacer()
                        Button { settings = true } label: {
                            Image(systemName:"antenna.radiowaves.left.and.right")
                                .frame(width:44,height:44)
                        }
                        .buttonStyle(.plain)
                        .accessibilityLabel("Motion connection settings")
                    }
                    Spacer(minLength:6)
                    Text("Corgi\nCrossroads")
                        .font(.system(size:compact ? 34 : 42,weight:.heavy,design:.rounded))
                        .tracking(-1.8)
                        .lineSpacing(-5)
                        .foregroundStyle(cream)
                        .fixedSize(horizontal:false,vertical:true)
                    Text("One small dog. One big crossing.")
                        .font(.system(size:14,weight:.medium,design:.rounded))
                        .foregroundStyle(cream.opacity(0.78))
                        .padding(.top,8)
                    HStack(spacing:8) {
                        Image(systemName:"pawprint.fill")
                            .font(.system(size:12))
                            .foregroundStyle(amber)
                        Text("01")
                            .font(.system(size:14,weight:.bold,design:.rounded))
                            .foregroundStyle(amber)
                        Rectangle().fill(amber.opacity(0.5)).frame(width:24,height:1)
                        Text("09 CROSSINGS")
                            .font(.system(size:11,weight:.bold,design:.rounded))
                            .tracking(1)
                            .foregroundStyle(cream.opacity(0.65))
                    }
                    .padding(.top,18)
                    Button {
                        showMainMenu = false
                        showLevelRoute = false
                        board.reset()
                        street.reset()
                        flow.reset()
                        configureInput()
                        updatePause()
                    } label: {
                        HStack {
                            Text("Start crossing")
                            Spacer()
                            Image(systemName:"arrow.right")
                        }
                        .font(.system(size:16,weight:.bold,design:.rounded))
                        .foregroundStyle(ink)
                        .padding(.horizontal,18)
                        .frame(height:52)
                        .background(amber,in:RoundedRectangle(cornerRadius:10))
                    }
                    .buttonStyle(.plain)
                    .padding(.top,18)
                    .accessibilityHint("Begin level 1")
                }
                .padding(.horizontal,compact ? 36 : 24)
                .padding(.top,compact ? 12 : 24)
                .padding(.bottom,compact ? 20 : 24)
            }
        }
    }

    private var citySilhouette: some View {
        Canvas { context,size in
            let buildings:[(CGFloat,CGFloat,CGFloat)] = [(0,0.54,0.16),(0.12,0.80,0.18),(0.28,0.62,0.15),(0.40,0.95,0.17),(0.55,0.72,0.18),(0.70,0.88,0.14),(0.83,0.58,0.20)]
            for (x,height,width) in buildings {
                let rect = CGRect(x:x*size.width,y:(1-height)*size.height,width:width*size.width,height:height*size.height)
                context.fill(Path(rect),with:.color(Color(red:0.075,green:0.18,blue:0.22)))
                for row in 0..<3 {
                    for col in 0..<2 {
                        let pane = CGRect(x:rect.minX+14+CGFloat(col)*18,y:rect.minY+18+CGFloat(row)*28,width:5,height:9)
                        if rect.contains(pane) { context.fill(Path(pane),with:.color((row+col)%3 == 0 ? amber.opacity(0.45) : mint.opacity(0.18))) }
                    }
                }
            }
        }
        .accessibilityHidden(true)
    }

    private var insideStreetPanel: some View {
        TiltStreetView(world:street)
            .frame(maxWidth:.infinity,maxHeight:.infinity)
            .contentShape(Rectangle())
            .gesture(crossingGesture)
            .overlay(alignment:.topTrailing) {
                if !showMainMenu { Button("Retry",action:reset)
                    .font(.system(size:13,weight:.bold,design:.rounded))
                    .foregroundStyle(.white)
                    .frame(minWidth:60,minHeight:44)
                    .background(ink.opacity(0.74),in:Capsule())
                    .accessibilityHint("Restart the cover run")
                    .padding(10) }
            }
            .overlay(alignment:.bottomLeading) {
                if street.phase == .safe || street.phase == .failed || street.phase == .won {
                    Text(street.hint)
                        .font(.system(size:12,weight:.semibold,design:.rounded))
                        .foregroundStyle(.white)
                        .lineLimit(2)
                        .padding(.horizontal,12).padding(.vertical,8)
                        .background(ink.opacity(0.8),in:Capsule())
                        .padding(10)
                        .allowsHitTesting(false)
                }
            }
    }

    private func outsideStreetPanel(size: CGSize) -> some View {
        TiltStreetView(world:street)
            .frame(width:size.width,height:size.height)
            .contentShape(Rectangle())
            .gesture(crossingGesture)
            .overlay(alignment:.top) { titleBar(outside:true) }
            .overlay(alignment:.bottomTrailing) {
                Button("Retry",action:reset)
                    .font(.system(size:13,weight:.bold,design:.rounded))
                    .foregroundStyle(.white)
                    .frame(minWidth:60,minHeight:44)
                    .background(ink.opacity(0.74),in:Capsule())
                    .accessibilityHint("Restart the cover run")
                    .padding(.trailing,54)
                    .padding(.bottom,10)
            }
            .overlay(alignment:.bottomLeading) {
                if !showLevelRoute && (flow.placement == nil || street.phase == .safe || street.phase == .failed || street.phase == .won) {
                    Text(flow.placement == nil ? "Open Duo to guide the cover" : outsideInstruction)
                        .font(.system(size:12,weight:.semibold,design:.rounded))
                        .foregroundStyle(.white)
                        .lineLimit(2)
                        .padding(.horizontal,12).padding(.vertical,8)
                        .background(ink.opacity(0.8),in:Capsule())
                        .padding(10)
                        .allowsHitTesting(false)
                }
            }
            .overlay(alignment:.bottom) {
                if showLevelRoute && street.phase == .won { levelRoute }
            }
    }

    private func titleBar(outside:Bool) -> some View {
        HStack(spacing:10) {
            Text("Corgi Crossroads")
                .font(.system(size:16,weight:.bold,design:.rounded))
                .tracking(-0.35)
                .foregroundStyle(cream)
            Text("01 / 09")
                .font(.system(size:11,weight:.bold,design:.rounded))
                .monospacedDigit()
                .foregroundStyle(cream.opacity(0.72))
            Spacer(minLength:8)
            Button { settings = true } label: {
                Image(systemName:"antenna.radiowaves.left.and.right")
                    .font(.system(size:17,weight:.semibold))
                    .frame(width:44,height:44)
            }
            .buttonStyle(.plain)
            .foregroundStyle(motion.isFresh || manual ? mint : amber)
            .accessibilityLabel("Motion connection settings")
        }
        .padding(.leading,16)
        .padding(.trailing,outside ? 54 : 10)
        .frame(height:48)
        .background(ink.opacity(0.94))
        .overlay(alignment:.bottom) { Rectangle().fill(amber.opacity(0.45)).frame(height:1) }
    }

    private var levelRoute: some View {
        VStack(alignment:.leading,spacing:10) {
            HStack(spacing:12) {
                Text("Street repaired")
                    .font(.system(size:19,weight:.bold,design:.rounded))
                    .foregroundStyle(cream)
                Text("LEVEL 02 NEXT")
                    .font(.system(size:11,weight:.bold,design:.rounded))
                    .foregroundStyle(mint)
                Spacer(minLength:4)
                Button { showLevelRoute = false } label: {
                    Image(systemName:"xmark").frame(width:44,height:44)
                }
                .buttonStyle(.plain)
                .accessibilityLabel("Close level route")
            }
            HStack(spacing:7) {
                ForEach(1...9,id:\.self) { level in
                    Text(String(format:"%02d",level))
                        .font(.system(size:11,weight:.bold,design:.rounded))
                        .monospacedDigit()
                        .frame(maxWidth:.infinity,minHeight:32)
                        .foregroundStyle(level == 1 ? ink : level == 2 ? mint : cream.opacity(0.45))
                        .background(level == 1 ? mint : cream.opacity(level == 2 ? 0.11 : 0.05),in:Capsule())
                        .overlay { Capsule().strokeBorder(level == 2 ? mint.opacity(0.6) : .clear,lineWidth:1) }
                        .accessibilityLabel(level == 1 ? "Level 1 complete" : level == 2 ? "Level 2 next" : "Level \(level) locked")
                }
            }
            Text("More crossings are coming to the district.")
                .font(.system(size:12,weight:.medium,design:.rounded))
                .foregroundStyle(cream.opacity(0.74))
        }
        .padding(.leading,16)
        .padding(.trailing,54)
        .padding(.vertical,10)
        .background(ink.opacity(0.96))
    }

    private var outsideInstruction: String {
        switch street.phase {
        case .waiting: return "Close Duo to see the cover land."
        case .dropping: return "Watch the cover settle into the street."
        case .safe: return "Swipe right to cross. Swipe up to jump."
        case .failed: return "Swipe across the street, or retry the cover."
        case .won: return "Kaprao made it safely across."
        }
    }

    private var crossingGesture: some Gesture {
        DragGesture(minimumDistance:20)
            .onChanged { value in
                guard flow.released else { return }
                if abs(value.translation.width) > abs(value.translation.height),
                   abs(value.translation.width) > 20 {
                    if value.translation.width > 0 { street.moveRight() }
                    else { street.moveLeft() }
                }
            }
            .onEnded { value in
                guard flow.released else { return }
                if abs(value.translation.width) > abs(value.translation.height) {
                    if value.translation.width > 0 { street.moveRight() }
                    else { street.moveLeft() }
                } else if value.translation.height < 0 { street.jump() }
                else { street.dash() }
            }
    }
    private var tiltPad: some View {
        VStack(spacing:4) {
            GeometryReader { geo in
                ZStack {
                    RoundedRectangle(cornerRadius:10).fill(.white.opacity(0.06))
                    Text("Drag to set tilt").font(.caption2).foregroundStyle(.white.opacity(0.5))
                    Circle().fill(mint).frame(width:12,height:12)
                        .offset(x:manualTilt.dx/0.6*geo.size.width/2,y:-manualTilt.dy/0.6*geo.size.height/2)
                }.contentShape(Rectangle()).gesture(DragGesture(minimumDistance:0).onChanged { value in
                    setManualTilt(CGVector(dx:max(-0.6,min(0.6,(value.location.x/geo.size.width*2-1)*0.6)),
                                           dy:max(-0.6,min(0.6,(1-value.location.y/geo.size.height*2)*0.6))))
                })
            }.frame(height:35)
            HStack(spacing:6) {
                tiltButton("arrow.left",label:"Tilt left",value:CGVector(dx:-0.6,dy:0))
                tiltButton("arrow.down",label:"Tilt down",value:CGVector(dx:0,dy:-0.6))
                tiltButton("circle",label:"Level board",value:.zero)
                tiltButton("arrow.up",label:"Tilt up",value:CGVector(dx:0,dy:0.6))
                tiltButton("arrow.right",label:"Tilt right",value:CGVector(dx:0.6,dy:0))
            }
        }
    }
    private func tiltButton(_ symbol:String,label:String,value:CGVector)->some View {
        Button { setManualTilt(value) } label: {
            Image(systemName:symbol).font(.caption.bold()).frame(maxWidth:.infinity,minHeight:38)
                .background(.white.opacity(0.08),in:RoundedRectangle(cornerRadius:8))
        }.buttonStyle(.plain).accessibilityLabel(label)
    }
    private func setManualTilt(_ value:CGVector) { manualTilt = value; configureInput() }
    private var inputSettings: some View {
        NavigationStack {
            Form {
                Section("Live input") {
                    Text(motion.status)
                    #if targetEnvironment(simulator)
                    TextField("Mac receiver host",text:$host).textInputAutocapitalization(.never).autocorrectionDisabled()
                    SecureField("Pairing token printed by receiver",text:$token).textInputAutocapitalization(.never).autocorrectionDisabled()
                    Button("Connect iPad bridge") { manual = false; connect() }
                    Text("Run MotionBridge/Receiver/receiver.py on this Mac. On your iPad, open Motion Sender and enter this Mac’s Wi-Fi IP and the same token.").font(.caption)
                    #else
                    Text("This device uses its own Core Motion sensors.").font(.caption)
                    #endif
                    Button("Calibrate neutral") {
                        if let g = motion.sample?.gravity, motion.isFresh { neutral = CGVector(dx:g.x,dy:g.y); configureInput() }
                    }.disabled(!motion.isFresh)
                }
                Section("Sound") {
                    Toggle("Mute",isOn:Binding(get:{ audio.muted },set:{ value in if value != audio.muted { audio.toggleMute() } }))
                }
                Section("Simulator diagnostics") {
                    Toggle("Manual tilt pad (simulated input)",isOn:$manual).onChange(of:manual) { _,_ in connect(); configureInput() }
                    Text("Manual input tests gameplay only. It does not verify iPad sensor streaming.").font(.caption)
                }
            }.navigationTitle("Motion input").toolbar { ToolbarItem(placement:.confirmationAction) { Button("Done") { settings = false } } }
        }
    }
    private func connect() {
        if manual { motion.stop() } else { motion.start(host:host,token:token) }
    }
    private func configureInput() {
        let paused = lifecycle != .active || settings || showMainMenu || flow.display != .inside
        let useManual = manual, manualValue = manualTilt, zero = neutral
        board.sampleProvider = { [weak motion] in
            guard !paused else { return nil }
            if useManual { return manualValue }
            guard let motion, motion.isFresh, let g = motion.sample?.gravity else { return nil }
            return CGVector(dx:max(-0.6,min(0.6,g.x-zero.dx)),dy:max(-0.6,min(0.6,g.y-zero.dy)))
        }
    }
    private func updateLayout(size:CGSize,divider:CGRect?,activeDivision:Bool) {
        transitionTask?.cancel(); outerStable = false; manualTilt = .zero
        if divider != nil { sawDivision = true }
        let mode = CrossroadsFlow.display(size:size,horizontalDivision:divider != nil,
            activeDivision:activeDivision,hingeKnown:hingeKnown,hingeClosed:hingeClosed,sawDivision:sawDivision)
        NSLog("[CrossroadsLayout] size=%@ division=%@ active=%@ closed=%@ display=%@",String(describing:size),String(describing:divider),String(activeDivision),String(hingeClosed),String(describing:mode))
        street.setOutsidePresentation(mode == .outside)
        flow.updateDisplay(mode,active:lifecycle == .active,renderReady:false)
        configureInput(); updatePause()
        if mode == .outside {
            transitionTask = Task { @MainActor in
                try? await Task.sleep(nanoseconds:300_000_000)
                guard !Task.isCancelled else { return }
                outerStable = true; updatePause(); attemptDrop()
            }
        }
    }
    private func updatePause() {
        street.scene.isPaused = lifecycle != .active || settings || showMainMenu || flow.display == .unknown || (flow.display == .outside && !outerStable)
    }
    private func attemptDrop() {
        guard flow.display == .outside, outerStable, !settings, !showMainMenu else { return }
        if flow.updateDisplay(.outside,active:lifecycle == .active,renderReady:street.rendererReady), let offset = flow.placement {
            street.drop(offset:offset)
        }
    }
    private func reset() {
        audio.stopAll(); audio.play("retry"); showLevelRoute = false; flow.reset(); board.reset(); street.reset(); manualTilt = .zero; configureInput()
    }
}
