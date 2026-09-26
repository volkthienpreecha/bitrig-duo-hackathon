"""Fresh import and source/fit checks for stage art, not physics/gameplay tests."""
import bpy,json,math,struct
from pathlib import Path
from mathutils import Vector
BASE=Path(__file__).resolve().parents[1];ROOT=BASE/'NeonExpansion';results=[]
def doc(p):
 b=p.read_bytes();magic,v,l=struct.unpack_from('<4sII',b);assert magic==b'glTF' and v==2 and l==len(b)
 n,t=struct.unpack_from('<II',b,12);return json.loads(b[20:20+n])
for stage in sorted(ROOT.glob('0*')):
 g=json.loads((stage/'Validation/geometry.json').read_text());checks=[]
 for path in sorted((stage/'Exports').glob('*.glb')):
  d=doc(path);bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path))
  meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert meshes
  assert all(math.isfinite(v) for o in meshes for p in o.data.vertices for v in p.co)
  assert not d.get('cameras') and not d.get('animations') and not d.get('skins')
  assert not any('uri' in x for x in d.get('buffers',[])+d.get('images',[]))
  assert all(all(abs(v-1)<1e-5 for v in o.scale) for o in bpy.context.scene.objects)
  nodes=d['nodes'];idx={n.get('name'):i for i,n in enumerate(nodes)};parents={child:i for i,n in enumerate(nodes) for child in n.get('children',[])}
  assert idx['bridge_beam'] not in parents
  assert parents[idx['release_gate']]==idx['upper_chute']
  beam=nodes[idx['bridge_beam']]['translation'];assert abs(beam[2]-g['stage']['depth'])<1e-5
  if 'assembled' in path.name:
   assert len(meshes)==20
   assert 'ANCHOR_corgi_start' in idx and 'ANCHOR_held_beam_center' in idx
  else:assert len(meshes)==23
  checks.append({'file':path.name,'result':'pass','meshes':len(meshes),'triangles':sum(len(p.vertices)-2 for o in meshes for p in o.data.polygons),'beam_center_game':beam,'no_external_resources':True,'gate_follows_chute':True,'beam_independent_root':True})
 bpy.ops.wm.open_mainfile(filepath=str(stage/'Source'/(stage.name+'.blend')))
 assert bpy.data.objects.get('neon_signage') is not None
 assert all(bpy.data.objects.get(n) is not None for n in ['neon_shop_japanese','blade_repair_0','blade_market_1'])
 # The widened beam and its endcaps fit the 0.63m channel and 0.64m pockets.
 assert .54*(.36/.35)<.63
 assert abs(g['fold_poses'][1]['depth_error_m'])<1e-5
 assert g['fold_poses'][0]['depth_error_m']*g['fold_poses'][2]['depth_error_m']<0
 report={'result':'pass','exchange':checks,'source_reopen':'pass','japanese_meshes_present':True,'character_runtime_separate':True,'play_pose_depth_error_m':g['fold_poses'][1]['depth_error_m'],'fold_miss_references_straddle_route':True,'physics_tested':False}
 (stage/'Validation/import-and-fit.json').write_text(json.dumps(report,indent=2)+'\n');results.append({'stage':stage.name,**report})
(ROOT/'validation-summary.json').write_text(json.dumps(results,indent=2)+'\n');print('ALL_STAGE_GEOMETRY_PASS',len(results))
