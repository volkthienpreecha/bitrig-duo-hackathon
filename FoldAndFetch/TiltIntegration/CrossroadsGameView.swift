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
    @State private var manual = false
    @State private var manualTilt = CGVector.zero
    @State private var neutral = CGVector.zero
    @AppStorage("motionBridgeHost") private var host = "127.0.0.1"
    @State private var token = ""
    private let ink = Color(red:0.025,green:0.055,blue:0.09)
    private let mint = Color(red:0.26,green:0.96,blue:0.79)

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
                ink.ignoresSafeArea()
                if flow.display == .outside {
                    streetPanel(outside:true).frame(width:geometry.size.width,height:geometry.size.height)
                } else {
                    VStack(spacing:6) {
                        header
                        HStack {
                            Label("COVER RUN",systemImage:"circle.hexagongrid.fill").font(.caption.bold())
                            Spacer()
                            Text(flow.released ? "DELIVERED" : board.held ? "PLACEMENT HELD" : "TILT TO GUIDE").font(.caption2.bold()).foregroundStyle(mint)
                        }
                        SpriteView(scene:board).frame(maxWidth:.infinity,maxHeight:.infinity).layoutPriority(1)
                            .clipShape(RoundedRectangle(cornerRadius:18))
                        Text(flow.released ? "Cover delivered · guide Kaprao across" : board.held ? "Close Duo to drop the cover" : board.hint)
                            .font(.caption).foregroundStyle(board.held ? mint : .white.opacity(0.85))
                    }.padding(.horizontal,14).padding(.top,8).padding(.bottom,10)
                        .frame(width:geometry.size.width,height:max(100,upperHeight))
                    streetPanel(outside:false).frame(width:geometry.size.width,height:max(100,geometry.size.height-lowerY)).offset(y:lowerY)
                    Rectangle().fill(mint.opacity(0.6)).frame(height:2).offset(y:upperHeight)
                }
            }
            .onChange(of:key,initial:true) { _,_ in updateLayout(size:geometry.size,divider:divider,activeDivision:activeDivision) }
        }
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
            case .won: audio.play("success")
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
                board.held = flow.placement != nil
            }
            connect(); configureInput()
        }
        .preferredColorScheme(.dark)
    }

    private var header: some View {
        HStack(spacing:8) {
            VStack(alignment:.leading,spacing:1) {
                Text("Corgi Crossroads").font(.system(size:21,weight:.heavy,design:.rounded))
                Text("A LITTLE TILT. A SAFER STREET.").font(.system(size:8,weight:.bold,design:.monospaced)).tracking(1)
                    .foregroundStyle(.white.opacity(0.5))
            }
            Spacer()
            Button { settings = true } label: { Image(systemName:"antenna.radiowaves.left.and.right").frame(width:44,height:44) }
                .tint(motion.isFresh || manual ? mint : .orange).accessibilityLabel("Motion connection settings")
        }
    }

    private func streetPanel(outside: Bool) -> some View {
        VStack(spacing:7) {
            if outside { header.padding(.horizontal,14) }
            HStack {
                Text(outside ? "THE CROSSING" : "KAPRAO IS WAITING").font(.caption.bold())
                Spacer()
                Text(street.phase == .safe ? "SAFE TO CROSS" : street.phase == .won ? "STREET REPAIRED" : "UTILITY CORNER")
                    .font(.caption2.bold()).foregroundStyle(mint)
            }.padding(.horizontal,16)
            TiltStreetView(world:street)
                .frame(maxWidth:.infinity,maxHeight:.infinity)
                .layoutPriority(1)
                .gesture(DragGesture(minimumDistance:20).onEnded { value in
                    guard flow.released else { return }
                    if abs(value.translation.width) > abs(value.translation.height) {
                        if value.translation.width > 0 { street.moveRight() } else { street.moveLeft() }
                    } else if value.translation.height < 0 { street.jump() } else { street.dash() }
                })
                .overlay(alignment:.top) {
                    if outside && flow.placement == nil {
                        Text("Open Duo to guide the cover").font(.callout.bold()).padding(12).background(ink.opacity(0.9),in:Capsule()).padding(8)
                    }
                }
                .clipShape(RoundedRectangle(cornerRadius:18))
                .padding(.horizontal,10)
            Text(street.hint).font(.caption).multilineTextAlignment(.center).padding(.horizontal,14)
            if flow.released {
                Text("OPENING COVERED  \(Int(street.coverage * 100))%")
                    .font(.system(size:10,weight:.semibold,design:.monospaced)).foregroundStyle(mint)
                HStack(spacing:9) {
                    control("arrow.left",label:"Move left",action:street.moveLeft)
                    control("arrow.up",label:"Jump",action:street.jump)
                    control("arrow.down",label:"Dash",action:street.dash)
                    control("arrow.right",label:"Move right",action:street.moveRight)
                }
            } else if manual && !outside && !board.held {
                tiltPad.frame(height:80).padding(.horizontal,16)
            }
            HStack {
                Circle().fill(manual || motion.isFresh ? mint : Color.orange).frame(width:6,height:6)
                Text(manual ? "MANUAL TILT · DIAGNOSTIC" : motion.status).font(.system(size:9,weight:.medium,design:.monospaced)).lineLimit(2)
                Spacer()
                Button("Retry",action:reset).font(.caption.bold()).frame(minWidth:52,minHeight:44)
            }.padding(.horizontal,16)
        }.padding(.top,10).padding(.bottom,4)
    }

    private func control(_ symbol:String,label:String,action:@escaping ()->Void)->some View {
        Button(action:action) { Image(systemName:symbol).font(.headline).frame(width:52,height:44).background(.white.opacity(0.09),in:RoundedRectangle(cornerRadius:12)) }
            .tint(mint).accessibilityLabel(label)
    }
    private var tiltPad: some View {
        GeometryReader { geo in
            ZStack {
                RoundedRectangle(cornerRadius:13).fill(.white.opacity(0.06))
                Text("Drag to tilt · release to level").font(.caption2).foregroundStyle(.white.opacity(0.5))
                Circle().fill(mint).frame(width:16,height:16).offset(x:manualTilt.dx/0.6*geo.size.width/2,y:-manualTilt.dy/0.6*geo.size.height/2)
            }.contentShape(Rectangle()).gesture(DragGesture(minimumDistance:0).onChanged { value in
                manualTilt = CGVector(dx:max(-0.6,min(0.6,(value.location.x/geo.size.width*2-1)*0.6)),dy:max(-0.6,min(0.6,(1-value.location.y/geo.size.height*2)*0.6)))
                configureInput()
            }.onEnded { _ in manualTilt = .zero; configureInput() })
        }
    }
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
        let paused = lifecycle != .active || settings || flow.display != .inside
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
        street.scene.isPaused = lifecycle != .active || settings || flow.display == .unknown || (flow.display == .outside && !outerStable)
    }
    private func attemptDrop() {
        guard flow.display == .outside, outerStable, !settings else { return }
        if flow.updateDisplay(.outside,active:lifecycle == .active,renderReady:street.rendererReady), let offset = flow.placement {
            street.drop(offset:offset)
        }
    }
    private func reset() {
        audio.stopAll(); audio.play("retry"); flow.reset(); board.reset(); street.reset(); manualTilt = .zero; configureInput()
    }
}
