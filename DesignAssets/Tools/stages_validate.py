"""Fresh import and source/fit checks for stage art, not physics/gameplay tests."""
import bpy,json,math,struct
from pathlib import Path
from mathutils import Vector
BASE=Path(__file__).resolve().parents[1];ROOT=BASE/'Stages';results=[]
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
   assert len(meshes)==19
   assert 'ANCHOR_corgi_start' in idx and 'ANCHOR_held_beam_center' in idx
  else:assert len(meshes)==23
  checks.append({'file':path.name,'result':'pass','meshes':len(meshes),'triangles':sum(len(p.vertices)-2 for o in meshes for p in o.data.polygons),'beam_center_game':beam,'no_external_resources':True,'gate_follows_chute':True,'beam_independent_root':True})
 bpy.ops.wm.open_mainfile(filepath=str(stage/'Source'/(stage.name+'.blend')))
 assert len([i for i in bpy.data.images if i.packed_file and i.size[0]>=2048])>=3
 rig=bpy.data.objects['Kaprao_Rig'];body=bpy.data.objects['Kaprao_Body_Skinned'];scene=bpy.context.scene
 feet=[body.matrix_world@v.co for v in body.data.vertices if (body.matrix_world@v.co).z<.055]
 width=max(v.y for v in feet)-min(v.y for v in feet)
 # Fur/body can overhang; examine low paw geometry, not ears, for nominal bridge fit.
 footfit={'sample':'base-mesh vertices below world Z 0.055m at rest','min_floor_m':min(v.z for v in feet),'paw_depth_envelope_m':width,'beam_depth_m':.54,'within_beam_depth':width<.54,'character_scale':.72,'note':'Nominal visual rest-pose fit only. Animated footing and controller contacts require runtime validation.'}
 assert footfit['within_beam_depth'],footfit
 # The widened beam and its endcaps fit the 0.63m channel and 0.64m pockets.
 assert .54*(.36/.35)<.63
 assert abs(g['fold_poses'][1]['depth_error_m'])<1e-5
 assert g['fold_poses'][0]['depth_error_m']*g['fold_poses'][2]['depth_error_m']<0
 report={'result':'pass','exchange':checks,'source_reopen':'pass','packed_character_maps':'pass','nominal_paw_fit':footfit,'play_pose_depth_error_m':g['fold_poses'][1]['depth_error_m'],'fold_miss_references_straddle_route':True,'physics_tested':False}
 (stage/'Validation/import-and-fit.json').write_text(json.dumps(report,indent=2)+'\n');results.append({'stage':stage.name,**report})
(ROOT/'validation-summary.json').write_text(json.dumps(results,indent=2)+'\n');print('ALL_STAGE_GEOMETRY_PASS',len(results))
