// Asset-only native hierarchy/anchor regression check. No gameplay implementation.
import Foundation
import SceneKit
let root=URL(fileURLWithPath:CommandLine.arguments[1]);var results=[[String:Any]]()
for slug in ["01-workshop","02-garden","03-terrace"] {
 let folder=root.appendingPathComponent(slug)
 let g=try JSONSerialization.jsonObject(with:Data(contentsOf:folder.appendingPathComponent("Validation/geometry.json"))) as! [String:Any]
 let anchors=g["anchors_game"] as! [String:[Double]]
 for suffix in ["assembled","colliders"] {
  let scene=try SCNScene(url:folder.appendingPathComponent("Runtime/\(slug)-\(suffix).scn"),options:[.checkConsistency:true])
  var count=0;scene.rootNode.enumerateChildNodes{n,_ in if n.geometry != nil{count += 1}}
  precondition(count == (suffix == "assembled" ? 19 : 23))
  let beam=scene.rootNode.childNode(withName:"bridge_beam",recursively:true)!
  let gate=scene.rootNode.childNode(withName:"release_gate",recursively:true)!
  precondition(gate.parent?.name == "upper_chute" && beam.parent?.name != "upper_chute")
  var checked=0
  if suffix == "assembled" {
   for (name,expected) in anchors {
    guard let n=scene.rootNode.childNode(withName:name,recursively:true) else {fatalError("Missing anchor \(slug) \(name)")}
    let p=n.worldPosition;let actual=[Double(p.x),Double(p.y),Double(p.z)]
    precondition(zip(actual,expected).allSatisfy{abs($0-$1)<0.0001},"Anchor position mismatch \(name)");checked+=1
   }
   precondition(scene.rootNode.childNode(withName:"ANCHOR_held_beam_center",recursively:true)?.parent?.name == "upper_chute")
  }
  results.append(["stage":slug,"file":suffix,"result":"pass","mesh_count":count,"anchors_checked":checked,"gate_follows_chute":true,"beam_independent":true])
 }
}
let data=try JSONSerialization.data(withJSONObject:results,options:[.prettyPrinted,.sortedKeys]);try data.write(to:root.appendingPathComponent("native-validation.json"));print("NATIVE_STAGE_PASS \(results.count) files; 45 anchor positions checked")
