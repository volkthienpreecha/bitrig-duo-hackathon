"""Reopen v3 source and sample deformation from actual evaluated meshes."""
import bpy, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'Revisions/Kaprao-v3'
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'Source/Kaprao/kaprao.blend'))
scene=bpy.context.scene;rig=bpy.data.objects['Kaprao_Rig']
for t in rig.animation_data.nla_tracks:t.mute=True
images=[{'name':i.name,'size':list(i.size),'packed':bool(i.packed_file)} for i in bpy.data.images if i.packed_file]
clips=[]
for name,end in [('Idle_Look',121),('Walk_InPlace',25),('Jump_Fall',37),('Celebrate',61)]:
    rig.animation_data.action=bpy.data.actions[name]
    if rig.animation_data.action.slots:rig.animation_data.action_slot=rig.animation_data.action.slots[0]
    poses=[]
    for frame in sorted(set([1,round(end*.25),round(end*.5),round(end*.75),end])):
        scene.frame_set(frame);deps=bpy.context.evaluated_depsgraph_get();points=[]
        for key in ('Kaprao_Body_Skinned','Kaprao_Fine_Fur_Skinned','Kaprao_RGB_Sunglasses_REMOVABLE'):
            obj=bpy.data.objects[key].evaluated_get(deps);mesh=obj.to_mesh();points.extend(obj.matrix_world@v.co for v in mesh.vertices);obj.to_mesh_clear()
        low=[min(p[i] for p in points) for i in range(3)];high=[max(p[i] for p in points) for i in range(3)]
        assert all(math.isfinite(v) for p in points for v in p)
        assert max(high[i]-low[i] for i in range(3))<2
        poses.append({'frame':frame,'bounds_m':[low,high]})
    clips.append({'name':name,'samples':poses})
report={'source_reopen':'pass','packed_images':images,'clips':clips,'scope':'Finite deformation and bounded geometry. Foot locking and locomotion blending are not certified.'}
(ROOT/'Validation/source-deformation.json').write_text(json.dumps(report,indent=2))
print('SOURCE_REOPEN_PASS',images)
print('MIN_POSED_Z',min(s['bounds_m'][0][2] for c in clips for s in c['samples']))
