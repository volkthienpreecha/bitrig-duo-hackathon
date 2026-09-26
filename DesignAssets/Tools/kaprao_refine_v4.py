"""Refine the approved Rodin reconstruction; no replacement primitive anatomy.
Blender source uses metres, +X forward, Z up. Exports use Y up.
"""
import bpy, math, random, json, bisect
from pathlib import Path
from mathutils import Vector, Euler, Matrix

ROOT=Path(__file__).resolve().parents[1]/'Revisions/Kaprao-v4'
for p in ('Source/Kaprao','Previews','Textures/Kaprao','Exports/Kaprao','Validation'):(ROOT/p).mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(ROOT/'Source/Incoming/kaprao-rodin-original.glb'))
hero=next(o for o in bpy.context.scene.objects if o.type=='MESH')
hero.name='Kaprao_Body_Skinned'
bpy.context.view_layer.objects.active=hero
hero.matrix_world=Matrix.Rotation(math.pi/2,4,'Z') @ hero.matrix_world
hero.scale*=.68
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
bottom=min(v.co.z for v in hero.data.vertices)
for v in hero.data.vertices:v.co.z-=bottom
hero.data.update()
hero.data.calc_loop_triangles()
mod=hero.modifiers.new('Mobile mesh, preserve UV texture','DECIMATE');mod.ratio=48000/len(hero.data.loop_triangles);mod.use_collapse_triangulate=True
bpy.ops.object.modifier_apply(modifier=mod.name)
for p in hero.data.polygons:p.use_smooth=True
for mat in hero.data.materials:
    mat.name='Kaprao_Coat_Scarf_PBR'
    for n in mat.node_tree.nodes:
        if n.type=='BSDF_PRINCIPLED':n.inputs['Specular IOR Level'].default_value=.22
for im in bpy.data.images:
    if im.packed_file:
        im.filepath_raw=str(ROOT/'Textures/Kaprao'/(im.name+'.png'));im.file_format='PNG';im.save();im.pack()

def material(name,color,rough=.65,emission=0):
    m=bpy.data.materials.new(name);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough
    p.inputs['Specular IOR Level'].default_value=.22
    if emission:p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=emission
    return m
ink=material('Frames_graphite',(.012,.016,.022),.3)
lens=material('Lenses_smoked_teal',(.008,.013,.017),.23)
cyan=material('RGB_cyan',(.06,.75,1),.3,2.0)
pink=material('RGB_magenta',(.85,.035,.35),.3,2.0)
amber=material('RGB_amber',(1,.35,.025),.3,1.8)

def make_mesh(name,vs,fs,mats):
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update()
    o=bpy.data.objects.new(name,me);bpy.context.scene.collection.objects.link(o)
    for m in mats:me.materials.append(m)
    for p in me.polygons:p.use_smooth=True
    return o

# Sculpted cheek/chest tufts are part of the reconstructed mesh; no strand ribbons.
glassparts=[]
def tube(name,points,radius,mat):
    cv=bpy.data.curves.new(name,'CURVE');cv.dimensions='3D';cv.resolution_u=3;cv.bevel_depth=radius;cv.bevel_resolution=2
    sp=cv.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
    for bp,co in zip(sp.bezier_points,points):bp.co=co;bp.handle_left_type='AUTO';bp.handle_right_type='AUTO'
    o=bpy.data.objects.new(name,cv);bpy.context.scene.collection.objects.link(o);cv.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.convert(target='MESH')
    glassparts.append(bpy.context.object)
def facepoint(y,z,offset=0):return (.688-1.60*y*y+offset,y,z)
for sign in (-1,1):
    outline=[(.048,.961),(.082,.998),(.242,1.005),(.281,.985),(.260,.909),(.09,.913)]
    points=[facepoint(sign*y,z) for y,z in outline]
    tube('Fitted graphite rim',points+[points[0]],.007,ink)
    o=make_mesh('Smoked lens',[(x-.004,y,z) for x,y,z in points],[(0,1,2,3,4,5)],[lens]);glassparts.append(o)
    tube('Temple arm',[(.572,sign*.277,.984),(.46,sign*.292,.99),(.30,sign*.277,.975)],.009,ink)
    tube('Cyan lower edge',[facepoint(sign*.259,.92,.006),facepoint(sign*.244,.911,.006),facepoint(sign*.198,.912,.006)],.0028,cyan)
    tube('Magenta brow inlay',[facepoint(sign*.102,1.002,.006),facepoint(sign*.16,1.004,.006)],.0025,pink)
    tube('Amber outer accent',[facepoint(sign*.269,.985,.006),facepoint(sign*.264,.959,.006)],.0025,amber)
