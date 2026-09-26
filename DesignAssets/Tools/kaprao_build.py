"""Rebuild original Kaprao asset with Blender 5.2.2: blender -b -t 6 --python kaprao_build.py.
No third-party meshes, textures, or downloads. Geometry authored in meters, +X forward, +Z up.
"""
import bpy, math, json, os, sys
from pathlib import Path
from mathutils import Vector, Quaternion

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'Source/Kaprao'
EXPORT = ROOT / 'Exports/Kaprao'
PREVIEW = ROOT / 'Previews/Kaprao'
TEXTURES = ROOT / 'Textures/Kaprao'
VALIDATION = ROOT / 'Validation'
for p in (SOURCE,EXPORT,PREVIEW,TEXTURES,VALIDATION): p.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for d in list(bpy.data.materials): bpy.data.materials.remove(d)
scene = bpy.context.scene
scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=1
scene.render.fps=30

def collection(name):
    c=bpy.data.collections.new(name); scene.collection.children.link(c); return c
MODEL=collection('KAPRAO • original character')
ACCESSORY=collection('OPTIONAL • removable RGB sunglasses')
PROXY=collection('COLLISION • guides only — excluded from exchange')
STUDIO=collection('STUDIO • excluded from exchange')

def move(o,c):
    for oc in list(o.users_collection): oc.objects.unlink(o)
    c.objects.link(o)

def lin(v): return v/12.92 if v<.04045 else ((v+.055)/1.055)**2.4
def rgb(h): return tuple(lin(int(h[i:i+2],16)/255) for i in (0,2,4))
mats={}
palette=[('Coat_Honey','C77E31',.73),('Coat_Sunlit','E19A43',.72),('Cream','FFF0D4',.80),('Cream_Shadow','EAD4AC',.8),('Ear_Rose','D69C92',.75),('Ink','2C2526',.31),('Eye_Espresso','271F1A',.12),('Tongue','E78F99',.56),('Scarf_Teal','237E87',.62),('Scarf_Light','61BAB3',.59),('Nose','332B2C',.3),('RGB_Cyan','65DAE0',.28),('RGB_Pink','EE98CA',.28),('RGB_Amber','F7D071',.28)]
for name,h,rough in palette:
    m=bpy.data.materials.new(name);m.diffuse_color=(*rgb(h),1);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*rgb(h),1);p.inputs['Roughness'].default_value=rough
    if name.startswith('RGB_'):
        p.inputs['Emission Color'].default_value=(*rgb(h),1);p.inputs['Emission Strength'].default_value=.3
    mats[name]=m
lens=bpy.data.materials.new('Lens_Dark_Smoke');lens.use_nodes=True;lens.diffuse_color=(*rgb('223942'),1)
lp=lens.node_tree.nodes.get('Principled BSDF');lp.inputs['Base Color'].default_value=(*rgb('223942'),1);lp.inputs['Alpha'].default_value=1;lp.inputs['Roughness'].default_value=.39;lp.inputs['Specular IOR Level'].default_value=.18
mats[lens.name]=lens

parts=[];glass=[]
def finish(o,name,mat,bone='body',col=MODEL):
    o.name=name;move(o,col)
    if mat:o.data.materials.append(mats[mat])
    if o.type=='MESH':
        for p in o.data.polygons:p.use_smooth=True
        if bone:
            vg=o.vertex_groups.new(name=bone);vg.add(list(range(len(o.data.vertices))),1,'REPLACE')
    (glass if col==ACCESSORY else parts).append(o)
    return o

def uv(name,loc,scale,mat,bone='body',seg=24,rings=14,col=MODEL,rot=None):
    if seg<28:seg=max(12,round(seg*.88));rings=max(8,round(rings*.88))
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=rings,location=loc)
    o=bpy.context.object;o.scale=scale
    if rot:o.rotation_euler=rot
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    return finish(o,name,mat,bone,col)

def mesh(name,vs,fs,mat,bone='body',col=MODEL,sub=0):
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update()
    o=bpy.data.objects.new(name,me);col.objects.link(o)
    if sub:
        bpy.context.view_layer.objects.active=o;o.select_set(True)
        mod=o.modifiers.new('Rounded sculpted silhouette','SUBSURF');mod.levels=sub
        bpy.ops.object.modifier_apply(modifier=mod.name);o.select_set(False)
    return finish(o,name,mat,bone,col)

