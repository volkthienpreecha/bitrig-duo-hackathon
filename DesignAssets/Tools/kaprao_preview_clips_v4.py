"""Render genuine rigged motion previews from the finalized Blender asset."""
import bpy,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1] / 'Revisions/Kaprao-v4'
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'Source/Kaprao/kaprao.blend'))
scene=bpy.context.scene;rig=bpy.data.objects['Kaprao_Rig'];scene.render.engine='CYCLES';scene.cycles.samples=12
scene.render.resolution_x=480;scene.render.resolution_y=480;scene.render.resolution_percentage=100
cam=scene.camera;cam.location=(3.6,-3.2,2);cam.rotation_euler=(Vector((.04,0,.59))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.64
dest=ROOT/'Previews/MotionFrames';dest.mkdir(parents=True,exist_ok=True)
for name,frames in [('Idle_Look',[1,31,61,91]),('Walk_InPlace',list(range(1,25,2))),('Jump_Fall',[1,7,13,19,25,31,37]),('Celebrate',[1,11,21,31,41,51,61])]:
    rig.animation_data.action=bpy.data.actions[name]
    if rig.animation_data.action.slots:rig.animation_data.action_slot=rig.animation_data.action.slots[0]
    for f in frames:
        scene.frame_set(f);scene.render.filepath=str(dest/('%s-%03d.png'%(name,f)));bpy.ops.render.render(write_still=True)
print('KAPRAO_MOTION_PREVIEWS_COMPLETE')