tube('Nose bridge',[facepoint(-.049,.968),(.705,0,.974),facepoint(.049,.968)],.006,ink)
bpy.ops.object.select_all(action='DESELECT')
for o in glassparts:o.select_set(True)
bpy.context.view_layer.objects.active=glassparts[0];bpy.ops.object.join();glasses=bpy.context.object;glasses.name='Kaprao_RGB_Sunglasses_REMOVABLE'
for v in glasses.data.vertices:
    v.co.x-=.065;v.co.y*=.92;v.co.z=.895+(v.co.z-.960)*.8
for p in glasses.data.polygons:p.use_smooth=True

# Smooth, normalized weights on the reconstructed continuous mesh.
arm=bpy.data.armatures.new('Kaprao_Rig');rig=bpy.data.objects.new('Kaprao_Rig',arm);bpy.context.scene.collection.objects.link(rig)
bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.mode_set(mode='EDIT')
defs=[('root',(0,0,0),(0,0,.15),None),('body',(-.15,0,.48),(.16,0,.54),'root'),('head',(.34,0,.78),(.59,0,.91),'body')]
for s in (-1,1):
    for kind,x in [('front',.43),('back',-.43)]:
        defs.extend([(f'leg_{kind}_{s}',(x,s*.23,.43),(x,s*.23,.18),'body'),(f'paw_{kind}_{s}',(x,s*.23,.18),(x+.07,s*.23,.07),f'leg_{kind}_{s}')])
for name,h,t,par in defs:
    bone=arm.edit_bones.new(name);bone.head=h;bone.tail=t
    if par:bone.parent=arm.edit_bones[par]
bpy.ops.object.mode_set(mode='OBJECT');rig.show_in_front=True
def smooth(a,b,v):
    t=max(0,min(1,(v-a)/(b-a)));return t*t*(3-2*t)
def weights(p):
    x,y,z=p;head=smooth(.64,.84,z)*smooth(.10,.31,x)
    leg=(1-smooth(.27,.52,z))*smooth(.04,.14,abs(y));leg*=1-head
    if x>0:kind='front';leg*=smooth(.15,.32,x)
    else:kind='back';leg*=1-smooth(-.42,-.23,x)
    paw=(1-smooth(.10,.23,z))*leg;side=1 if y>=0 else -1
    return {'head':head,'body':1-head-leg,f'leg_{kind}_{side}':leg-paw,f'paw_{kind}_{side}':paw}
for obj in (hero,glasses):
    groups={b.name:obj.vertex_groups.new(name=b.name) for b in arm.bones}
    for v in obj.data.vertices:
        w={'head':1} if obj==glasses else weights(v.co)
        for name,val in w.items():
            if val>1e-6:groups[name].add([v.index],val,'REPLACE')
    obj.parent=rig;mod=obj.modifiers.new('Smooth quadruped skin','ARMATURE');mod.object=rig

scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.render.fps=30
def reset():
    for b in rig.pose.bones:b.rotation_mode='QUATERNION';b.rotation_quaternion=(1,0,0,0);b.location=(0,0,0)
def rotate(name,xyz):
    b=rig.pose.bones[name];q=b.bone.matrix_local.to_quaternion();b.rotation_quaternion=q.inverted()@Euler(xyz).to_quaternion()@q
def shift(name,v):
    b=rig.pose.bones[name];b.location=b.bone.matrix_local.to_quaternion().inverted()@Vector(v)
clips=[('Idle_Look',121),('Walk_InPlace',25),('Jump_Fall',37),('Celebrate',61)]
rig.animation_data_create()
for name,end in clips:
    act=bpy.data.actions.new(name);rig.animation_data.action=act
    for frame in range(1,end+1,2):
        t=(frame-1)/(end-1);a=t*2*math.pi;reset()
        if name=='Idle_Look':
            shift('body',(0,0,.006*math.sin(a)));rotate('head',(0,.025*math.sin(a),.07*math.sin(a)))
        elif name=='Walk_InPlace':
            shift('body',(0,0,.012*(1-math.cos(2*a))));rotate('head',(0,.022*math.sin(2*a),0))
            for s in (-1,1):
                for kind,phase in [('front',0),('back',math.pi)]:
                    swing=.27*math.sin(a+phase+(math.pi if s<0 else 0));rotate(f'leg_{kind}_{s}',(0,swing,0));rotate(f'paw_{kind}_{s}',(0,-swing*.42,0))
        elif name=='Jump_Fall':
            k=math.sin(math.pi*t);rotate('body',(0,-.06*k,0));rotate('head',(0,.05*k,0))
            for s in (-1,1):rotate(f'leg_front_{s}',(0,-.30*k,0));rotate(f'leg_back_{s}',(0,.28*k,0))
        else:
            k=math.sin(math.pi*t)**2;shift('body',(0,0,.035*k));rotate('head',(.035*math.sin(2*a)*k,-.07*k,.10*math.sin(a)*k))
        for b in rig.pose.bones:
            b.keyframe_insert(data_path='rotation_quaternion',frame=frame,group=b.name);b.keyframe_insert(data_path='location',frame=frame,group=b.name)
    track=rig.animation_data.nla_tracks.new();track.name=name;strip=track.strips.new(name,1,act);track.mute=True