def tuft(name,base,tip,width,depth,mat='Cream',bone='body'):
    # Organic tapered lobes; broad crown disappears inside the underlying ruff.
    direction=Vector(tip)-Vector(base);direction.normalize()
    u=direction.cross(Vector((1,0,0)))
    if u.length<.01:u=direction.cross(Vector((0,1,0)))
    u.normalize();v=direction.cross(u).normalized()
    vs=[];fs=[];n=12
    profile=[(0,.24),(.12,.75),(.32,1),(.52,.90),(.73,.62),(.90,.28),(1,.01)]
    for t,r in profile:
        c=Vector(base).lerp(Vector(tip),t)
        for i in range(n):
            a=2*math.pi*i/n;vs.append(c+u*math.cos(a)*width*r+v*math.sin(a)*depth*r)
    for j in range(len(profile)-1):
        for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    fs += [tuple(reversed(range(n))),tuple((len(profile)-1)*n+i for i in range(n))]
    return mesh(name,vs,fs,mat,bone)

def curve(name,points,radius,mat,bone='head',col=MODEL):
    cv=bpy.data.curves.new(name,'CURVE');cv.dimensions='3D';cv.resolution_u=2;cv.bevel_depth=radius;cv.bevel_resolution=1
    sp=cv.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
    for bp,co in zip(sp.bezier_points,points):bp.co=co;bp.handle_left_type='AUTO';bp.handle_right_type='AUTO'
    o=bpy.data.objects.new(name,cv);col.objects.link(o);bpy.context.view_layer.objects.active=o
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.ops.object.convert(target='MESH')
    return finish(bpy.context.object,name,mat,bone,col)

# Main body: low, long and very soft, with generous chest and haunches.
uv('long orange body',(-.115,0,.383),(.456,.260,.300),'Coat_Sunlit',seg=32,rings=20)
uv('full cream chest ruff',(.218,0,.432),(.244,.277,.314),'Cream',seg=32,rings=20)

for side in (-1,1):
    sy=side
    uv('rounded hind haunch '+str(side),(-.388,sy*.173,.299),(.191,.132,.196),'Coat_Honey',bone='leg_back_'+str(side),seg=24,rings=14)
    for front,x in [(True,.238),(False,-.398)]:
        b=('leg_front_' if front else 'leg_back_')+str(side)
        uv('short ankle '+b,(x,sy*.177,.145),(.080,.083,.128),'Cream' if front else 'Coat_Sunlit',b,seg=20,rings=12)
        uv('soft white paw '+b,(x+.043,sy*.177,.062),(.115,.09,.062),'Cream',b,seg=20,rings=12)
        for k in (-1,0,1):
            uv('paw toe '+b+' '+str(k),(x+.112,sy*.177+k*.043,.053),(.042,.023,.037),'Cream',b,seg=12,rings=8)

# The head intentionally dominates. The user's dog has big cream cheeks and a clear white blaze.
# The blaze is assigned directly to the sphere surface, with its edges built into
# the latitude rings. There is no raised white plate or separate decal geometry.
vs=[];fs=[];nr=28;ns=32
for i in range(nr+1):
    phi=-math.pi/2+.006+(math.pi-.012)*i/nr;z=.747+.251*math.sin(phi);ry=.26*math.cos(phi);rx=.273*math.cos(phi)
    if z>.97:w=.008
    elif z>.94:w=.020
    elif z>.88:w=.034
    elif z>.82:w=.041
    else:w=.058
    a=math.asin(min(.90,w/max(.001,ry)))
    for j in range(ns):
        theta=(-a+2*a*j/4) if j<4 else (a+(math.tau-2*a)*(j-4)/(ns-4))
        vs.append((.386+rx*math.cos(theta),ry*math.sin(theta),z))
for i in range(nr):
    for j in range(ns):fs.append((i*ns+j,i*ns+(j+1)%ns,(i+1)*ns+(j+1)%ns,(i+1)*ns+j))
fs+=[tuple(reversed(range(ns))),tuple(nr*ns+j for j in range(ns))]
head=mesh('round head with integrated white blaze',vs,fs,'Coat_Sunlit','head');head.data.materials.append(mats['Cream'])
for i in range(nr):
    z=(vs[i*ns][2]+vs[(i+1)*ns][2])*.5
    if .746<z<.978:
        for j in range(4):head.data.polygons[i*ns+j].material_index=1
