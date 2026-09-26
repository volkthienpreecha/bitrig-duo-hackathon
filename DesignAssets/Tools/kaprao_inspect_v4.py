"""Render the actual Rodin reconstruction from four sides before editing it."""
import bpy, json, math
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1] / 'Revisions/Kaprao-v4'
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(ROOT/'Source/Incoming/kaprao-rodin-original.glb'))
objects = [o for o in bpy.context.scene.objects if o.type == 'MESH']
points = [o.matrix_world @ Vector(p) for o in objects for p in o.bound_box]
lo = Vector([min(p[i] for p in points) for i in range(3)])
hi = Vector([max(p[i] for p in points) for i in range(3)])
center = (lo+hi)/2
size = max(hi-lo)
report = {'bounds':[list(lo),list(hi)],'objects':[], 'images':[]}
for o in objects:
    report['objects'].append({'name':o.name,'vertices':len(o.data.vertices),'polygons':len(o.data.polygons),'materials':[m.name for m in o.data.materials]})
for im in bpy.data.images:
    report['images'].append({'name':im.name,'size':list(im.size),'packed':bool(im.packed_file)})
(ROOT/'Validation/rodin-original.json').write_text(json.dumps(report,indent=2))
scene=bpy.context.scene
scene.render.engine='CYCLES';scene.cycles.samples=20
scene.render.resolution_x=720;scene.render.resolution_y=720;scene.render.resolution_percentage=100
scene.world.color=(.22,.22,.22)
scene.view_settings.view_transform='AgX'
def aim(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
for name,offset,power,area in [('Key',(-2,-3,4),450,3),('Fill',(3,1,2),230,3),('Rim',(-2,3,3),320,2)]:
    bpy.ops.object.light_add(type='AREA',location=center+Vector(offset)*size)
    o=bpy.context.object;o.name=name;o.data.energy=power*size*size;o.data.shape='DISK';o.data.size=area*size;aim(o,center)
bpy.ops.object.camera_add()
cam=bpy.context.object;scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=size*1.4
for name,offset in [('negative-y',(0,-3,.25)),('positive-y',(0,3,.25)),('negative-x',(-3,0,.25)),('three-quarter',(2.5,-3,1.1))]:
    cam.location=center+Vector(offset)*size;aim(cam,center)
    scene.render.filepath=str(ROOT/'Previews'/('rodin-'+name+'.png'))
    bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Source/Incoming/kaprao-rodin-inspected.blend'))
print('INSPECTED_RODIN',json.dumps(report))
