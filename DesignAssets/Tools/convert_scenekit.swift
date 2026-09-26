// Asset conversion utility only. No game code. Uses Apple's SceneKit USD importer.
import Foundation
import SceneKit
import AppKit
let args = Array(CommandLine.arguments.dropFirst())
guard args.count == 2 else {fatalError("usage: convert_scenekit INPUT_DIRECTORY OUTPUT_DIRECTORY")}
let input = URL(fileURLWithPath:args[0]);let output=URL(fileURLWithPath:args[1])
try FileManager.default.createDirectory(at:output,withIntermediateDirectories:true)
var reports = [[String:Any]]()
for url in try FileManager.default.contentsOfDirectory(at:input,includingPropertiesForKeys:nil).filter({$0.pathExtension == "usdc"}).sorted(by:{$0.path<$1.path}) {
 do {
  let scene=try SCNScene(url:url,options:[.checkConsistency:true])
  var count=0,meshes=0,skins=0,tracks=0,materials=Set<String>(),textures=0
  scene.rootNode.enumerateChildNodes {n,_ in
   count+=1;if n.geometry != nil{meshes+=1};if n.skinner != nil{skins+=1};tracks+=n.animationKeys.count
   for m in n.geometry?.materials ?? [] {
    materials.insert(m.name ?? "unnamed")
    for p in [m.diffuse,m.normal,m.metalness,m.roughness,m.emission,m.ambientOcclusion] {
     if let u=p.contents as? URL, let image=NSImage(contentsOf:u){p.contents=image;textures+=1}
    }
   }
  }
  let dest=output.appendingPathComponent(url.deletingPathExtension().lastPathComponent+".scn")
  guard scene.write(to:dest,options:nil,delegate:nil,progressHandler:nil) else {throw NSError(domain:"AssetExport",code:1)}
  let reloaded=try SCNScene(url:dest,options:[.checkConsistency:true]);var rm=0,rs=0,ra=0
  reloaded.rootNode.enumerateChildNodes{n,_ in if n.geometry != nil{rm+=1};if n.skinner != nil{rs+=1};ra+=n.animationKeys.count}
  guard rm==meshes && rs==skins && ra==tracks else {throw NSError(domain:"AssetRoundtrip",code:2)}
  let box=reloaded.rootNode.boundingBox
  reports.append(["source":url.lastPathComponent,"runtime":dest.lastPathComponent,"nodes":count,"meshes":meshes,"skins":skins,"animationTracks":tracks,"materials":materials.sorted(),"embeddedTextureConversions":textures,"bounds":[[box.min.x,box.min.y,box.min.z],[box.max.x,box.max.y,box.max.z]],"roundtrip":"pass"])
  print("PASS \(url.lastPathComponent) -> \(dest.lastPathComponent) meshes=\(meshes) skins=\(skins) tracks=\(tracks)")
 }catch{reports.append(["source":url.lastPathComponent,"error":String(describing:error)]);print("FAIL \(url): \(error)")}
}
let data=try JSONSerialization.data(withJSONObject:reports,options:[.prettyPrinted,.sortedKeys]);try data.write(to:output.appendingPathComponent("scenekit-conversion.json"))