uv('white face bib',(.493,0,.691),(.208,.23,.179),'Cream','head',seg=28,rings=16)
for side in (-1,1):
    uv('fluffy cream cheek '+str(side),(.421,side*.205,.665),(.171,.11,.148),'Cream','head',seg=24,rings=14)
    for j in range(3):
        tuft('cheek side tuft '+str(side)+' '+str(j),(.398-j*.038,side*(.18+j*.008),.745-j*.054),(.339-j*.042,side*(.294+j*.006),.66-j*.062),.07,.048,'Cream','head')

# Rounded triangular ears: curved outline with convex front/back surfaces.
for side in (-1,1):
    b='ear_'+str(side)
    def ear_shape(name,inset,material):
        # Sample a softly rounded triangular perimeter via quadratic corner arcs.
        triangle=[Vector((.106,.868)),Vector((.360,.902)),Vector((.368,1.196))]
        center=sum(triangle,Vector((0,0)))/3
        outline=[]
        for k,p in enumerate(triangle):
            a=p.lerp(triangle[(k-1)%3],.20);c=p.lerp(triangle[(k+1)%3],.20)
            for j in range(7):
                t=j/6;outline.append((1-t)**2*a+2*t*(1-t)*p+t*t*c)
        n=len(outline);vs=[];fs=[]
        shrink=.68 if inset else 1
        # Full ear shell and inset both sit on the same convex cap.
        for rr in (.03,.33,.66,1):
            for pt in outline:
                yz=center+(pt-center)*rr*shrink
                x=.298+.066*math.sqrt(max(0,1-(rr*shrink)**2))+(0.003 if inset else 0)
                vs.append((x,side*yz.x,yz.y))
        for r in range(3):
            for i in range(n):fs.append((r*n+i,r*n+(i+1)%n,(r+1)*n+(i+1)%n,(r+1)*n+i))
        fs.append(tuple(reversed(range(n))))
        if not inset:
            off=len(vs)
            for pt in outline:vs.append((.260,side*pt.x,pt.y))
            for i in range(n):fs.append((3*n+i,3*n+(i+1)%n,off+(i+1)%n,off+i))
            fs.append(tuple(range(off,off+n)))
        return mesh(name,vs,fs,material,b,sub=2)
    ear_shape('upright rounded ear '+str(side),False,'Coat_Honey')
    ear_shape('rose inner ear '+str(side),True,'Ear_Rose')

# Open smile sits behind two plump muzzle lobes.
uv('broad smiling mouth',(.66,0,.618),(.087,.15,.078),'Ink','head',seg=28,rings=16)
uv('white lower jaw',(.616,0,.57),(.095,.133,.048),'Cream','head',seg=24,rings=12)
uv('happy pink tongue',(.731,0,.6),(.025,.072,.063),'Tongue','head',seg=24,rings=14)
curve('tongue center crease',[(.755,0,.632),(.758,0,.610),(.754,0,.59)],.0022,'Ear_Rose','head')
for side in (-1,1):
    uv('smile corner '+str(side),(.624,side*.13,.657),(.049,.033,.052),'Ink','head',seg=16,rings=10)
    uv('muzzle cushion '+str(side),(.67,side*.079,.708),(.13,.102,.078),'Cream','head',seg=28,rings=16)
    uv('little tooth '+str(side),(.699,side*.099,.65),(.014,.014,.024),'Cream','head',seg=12,rings=8)
uv('velvet triangular nose',(.788,0,.749),(.049,.061,.043),'Nose','head',seg=24,rings=14)
uv('nose soft shine',(.829,-.016,.769),(.004,.018,.006),'Cream_Shadow','head',seg=12,rings=8)
curve('philtrum',[(.794,0,.72),(.787,0,.700),(.776,0,.687)],.0045,'Nose','head')

