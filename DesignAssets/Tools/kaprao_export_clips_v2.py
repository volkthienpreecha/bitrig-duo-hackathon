"""Export separate Y-up USD animation files from Kaprao's four named actions."""
import bpy, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1] / 'Revisions/Kaprao-v2'
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'Source/Kaprao/kaprao.blend'))
rig=bpy.data.objects['Kaprao_Rig'];scene=bpy.context.scene
for t in rig.animation_data.nla_tracks:t.mute=True
bpy.ops.object.select_all(action='DESELECT')
for name in ('Kaprao_Rig','Kaprao_Body_Skinned','Kaprao_RGB_Sunglasses_REMOVABLE'):
    bpy.data.objects[name].hide_set(False);bpy.data.objects[name].select_set(True)
bpy.context.view_layer.objects.active=rig
report=[]
rig.animation_data.action=None
for b in rig.pose.bones:b.location=(0,0,0);b.rotation_euler=(0,0,0);b.scale=(1,1,1)
scene.frame_set(1)
bpy.ops.wm.usd_export(filepath=str(ROOT/'Exports/Kaprao/kaprao-static.usdc'),selected_objects_only=True,export_animation=False,export_materials=True,export_armatures=True,convert_orientation=True,export_global_forward_selection='NEGATIVE_Z',export_global_up_selection='Y',convert_world_material=False)
for name,end in [('Idle_Look',121),('Walk_InPlace',25),('Jump_Fall',37),('Celebrate',61)]:
    for b in rig.pose.bones:b.location=(0,0,0);b.rotation_euler=(0,0,0);b.scale=(1,1,1)
    rig.animation_data.action=bpy.data.actions[name]
    if bpy.data.actions[name].slots:rig.animation_data.action_slot=bpy.data.actions[name].slots[0]
    scene.frame_start=1;scene.frame_end=end;scene.frame_set(1)
    dest=ROOT/'Exports/Kaprao'/('kaprao-'+name+'.usdc')
    bpy.ops.wm.usd_export(filepath=str(dest),selected_objects_only=True,export_animation=True,export_materials=True,export_armatures=True,convert_orientation=True,export_global_forward_selection='NEGATIVE_Z',export_global_up_selection='Y',convert_world_material=False)
    report.append({'clip':name,'file':str(dest.relative_to(ROOT)),'frames':[1,end],'fps':30,'loop':name in ['Idle_Look','Walk_InPlace'],'root_motion':False})
(ROOT/'Validation/kaprao-usd-clips.json').write_text(json.dumps(report,indent=2))
print('KAPRAO_USD_CLIPS_EXPORTED',json.dumps(report))
