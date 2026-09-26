"""Finalize and independently inspect the saved editable source after previews."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
BASE=Path(__file__).resolve().parents[1]
path=BASE/'Source/Workshop/fold-and-fetch-workshop.blend'
bpy.ops.wm.open_mainfile(filepath=str(path))
scene=bpy.context.scene
image=bpy.data.images.get('Workshop_Palette')
if image is None:
    image=bpy.data.images.load(str(BASE/'Textures/Workshop/workshop-palette.png'));image.name='Workshop_Palette'
image.use_fake_user=True
if image.packed_file is None:image.pack()
for collection in [bpy.data.meshes,bpy.data.curves,bpy.data.materials]:
    for item in list(collection):
        if item.users==0:collection.remove(item)
scene.camera=bpy.data.objects['CAM_workshop_main'];scene.render.filepath=str(BASE/'Previews/Workshop/workshop-main.png')
visible=bpy.data.collections['00_WORKSHOP_VISIBLE'];coll=bpy.data.collections['90_COLLISION_PROXIES_NONRENDER']
assert bpy.data.objects['bridge_beam'].parent is None
assert bpy.data.objects['release_gate'].parent==bpy.data.objects['upper_chute']
assert abs(bpy.data.objects['upper_chute'].rotation_euler.x)<1e-6
assert all(abs(a-b)<1e-5 for a,b in zip(bpy.data.objects['bridge_beam'].matrix_world.translation,[0,0,-.11]))
scales=[o.name for o in visible.objects if any(abs(s-1)>1e-5 for s in o.scale)]
assert not scales
triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in visible.objects if o.type=='MESH')
def bounds(o):
    points=[o.matrix_world@Vector(c) for c in o.bound_box]
    return ([min(p[i] for p in points) for i in range(3)],[max(p[i] for p in points) for i in range(3)])
beam_bounds=bounds(bpy.data.objects['COL_bridge_beam'])
floor_clearance={}
for obj in coll.objects:
    if obj.name.startswith('COL_floor_'):
        lo,hi=bounds(obj);overlap=[min(beam_bounds[1][i],hi[i])-max(beam_bounds[0][i],lo[i]) for i in range(3)]
        assert not all(v>1e-6 for v in overlap),('beam intersects floor collider',obj.name,overlap)
        floor_clearance[obj.name]={'signed_overlap_xyz_source_m':overlap,'positive_volume_overlap':False}
visual_pocket_checks={}
for side,sign in [('left',-1),('right',1)]:
    body=bpy.data.objects['floor_'+side+'_body'];inv=body.matrix_world.inverted()
    hit,point,normal,index=body.ray_cast(inv@Vector((sign*1.32,0,.15)),inv.to_3x3()@Vector((0,0,-1)))
    assert hit and (body.matrix_world@point).z<-.249
    visual_pocket_checks[side]=list(body.matrix_world@point)
for o in coll.objects:o.hide_render=True;o.hide_set(True)
scene.render.use_motion_blur=False
assert not any(o.data.dof.use_dof for o in bpy.data.objects if o.type=='CAMERA')
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(path))
report={'source_reopened':'passed','visible_triangles':triangles,'nonunit_mesh_scales':scales,
 'beam_independent_root':True,'gate_parent':'upper_chute','neutral_pose':'landed beam; hinge rotation zero',
 'packed_palette':bool(image.packed_file),'depth_of_field':False,'motion_blur':False,
 'nominal_landed_beam_floor_clearance':floor_clearance,'visual_pocket_floor_ray_hits_source':visual_pocket_checks,
 'colliders_hidden_for_render':all(o.hide_render for o in coll.objects),'game_implementation_included':False}
(BASE/'Validation/workshop-source-validation.json').write_text(json.dumps(report,indent=2))
print('WORKSHOP_SOURCE_FINALIZED',triangles,flush=True)