for side in (-1,1):
    # Recessed espresso eyes with a warm eyelid and small white catchlights.
    uv('warm eye socket '+str(side),(.595,side*.137,.823),(.037,.067,.070),'Coat_Honey','head',seg=24,rings=14)
    uv('expressive eye '+str(side),(.622,side*.137,.829),(.027,.044,.052),'Eye_Espresso','head',seg=24,rings=16)
    uv('big eye catchlight '+str(side),(.646,side*.126,.848),(.007,.012,.014),'Cream','head',seg=12,rings=8)
    uv('tiny eye catchlight '+str(side),(.648,side*.155,.814),(.004,.006,.006),'Cream','head',seg=10,rings=6)
    uv('cream eyebrow '+str(side),(.592,side*.135,.89),(.020,.050,.017),'Cream','head',seg=20,rings=10,rot=(side*.12,0,0))

# Broad layered ruff lobes follow the silhouette, rather than a hair system.
for ring in range(2):
    for j in range(9):
        angle=(-.96+j/8*1.92)*math.pi/2
        y=math.sin(angle)*(.220+ring*.016)
        x=.31+math.cos(angle)*(.100-ring*.027)
        z=.485-ring*.106
        tuft('ruff scallop %d %d'%(ring,j),(x-.055,y*.85,z+.095),(x+.016,y*1.09,z-.115),.066,.042,'Cream')
for side in (-1,1):
    for j in range(3):
        tuft('orange shoulder tuft '+str(side)+' '+str(j),(.12-j*.11,side*.206,.45),(.058-j*.118,side*.271,.347),.058,.037,'Coat_Sunlit')
uv('corgi tiny tail',(-.584,0,.414),(.087,.082,.096),'Coat_Sunlit','tail',seg=20,rings=12)
uv('cream tail tip',(-.625,0,.448),(.049,.060,.058),'Cream','tail',seg=16,rings=10)

# Teal neckerchief is a narrow collar band with a soft triangular front fold.
# Curve rests on the upper chest; the lower cream ruff remains visible.
points=[]
for j in range(13):
    a=2*math.pi*j/12;points.append((.216+.245*math.cos(a),.270*math.sin(a),.542+.013*math.cos(a)))
curve('soft teal scarf collar',points,.033,'Scarf_Teal','body')
vs=[];fs=[]
for i in range(8):
    t=i/7;w=.24*(1-t)+.006;z=.558-.224*t
    for j in range(15):
        y=(j/14*2-1)*w;vs.append((.508-.95*y*y+.01*math.sin(t*math.pi),y,z+.018*(abs(y)/.246)))
for i in range(7):
    for j in range(14):a=i*15+j;fs.append((a,a+1,a+16,a+15))
scarf=mesh('scarf broad front fold',vs,fs,'Scarf_Teal','body',sub=1)
mod=scarf.modifiers.new('Soft fabric thickness','SOLIDIFY');mod.thickness=.009;bpy.context.view_layer.objects.active=scarf;bpy.ops.object.modifier_apply(modifier=mod.name)
curve('scarf stitched top edge',[(.48,-.14,.542),(.513,0,.538),(.48,.14,.542)],.003,'Scarf_Light','body')
uv('scarf embroidered paw pad',(.533,-.048,.438),(.004,.017,.015),'Cream','body',seg=16,rings=8)
for y,z in [(-.069,.457),(-.051,.467),(-.034,.461)]:uv('scarf embroidered toe '+str(y),(.532,y,z),(.004,.006,.008),'Cream','body',seg=12,rings=8)
uv('scarf knot',(.31,-.264,.542),(.056,.047,.05),'Scarf_Teal','body',seg=20,rings=12)
tuft('scarf side end',(.294,-.263,.544),(.21,-.294,.407),.05,.021,'Scarf_Teal','body')
tuft('scarf short end',(.318,-.263,.544),(.352,-.315,.456),.035,.02,'Scarf_Light','body')

