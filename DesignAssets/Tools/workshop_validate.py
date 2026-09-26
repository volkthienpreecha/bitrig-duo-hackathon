"""Validate generated exchange geometry in Blender; no game code is executed."""
import bpy,json,math,struct
from pathlib import Path
from mathutils import Vector
BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'Validation'/'workshop-import-validation.json'
EX=BASE/'Exports'/'Workshop'
def glb_json(path):
    data=path.read_bytes();magic,version,length=struct.unpack_from('<4sII',data)
    assert magic==b'glTF' and version==2 and length==len(data)
    chunklen,kind=struct.unpack_from('<II',data,12);assert kind==0x4E4F534A
    return json.loads(data[20:20+chunklen])
results={}
for path in sorted(EX.glob('*.glb')):
    doc=glb_json(path)
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    bpy.ops.import_scene.gltf(filepath=str(path))
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
    coords=[o.matrix_world@Vector(c) for o in meshes for c in o.bound_box]
    bounds=[[min(p[i] for p in coords) for i in range(3)],[max(p[i] for p in coords) for i in range(3)]]
    nonunit=[o.name for o in bpy.context.scene.objects if any(abs(s-1)>1e-5 for s in o.scale)]
    finite=all(math.isfinite(v) for o in meshes for p in o.data.vertices for v in p.co)
    tris=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in meshes)
    results[path.name]={
      'blender_import':'passed','mesh_count':len(meshes),'triangles':tris,'finite_coordinates':finite,
      'non_unit_scale_nodes':nonunit,'bounds_in_blender_z_up':bounds,
      'material_primitives':sum(len(m['primitives']) for m in doc.get('meshes',[])),
      'external_resources':[d['uri'] for d in doc.get('buffers',[])+doc.get('images',[]) if 'uri' in d],
      'camera_count':len(doc.get('cameras',[])),'animation_count':len(doc.get('animations',[])),
      'node_count':len(doc.get('nodes',[]))}
    assert finite and not nonunit,(path.name,nonunit)
    assert not results[path.name]['external_resources']
    assert results[path.name]['camera_count']==0 and results[path.name]['animation_count']==0
    if path.name not in ['workshop-assembled.glb','workshop-collision-proxies.glb']:
        assert len(meshes)==1,(path.name,len(meshes))
assert results['workshop-assembled.glb']['mesh_count']==19
assert results['workshop-collision-proxies.glb']['triangles']==276
assembled=glb_json(EX/'workshop-assembled.glb');nodes=assembled['nodes']
indices={n.get('name'):i for i,n in enumerate(nodes)}
parents={child:i for i,node in enumerate(nodes) for child in node.get('children',[])}
assert indices['bridge_beam'] not in parents,'Beam must remain an independent world root.'
assert parents[indices['release_gate']]==indices['upper_chute']
assert all(abs(a-b)<1e-5 for a,b in zip(nodes[indices['upper_chute']]['translation'],[0,3,-1.2]))
assert all(abs(a-b)<1e-5 for a,b in zip(nodes[indices['bridge_beam']]['translation'],[0,-.11,0]))
report={
 'status':'passed','blender':bpy.app.version_string,'checks':results,
 'hierarchy_checks':{'beam_is_independent_root':True,'gate_follows_upper_chute':True,'hinge_game_position':[0,3,-1.2],'beam_game_position':[0,-.11,0]},
 'scope':'Fresh Blender reimport plus GLB container/resource/mesh inspection. Not mobile renderer or physics verification.'}
OUT.write_text(json.dumps(report,indent=2));print('WORKSHOP_VALIDATION_PASSED',len(results),flush=True)
