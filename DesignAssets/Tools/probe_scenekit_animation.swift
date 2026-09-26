import Foundation
import SceneKit
import QuartzCore
import Metal
let paths=CommandLine.arguments.dropFirst()
for path in paths {
 do {
 let scene=try SCNScene(url:URL(fileURLWithPath:path),options:nil)
 let renderer=SCNRenderer(device:MTLCreateSystemDefaultDevice(),options:nil);renderer.scene=scene;renderer.isPlaying=true
 var keys=0
 scene.rootNode.enumerateChildNodes{n,_ in for k in n.animationKeys { if let p=n.animationPlayer(forKey:k){p.animation.usesSceneTimeBase=true;p.animation.repeatCount=100;p.play();keys+=1}}}
 func values()->[Double]{var result=[Double]();scene.rootNode.enumerateChildNodes{n,_ in if let s=n.skinner {for b in s.bones {let t=b.presentation.transform;result += [Double(t.m11),Double(t.m12),Double(t.m13),Double(t.m21),Double(t.m22),Double(t.m23),Double(t.m31),Double(t.m32),Double(t.m33),Double(t.m41),Double(t.m42),Double(t.m43)]}}};return result}
 renderer.sceneTime=0;renderer.update(atTime:0);let a=values()
 renderer.sceneTime=0.23;renderer.update(atTime:0.23);let b=values()
 let delta=zip(a,b).map{abs($0-$1)}.max() ?? 0
 print("\(URL(fileURLWithPath:path).lastPathComponent) tracks=\(keys) sampledBoneComponents=\(a.count) maxChange=\(delta) \(delta>0.00001 ? "MOTION_PASS" : "MOTION_UNCONFIRMED")")
 } catch {print("FAIL \(error)")}
}