# Optional small rounded frames and very light smoky lenses keep the eyes legible.
for side in (-1,1):
    cy=side*.137;cx=.799;cz=.794
    outline=[]
    for k in range(25):
        a=2*math.pi*k/24
        outline.append((cx,cy+.070*math.copysign(abs(math.cos(a))**.55,math.cos(a)),cz+.032*math.copysign(abs(math.sin(a))**.55,math.sin(a))))
    curve('dark sunglasses rim '+str(side),outline,.009,'Ink','head',ACCESSORY)
    # separate inner lens surface, low-alpha and easy to remove as a single mesh
    vs=[(cx-.001,cy,cz)]+outline[:-1];fs=[(0,i+1,(i+1)%24+1) for i in range(24)]
    mesh('smoky translucent lens '+str(side),vs,fs,lens.name,'head',ACCESSORY)
    for a0,a1,mat in [(0,math.pi*.70,'RGB_Cyan'),(math.pi*.70,math.pi*1.38,'RGB_Pink'),(math.pi*1.38,math.pi*2,'RGB_Amber')]:
        pp=[]
        for k in range(9):
            a=a0+(a1-a0)*k/8;pp.append((cx+.012,cy+.070*math.copysign(abs(math.cos(a))**.55,math.cos(a)),cz+.032*math.copysign(abs(math.sin(a))**.55,math.sin(a))))
        curve('subtle frame edge '+mat+' '+str(side),pp,.0022,mat,'head',ACCESSORY)
    curve('sunglasses arm '+str(side),[(.799,side*.204,.816),(.555,side*.244,.819),(.424,side*.246,.831)],.006,'Ink','head',ACCESSORY)
curve('sunglasses bridge',[(.799,-.067,.811),(.824,0,.819),(.799,.067,.811)],.0065,'Ink','head',ACCESSORY)

# Fuse intersecting cream lobes into smooth, continuous sculpted surfaces.
def sculpt_union(prefixes,name,bone):
    objs=[o for o in parts if any(o.name.startswith(p) for p in prefixes)]
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:o.select_set(True);parts.remove(o)
    bpy.context.view_layer.objects.active=objs[0];bpy.ops.object.join();o=bpy.context.object;o.name=name
    mod=o.modifiers.new('Sculpted lobe union','REMESH');mod.mode='VOXEL';mod.voxel_size=.007;mod.use_smooth_shade=True
    bpy.ops.object.modifier_apply(modifier=mod.name)
    mod=o.modifiers.new('Gentle clay smoothing','SMOOTH');mod.factor=.7;mod.iterations=4;bpy.ops.object.modifier_apply(modifier=mod.name)
    o.data.calc_loop_triangles();target=3400 if bone=='head' else 2800
    mod=o.modifiers.new('Sculpted surface optimization','DECIMATE');mod.ratio=min(1,target/len(o.data.loop_triangles));mod.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=mod.name)
    o.vertex_groups.clear();vg=o.vertex_groups.new(name=bone);vg.add(list(range(len(o.data.vertices))),1,'REPLACE')
    parts.append(o)
sculpt_union(['white face bib','fluffy cream cheek','cheek side tuft','muzzle cushion','white lower jaw'],'sculpted cream face','head')
sculpt_union(['full cream chest ruff','ruff scallop'],'sculpted layered chest','body')

# Single armature: islands receive rigid 1.0 weights for a compact, predictable first-demo skin.
bpy.ops.object.select_all(action='DESELECT')
armdata=bpy.data.armatures.new('Kaprao_Rig');rig=bpy.data.objects.new('Kaprao_Rig',armdata);MODEL.objects.link(rig)
bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
bone_defs=[('root',(0,0,0),None),('body',(0,0,.35),'root'),('head',(.235,0,.64),'body'),('tail',(-.49,0,.41),'body')]
for side in (-1,1):
    bone_defs.extend([('leg_front_'+str(side),(.22,side*.177,.255),'body'),('leg_back_'+str(side),(-.376,side*.177,.28),'body'),('ear_'+str(side),(.29,side*.197,.92),'head')])
for name,co,parent in bone_defs:
    b=armdata.edit_bones.new(name);b.head=co;b.tail=Vector(co)+Vector((0,0,.12))
    if parent:b.parent=armdata.edit_bones[parent]
bpy.ops.object.mode_set(mode='OBJECT');rig.show_in_front=True

def join_skinned(objs,name):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:o.select_set(True)
    bpy.context.view_layer.objects.active=objs[0];bpy.ops.object.join();o=bpy.context.object;o.name=name
    # Place object origins at the world origin; make mesh and armature transforms identity.
    scene.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    # Recalculate all normals after unions and cap construction.
    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT')
    o.data.calc_loop_triangles();target=18000 if name=='Kaprao_Body_Skinned' else 1900
    if len(o.data.loop_triangles)>target:
        mod=o.modifiers.new('Measured mobile geometry budget','DECIMATE');mod.ratio=target/len(o.data.loop_triangles);mod.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=mod.name)
    o.parent=rig;mod=o.modifiers.new('Kaprao weighted skin','ARMATURE');mod.object=rig
    return o