rig.animation_data.action=None;reset();scene.frame_set(1)
rig['source']='Rodin V2 reconstruction of user-directed Kaprao reference, refined in Blender'
rig['axis_contract']='meters; Blender Z-up/+X-forward; runtime Y-up/+X-forward'
glasses['removable']=True
bpy.ops.object.select_all(action='DESELECT')
for o in (rig,hero,glasses):o.select_set(True)
bpy.context.view_layer.objects.active=rig
scene.frame_start=1;scene.frame_end=121
# Keep the studio out of all runtime exports.
texture_sources=[]
(ROOT/'Exports/Kaprao/textures').mkdir(exist_ok=True)
for im in bpy.data.images:
    if im.packed_file and im.size[0]>1024:
        texture_sources.append((im,str(ROOT/'Textures/Kaprao'/(im.name+'.png'))))
        im.scale(1024,1024);im.pack()
        im.filepath_raw=str(ROOT/'Exports/Kaprao/textures'/(im.name+'.png'));im.save()
for tr in rig.animation_data.nla_tracks:tr.mute=False
bpy.ops.export_scene.gltf(filepath=str(ROOT/'Exports/Kaprao/kaprao.glb'),export_format='GLB',use_selection=True,export_yup=True,export_animations=True,export_animation_mode='NLA_TRACKS',export_nla_strips=True,export_force_sampling=True,export_skins=True)
for tr in rig.animation_data.nla_tracks:tr.mute=True
for name,end in [('static',1)]+clips:
    rig.animation_data.action=None if name=='static' else bpy.data.actions[name]
    if rig.animation_data.action and rig.animation_data.action.slots:rig.animation_data.action_slot=rig.animation_data.action.slots[0]
    reset();scene.frame_start=1;scene.frame_end=end;scene.frame_set(1)
    bpy.ops.wm.usd_export(filepath=str(ROOT/'Exports/Kaprao'/('kaprao-'+name+'.usdc')),selected_objects_only=True,export_animation=name!='static',export_materials=True,export_armatures=True,convert_orientation=True,export_global_forward_selection='NEGATIVE_Z',export_global_up_selection='Y',convert_world_material=False)
rig.animation_data.action=None;reset();scene.frame_set(1)
for im,path in texture_sources:
    im.filepath_raw=path;im.unpack(method='REMOVE');im.reload();im.pack()

scene.render.engine='CYCLES';scene.cycles.samples=48
scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.world.color=(.35,.32,.29);scene.view_settings.view_transform='Standard';scene.view_settings.exposure=-1.0
def aim(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
for name,loc,power,size in [('STUDIO_key',(3,-4,5),650,4),('STUDIO_fill',(2,3,3),350,3),('STUDIO_rim',(-3,2,4),500,3)]:
    bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,(0,0,.55))
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='STUDIO_camera';scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=1.85
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.008))
floor=bpy.context.object;floor.name='STUDIO_ground';floor.data.materials.append(material('STUDIO_warm_ivory',(.65,.57,.52),.85))
for name,loc in [('hero',(3,-4,2)),('front',(4,0,1)),('side',(0,-4,1)),('rear',(-4,0,1))]:
    cam.location=loc;aim(cam,(0,0,.58));scene.render.filepath=str(ROOT/'Previews'/('kaprao-'+name+'.png'));bpy.ops.render.render(write_still=True)
glasses.hide_render=True;cam.location=(3,-4,2);aim(cam,(0,0,.58));scene.render.filepath=str(ROOT/'Previews/kaprao-no-glasses.png');bpy.ops.render.render(write_still=True);glasses.hide_render=False
scene.frame_end=121
for o in (hero,glasses):o.data.calc_loop_triangles()
report={'meshes':{o.name:len(o.data.loop_triangles) for o in (hero,glasses)},'fur_ribbons':0,'bones':len(arm.bones),'clips':[n for n,e in clips],'status':'first refinement; review actual previews before acceptance'}
(ROOT/'Validation/refinement.json').write_text(json.dumps(report,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Source/Kaprao/kaprao.blend'))
print('V4_REFINED',json.dumps(report))
