// Preparation tool: portable image-based character asset and native render probes.
import Foundation
import SceneKit
import AppKit
import Metal
let root = URL(fileURLWithPath:CommandLine.arguments[1])
let runtime = root.appendingPathComponent("Runtime")
let imageURL = runtime.appendingPathComponent("kaprao-idle.png")
let image = NSImage(contentsOf:imageURL)!
let bitmap = NSBitmapImageRep(data:try Data(contentsOf:imageURL))!
let width = bitmap.pixelsWide, height = bitmap.pixelsHigh
var left=width,top=height,right=0,bottom=0
for y in 0..<height {for x in 0..<width {if (bitmap.colorAt(x:x,y:y)?.alphaComponent ?? 0)>0.5 {left=min(left,x);right=max(right,x+1);top=min(top,y);bottom=max(bottom,y+1)}}}
let visibleHeight=0.84
let units=visibleHeight/Double(bottom-top)
let plane=SCNPlane(width:Double(width)*units,height:Double(height)*units)
let material=SCNMaterial();material.name="Kaprao_Illustration_Unlit"
material.lightingModel = .constant;material.diffuse.contents=image
material.isDoubleSided=true;material.blendMode = .alpha
material.transparencyMode = .singleLayer
material.readsFromDepthBuffer=true;material.writesToDepthBuffer=false
material.diffuse.magnificationFilter = .linear;material.diffuse.minificationFilter = .linear
material.diffuse.mipFilter = .linear;material.diffuse.wrapS = .clamp;material.diffuse.wrapT = .clamp
plane.materials=[material]
let scene=SCNScene();let player=SCNNode();player.name="KapraoSpriteRoot";scene.rootNode.addChildNode(player)
let visual=SCNNode(geometry:plane);visual.name="KapraoSpriteVisual";visual.castsShadow=false
visual.position=SCNVector3((Double(width)/2-Double(left+right)/2)*units,(Double(bottom)-Double(height)/2)*units,0)
player.addChildNode(visual)
let output=runtime.appendingPathComponent("kaprao-sprite.scn")
guard scene.write(to:output,options:nil,delegate:nil,progressHandler:nil) else {fatalError("SCN write failed")}
let loaded=try SCNScene(url:output,options:[.checkConsistency:true]);let loadedVisual=loaded.rootNode.childNode(withName:"KapraoSpriteVisual",recursively:true)!
let restoredTexture=loadedVisual.geometry?.firstMaterial?.diffuse.contents
print("RESTORED_TEXTURE",String(describing:restoredTexture.map{type(of:$0)}))
guard restoredTexture != nil, !(restoredTexture is String), !(restoredTexture is URL) else {fatalError("Texture is not embedded")}
let renderer=SCNRenderer(device:MTLCreateSystemDefaultDevice(),options:nil);renderer.scene=loaded
let camera=SCNNode();camera.camera=SCNCamera();camera.camera!.usesOrthographicProjection=true;camera.camera!.orthographicScale=1.06;camera.position=SCNVector3(0,0.42,2);loaded.rootNode.addChildNode(camera);renderer.pointOfView=camera
for (name,color) in [("native-cream",NSColor(calibratedRed:0.91,green:0.86,blue:0.8,alpha:1)),("native-night",NSColor(calibratedRed:0.06,green:0.08,blue:0.13,alpha:1))] {
 loaded.background.contents=color
 let shot=renderer.snapshot(atTime:0,with:CGSize(width:900,height:900),antialiasingMode:.multisampling4X)
 let data=NSBitmapImageRep(data:shot.tiffRepresentation!)!.representation(using:.png,properties:[:])!
 try data.write(to:root.appendingPathComponent("Validation/\(name).png"))
}
let report:[String:Any] = ["nativeImport":"PASS","embeddedTexture":true,"geometryCount":1,"materialCount":1,"physicsBodies":0,"billboardConstraints":0,"pixelSize":[width,height],"alphaBoundsThreshold":0.5,"visibleBoundsTopLeftPixels":[left,top,right,bottom],"visibleHeightMeters":visibleHeight,"planeSizeMeters":[Double(width)*units,Double(height)*units],"visualOffsetMeters":[Double(visual.position.x),Double(visual.position.y),0],"scope":"macOS SceneKit asset reload and render only; no Duo hinge, gameplay or physical-device performance certification"]
try JSONSerialization.data(withJSONObject:report,options:[.prettyPrinted,.sortedKeys]).write(to:root.appendingPathComponent("Validation/native-validation.json"))
print("PASS: embedded image, one native plane, floor-aligned visible silhouette, two native render probes")
let atlasURL=runtime.appendingPathComponent("kaprao-poses.png")
if FileManager.default.fileExists(atPath:atlasURL.path) {
 let atlasImage=NSImage(contentsOf:atlasURL)!
 let atlasScene=SCNScene();atlasScene.background.contents=NSColor(calibratedRed:0.06,green:0.08,blue:0.13,alpha:1)
 let atlasCamera=SCNNode();atlasCamera.camera=SCNCamera();atlasCamera.camera!.usesOrthographicProjection=true;atlasCamera.camera!.orthographicScale=1.15;atlasCamera.position=SCNVector3(0,0,3);atlasScene.rootNode.addChildNode(atlasCamera)
 for index in 0..<6 {
  let col=index%3,row=index/3;let m=material.copy() as! SCNMaterial;m.diffuse.contents=atlasImage
  var transform=SCNMatrix4MakeScale(1.0/3.0,0.5,1);transform.m41=CGFloat(col)/3;transform.m42=CGFloat(row)/2;m.diffuse.contentsTransform=transform
  let card=SCNPlane(width:0.94,height:0.94);card.materials=[m]
  let n=SCNNode(geometry:card);n.position=SCNVector3(Double(col)-1,0.5-Double(row),0);atlasScene.rootNode.addChildNode(n)
 }
 renderer.scene=atlasScene;renderer.pointOfView=atlasCamera
 let preview=renderer.snapshot(atTime:0,with:CGSize(width:1350,height:900),antialiasingMode:.multisampling4X)
 try NSBitmapImageRep(data:preview.tiffRepresentation!)!.representation(using:.png,properties:[:])!.write(to:root.appendingPathComponent("Validation/native-pose-atlas.png"))
 print("PASS: six pose atlas UV cards rendered natively")
}