hero=join_skinned(parts,'Kaprao_Body_Skinned')
glasses=join_skinned(glass,'Kaprao_RGB_Sunglasses_REMOVABLE')
glasses['removable']=True;glasses['detach_instructions']='Hide/delete this mesh node. It shares the Kaprao head joint.'
rig['character']='Kaprao, inspired by the user-supplied orange and cream corgi photograph'
rig['forward_axis']='+X';rig['up_axis_blender']='+Z';rig['up_axis_glb']='+Y';rig['units']='meters';rig['skin_method']='rigid weighted islands; smooth-shaded geometric character; no cloth or fur simulation'

def pose_reset():
    for b in rig.pose.bones:
        b.rotation_mode='XYZ';b.rotation_euler=(0,0,0);b.location=(0,0,0);b.scale=(1,1,1)
def pose_euler(name,xyz):
    # Input angles about world X,Y,Z. Convert to the bone's rest local basis.
    from mathutils import Euler
    bone=rig.pose.bones[name];R=bone.bone.matrix_local.to_quaternion();world=Euler(xyz,'XYZ').to_quaternion()
    bone.rotation_euler=(R.inverted() @ world @ R).to_euler('XYZ')
def pose_worldloc(name,xyz):
    bone=rig.pose.bones[name];bone.location=bone.bone.matrix_local.to_quaternion().inverted() @ Vector(xyz)

clips=[('Idle_Look',121,True),('Walk_InPlace',25,True),('Jump_Fall',37,False),('Celebrate',61,False)]
rig.animation_data_create()
for name,end,loop in clips:
    rig.animation_data.action=None
    action=bpy.data.actions.new(name);action.use_fake_user=True;rig.animation_data.action=action
    action['loop']=loop;action['root_motion']=False;action['notes']='In-place character art only; runtime controller owns world trajectory.'
    for f in range(1,end+1,2):
        t=(f-1)/(end-1);pose_reset()
        if name=='Idle_Look':
            pose_worldloc('body',(0,0,.006*math.sin(t*math.tau)))
            pose_euler('head',(0,.018*math.sin(t*math.tau),.10*math.sin(t*math.tau)))
            pose_euler('tail',(.10*math.sin(t*math.tau*3),0,0))
            for side in (-1,1):pose_euler('ear_'+str(side),(.028*side*math.sin(t*math.tau),0,0))
        elif name=='Walk_InPlace':
            pose_worldloc('body',(0,0,.012*(1-math.cos(t*math.tau*2))))
            pose_euler('head',(0,.026*math.sin(t*math.tau*2),0))
            for side in (-1,1):
                for front in (True,False):
                    phase=0 if ((side==1)==front) else math.pi
                    a=.29*math.sin(t*math.tau+phase)
                    pose_euler(('leg_front_' if front else 'leg_back_')+str(side),(0,a,0))
            pose_euler('tail',(.13*math.sin(t*math.tau*2),0,0))
        elif name=='Jump_Fall':
            # Art pose clip only: no root translation and no simulated physical trajectory.
            crouch=math.sin(min(t/.22,1)*math.pi) if t<.22 else 0
            airborne=math.sin(max(0,min(1,(t-.16)/.84))*math.pi)
            pose_worldloc('body',(0,0,-.035*crouch))
            pose_euler('body',(0,-.08*airborne,0));pose_euler('head',(0,-.10*airborne,0))
            for side in (-1,1):
                pose_euler('leg_front_'+str(side),(0,-.52*airborne,0));pose_euler('leg_back_'+str(side),(0,.42*airborne,0))
                pose_euler('ear_'+str(side),(0,-.12*airborne,0))
        else:
            env=math.sin(t*math.pi)
            pose_worldloc('body',(0,0,.06*env*abs(math.sin(t*math.tau*2))))
            pose_euler('head',(.10*env*math.sin(t*math.tau*2),-.055*env,.13*env*math.sin(t*math.tau*2)))
            pose_euler('tail',(.35*env*math.sin(t*math.tau*6),0,0))
            for side in (-1,1):
                pose_euler('leg_front_'+str(side),(0,.20*env*math.sin(t*math.tau*2+side),0))
                pose_euler('ear_'+str(side),(.10*side*env*math.sin(t*math.tau*2),0,0))
        for b in rig.pose.bones:
            for dp in ('location','rotation_euler','scale'):b.keyframe_insert(data_path=dp,frame=f,group=b.name)
    # Keep actions discoverable and separate. Muted NLA tracks prevent simultaneous playback.
    track=rig.animation_data.nla_tracks.new();track.name=name;track.mute=True
    strip=track.strips.new(name,1,action)
    if hasattr(strip,'action_slot') and action.slots:strip.action_slot=action.slots[0]
rig.animation_data.action=None;pose_reset();scene.frame_set(1)

# Guide collider: no armature and not exported. Red wire capsule-like ellipsoid.
bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,location=(0,0,.35));proxy=bpy.context.object
proxy.name='COL_corgi';proxy.scale=(.52,.245,.35);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
move(proxy,PROXY);proxy.display_type='WIRE';proxy.hide_render=True;proxy.hide_set(True)
proxy['usage']='Reference dimensions only. Build runtime primitive controller separately.'
marker=bpy.data.objects.new('FORWARD_+X • route direction',None);PROXY.objects.link(marker);marker.empty_display_type='SINGLE_ARROW';marker.rotation_euler=(0,math.pi/2,0);marker.empty_display_size=.6;marker.hide_render=True;marker.hide_set(True)

# Warm neutral studio, intentionally excluded from exchange exports.
floor_mat=bpy.data.materials.new('STUDIO warm ivory');floor_mat.diffuse_color=(*rgb('ECE3D5'),1);floor_mat.use_nodes=True;floor_mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*rgb('ECE3D5'),1);floor_mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.84
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.006));floor=bpy.context.object;floor.name='STUDIO floor';move(floor,STUDIO);floor.data.materials.append(floor_mat)
world=bpy.data.worlds.new('Warm studio');scene.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(*rgb('ECE7DE'),1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35
def area(name,co,power,size,color):
    data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size;data.color=rgb(color)
    o=bpy.data.objects.new(name,data);STUDIO.objects.link(o);o.location=co;o.rotation_euler=(Vector((0,0,.55))-o.location).to_track_quat('-Z','Y').to_euler()
area('STUDIO large softbox',(2.5,-3.2,4.1),360,3.6,'FFF5E6');area('STUDIO fill',(1.5,3,2.8),210,3,'E6F2FF');area('STUDIO rim',(-2,1.5,3),320,2.8,'FFF2D8')
camdata=bpy.data.cameras.new('Kaprao showcase camera');cam=bpy.data.objects.new('Kaprao showcase camera',camdata);STUDIO.objects.link(cam);scene.camera=cam;camdata.type='ORTHO';camdata.ortho_scale=1.7;camdata.lens=50;camdata.dof.use_dof=False
def camera(co,target=(.04,0,.59),scale=1.7):
    cam.location=co;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();camdata.ortho_scale=scale
camera((3.6,-3.2,2.0))
scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True
scene.render.resolution_x=1400;scene.render.resolution_y=1400;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
scene.render.use_file_extension=True
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=-.5
if hasattr(scene.render,'use_motion_blur'):scene.render.use_motion_blur=False
scene['presentation']='No depth of field, no motion blur. Solid base-color PBR; generated geometry only.'

# Palette reference (materials do not rely on textures or external files).
img=bpy.data.images.new('Kaprao palette • reference only',width=256,height=16,alpha=True)
colors=[rgb(h) for n,h,r in palette]+[rgb('396C79')];pix=[]
for y in range(16):
    for x in range(256):pix.extend((*colors[min(len(colors)-1,x*len(colors)//256)],1))
img.pixels=pix;img.filepath_raw=str(TEXTURES/'kaprao-palette.png');img.file_format='PNG';img.save();img.pack()

# Measured source geometry and skin checks.
def metrics(o):
    o.data.calc_loop_triangles()
    return {'name':o.name,'vertices':len(o.data.vertices),'triangles':len(o.data.loop_triangles),'materials':[m.name for m in o.data.materials], 'bounds_blender_m':[[round(min((o.matrix_world@v.co)[i] for v in o.data.vertices),5) for i in range(3)],[round(max((o.matrix_world@v.co)[i] for v in o.data.vertices),5) for i in range(3)]], 'weighted_vertices':sum(bool(v.groups) for v in o.data.vertices),'smooth_faces':sum(p.use_smooth for p in o.data.polygons),'faces':len(o.data.polygons)}
manifest={'asset':'Kaprao','authoring':'Original procedural geometry authored for the user; photo reference supplied by user. No external asset dependencies.','units':'meters','coordinate_conversion':'Blender Z-up, +X forward. GLB Y-up, +X forward: (X,Y,Z)_Blender -> (X,Z,-Y)_GLB. USD explicitly exported Y-up.','source_version':bpy.app.version_string,'meshes':[metrics(hero),metrics(glasses)],'bones':[b.name for b in armdata.bones],'skin':'True glTF skin; disconnected smooth geometric islands with 1.0 rigid bone weights. No fur/cloth simulation; no organic bend deformation.','animations':[{'name':n,'frames':[1,e],'fps':30,'duration_seconds':(e-1)/30,'loop':loop,'root_motion':False} for n,e,loop in clips],'optional_accessory':glasses.name,'collider':{'name':proxy.name,'exported':False,'dimensions_m':list(proxy.dimensions),'purpose':'guide only'},'materials':[{'name':n,'base_color_srgb':'#'+h,'roughness':r} for n,h,r in palette]+[{'name':lens.name,'base_color_srgb':'#223942','alpha':1.0,'roughness':.39}],'textures':'No texture dependency. Palette PNG reference only.','tested':'Blender source construction/export, exported GLB validation handled separately; no Duo runtime import claim.'}
manifest['rendered_triangles_total']=sum(m['triangles'] for m in manifest['meshes'])
(VALIDATION/'kaprao-manifest.json').write_text(json.dumps(manifest,indent=2))

def select_export():
    bpy.ops.object.select_all(action='DESELECT')
    for o in (rig,hero,glasses):o.hide_set(False);o.select_set(True)
    bpy.context.view_layer.objects.active=rig
select_export()
bpy.ops.export_scene.gltf(filepath=str(EXPORT/'kaprao.glb'),export_format='GLB',use_selection=True,export_yup=True,export_animations=True,export_animation_mode='ACTIONS',export_force_sampling=True,export_anim_single_armature=True,export_skins=True,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_materials='EXPORT')

# USD is a static Y-up exchange fallback; GLB is authoritative for named clips.
try:
    bpy.ops.wm.usd_export(filepath=str(EXPORT/'kaprao-static.usdc'),selected_objects_only=True,export_animation=False,export_materials=True,export_armatures=True,convert_orientation=True,export_global_forward_selection='NEGATIVE_Z',export_global_up_selection='Y',convert_world_material=False)
    manifest['usd']='Static Y-up USDC with materials and rest rig; no named animation clips. See GLB for four clips.'
except Exception as e:manifest['usd']='USD export failed: '+str(e)
(VALIDATION/'kaprao-manifest.json').write_text(json.dumps(manifest,indent=2))

# Save editable source with neutral pose, organized collections, inactive clips ready to choose.
scene.frame_start=1;scene.frame_end=121
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE/'kaprao.blend'))

def render(name,co,scale=1.7,res=1200):
    camera(co,scale=scale);scene.render.resolution_x=res;scene.render.resolution_y=res;scene.render.filepath=str(PREVIEW/name);bpy.ops.render.render(write_still=True)
render('kaprao-hero.png',(3.6,-3.2,2.0),1.64,1400)
glasses.hide_render=True
render('kaprao-unadorned.png',(3.6,-3.2,2.0),1.64,1400)
for name,co in [('front',(4,0,1.05)),('left',(0,-4,1.05)),('rear',(-4,0,1.05)),('right',(0,4,1.05))]:render('kaprao-'+name+'.png',co,1.5,900)
glasses.hide_render=False
camera((3.6,-3.2,2.0),scale=1.64)
scene.render.resolution_x=1400;scene.render.resolution_y=1400
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE/'kaprao.blend'))
print('KAPRAO_BUILD_COMPLETE',json.dumps({'triangles':manifest['rendered_triangles_total'],'usd':manifest.get('usd')}))
