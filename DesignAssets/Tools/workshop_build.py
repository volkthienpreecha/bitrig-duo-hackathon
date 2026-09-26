"""Reproducible original Fold & Fetch rooftop workshop art.
Run Blender 5.2+: blender -b --factory-startup --python workshop_build.py
Source: meters, Blender Z up. GLB and USD exports: Y up, +X route, +Z front.
The scene is a design kit, not a physics or simulator implementation.
"""
import bpy, math, os, json, random, argparse, sys
from mathutils import Vector, Matrix
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
SOURCE=BASE/'Source'/'Workshop'; EXPORT=BASE/'Exports'/'Workshop'
TEXTURE=BASE/'Textures'/'Workshop'; PREVIEW=BASE/'Previews'/'Workshop'; VALID=BASE/'Validation'
for p in [SOURCE,EXPORT,TEXTURE,PREVIEW,VALID]: p.mkdir(parents=True,exist_ok=True)
random.seed(25)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
    if c.name!='Collection': bpy.data.collections.remove(c)
default=bpy.data.collections.get('Collection'); default.name='00_WORKSHOP_VISIBLE'
visible=default
coll=bpy.data.collections.new('90_COLLISION_PROXIES_NONRENDER'); bpy.context.scene.collection.children.link(coll)
anchors=bpy.data.collections.new('80_NAMED_ANCHORS'); bpy.context.scene.collection.children.link(anchors)
stage=bpy.data.collections.new('99_DESIGN_PREVIEW_ONLY'); bpy.context.scene.collection.children.link(stage)
palette={
 'Enamel Ivory':'#F3E7CF','Enamel Pale':'#FFF0D3','Deep Teal':'#245E5A',
 'Sea Glass':'#4D9B91','Teal Shadow':'#153C48','Copper Orange':'#E79554',
 'Copper Edge':'#B77950','Brass':'#E7BC76','Ink':'#243449','Dusk Lavender':'#7F809F',
 'Lilac Gray':'#AAA5BC','Plant Jade':'#397D69','Plant Mint':'#78B18A',
 'Lamp Peach':'#FFD9A5','Signal Cyan':'#82D9CE','Rubber':'#334047',
 'Window Dark':'#3C5268','Sky Ink':'#202D49', 'Paper':'#E3D0A8'
}
M={}
def srgb(v): return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4
def material(name,hexcol,metal=0,rough=.52,emission=0):
    m=bpy.data.materials.new(name); m.use_nodes=True
    rgb=tuple(srgb(int(hexcol[i:i+2],16)/255) for i in (1,3,5))
    bs=m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value=(*rgb,1)
    bs.inputs['Roughness'].default_value=rough; bs.inputs['Metallic'].default_value=metal
    if emission:
        bs.inputs['Emission Color'].default_value=(*rgb,1); bs.inputs['Emission Strength'].default_value=emission
    m.diffuse_color=(*rgb,1); M[name]=m; return m
for name,h in palette.items():
    material(name,h, .5 if name in ['Copper Orange','Copper Edge','Brass'] else .08,
             .35 if name in ['Copper Orange','Brass'] else .52,
             2.0 if name=='Lamp Peach' else .65 if name=='Signal Cyan' else 0)

modules={}; current=None
def ancestors(o):
    result=[];p=o.parent
    while p:
        result.append(p);p=p.parent
    return result
def relink(o,c):
    for old in list(o.users_collection): old.objects.unlink(o)
    c.objects.link(o)
def empty(name,loc=(0,0,0),collection=visible,parent=None):
    o=bpy.data.objects.new(name,None); collection.objects.link(o); o.location=loc
    o.empty_display_size=.18; o.empty_display_type='PLAIN_AXES'
    if parent: o.parent=parent
    return o
def module(name,origin=(0,0,0)):
    global current
    current=empty(name,origin); current['asset_role']='modular_visual_root'
    current['units']='meters'; modules[name]=current; return current
def attach(o,name,mat,parent=None,collection=visible):
    o.name=name; relink(o,collection)
    if mat: o.data.materials.append(M[mat])
    if parent is None: parent=current
    if parent:
        bpy.context.view_layer.update()
        world=o.matrix_world.copy(); o.parent=parent; o.matrix_world=world
    return o
def apply(o):
    bpy.context.view_layer.objects.active=o; o.select_set(True)
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.select_set(False)
def bevel(o,w=.04,segments=3):
    if w:
        mod=o.modifiers.new('Soft manufactured edges','BEVEL'); mod.width=w; mod.segments=segments
        mod.affect='EDGES'
        bpy.context.view_layer.objects.active=o
        bpy.ops.object.modifier_apply(modifier=mod.name)
    for p in o.data.polygons: p.use_smooth=True
    n=o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL'); n.keep_sharp=True; n.weight=35
    bpy.context.view_layer.objects.active=o; bpy.ops.object.modifier_apply(modifier=n.name)
    return o
def box(name,loc,dim,mat,w=.035,parent=None,collection=visible,segments=3):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.dimensions=dim; apply(o)
    bevel(o,w,segments); return attach(o,name,mat,parent,collection)
def cyl(name,loc,r,depth,mat,axis='Z',vertices=24,parent=None,w=.012):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=depth,location=loc)
    o=bpy.context.object
    if axis=='X': o.rotation_euler[1]=math.pi/2
    if axis=='Y': o.rotation_euler[0]=math.pi/2
    bevel(o,w,2); return attach(o,name,mat,parent)
def uv(name,loc,scale,mat,seg=16,rings=8,parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=rings,radius=1,location=loc)
    o=bpy.context.object; o.scale=scale; apply(o)
    for p in o.data.polygons:p.use_smooth=True
    return attach(o,name,mat,parent)
def torus(name,loc,major,minor,mat,axis='Z',parent=None):
    bpy.ops.mesh.primitive_torus_add(major_segments=24,minor_segments=8,location=loc,major_radius=major,minor_radius=minor)
    o=bpy.context.object
    if axis=='X':o.rotation_euler[1]=math.pi/2
    if axis=='Y':o.rotation_euler[0]=math.pi/2
    for p in o.data.polygons:p.use_smooth=True
    return attach(o,name,mat,parent)
def path(name,points,rad,mat,parent=None):
    cu=bpy.data.curves.new(name,'CURVE'); cu.dimensions='3D'; cu.resolution_u=2 if '_stem' in name else 10
    cu.bevel_depth=rad; cu.bevel_resolution=2 if '_stem' in name else 4;cu.use_fill_caps=True
    sp=cu.splines.new('BEZIER'); sp.bezier_points.add(len(points)-1)
    for b,p in zip(sp.bezier_points,points):b.co=p;b.handle_left_type='AUTO';b.handle_right_type='AUTO'
    o=bpy.data.objects.new(name,cu); visible.objects.link(o)
    bpy.context.view_layer.objects.active=o; o.select_set(True);bpy.ops.object.convert(target='MESH');o.select_set(False)
    for p in o.data.polygons:p.use_smooth=True
    return attach(o,name,mat,parent)
def text3(name,body,loc,size,mat,rot=(math.pi/2,0,0),align='CENTER',parent=None):
    cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.size=size;cu.align_x=align;cu.align_y='CENTER';cu.extrude=.0005;cu.resolution_u=4
    o=bpy.data.objects.new(name,cu);visible.objects.link(o);o.location=loc;o.rotation_euler=rot
    bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');o.select_set(False)
    return attach(o,name,mat,parent)
def proxy(name,loc,dim,parent=None):
    o=box('COL_'+name,loc,dim,None,0,parent,coll);o.hide_render=True;o.display_type='WIRE'
    o['physics_role']='simple box proposal; runtime physics validation required';return o
def anchor(name,loc,parent=None):
    o=empty(name,loc,anchors)
    if parent:
        bpy.context.view_layer.update()
        world=o.matrix_world.copy();o.parent=parent;o.matrix_world=world
    o['purpose']='named placement reference, not gameplay code';return o

# STATIC ISLAND: a shallow framed roof with a legible open front route.
module('rooftop_base')
box('rounded_diorama_foundation',(0,.8,-1.22),(8.9,5.6,.38),'Teal Shadow',.18)
box('foundation_lavender_shadow',(0,.8,-1.46),(8.55,5.32,.18),'Dusk Lavender',.085)
box('foundation_cream_pinstripe',(0,-1.99,-1.15),(8.24,.035,.042),'Brass',.015)
for x in [-3.65,3.65]:
    box('foundation_foot',(x,1.5,-1.67),(.55,.7,.32),'Ink',.12)
box('rear_service_deck',(0,1.57,-.13),(8.25,2.22,.26),'Deep Teal',.12)
box('rear_service_deck_top',(0,1.57,.018),(8.15,2.16,.065),'Sea Glass',.06)
for x in [-3,-1.5,0,1.5,3]:box('rear_deck_seam',(x,1.65,.055),(.018,1.75,.008),'Deep Teal',.003)

# Split route decks. Top exactly Z=0, gap exactly 2.2m.
for side,x in [('left',-2.55),('right',2.55)]:
    root=module('floor_'+side,(x,0,0))
    body=box('floor_'+side+'_body',(x,0,-.37),(2.9,1.9,.7),'Deep Teal',.12)
    deck=box('floor_'+side+'_ivory_deck',(x,0,-.09),(2.9,1.92,.18),'Enamel Ivory',.085)
    # Shallow end pocket keeps the flush bridge from intersecting the solid deck.
    sign=-1 if side=='left' else 1
    bpy.ops.mesh.primitive_cube_add(size=1,location=(sign*1.1,0,0))
    cutter=bpy.context.object;cutter.dimensions=(.76,.64,.5);apply(cutter);bevel(cutter,.025,3)
    for part in [body,deck]:
        mod=part.modifiers.new('Beam landing pocket','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
        bpy.context.view_layer.objects.active=part;bpy.ops.object.modifier_apply(modifier=mod.name)
        normals=part.modifiers.new('Pocket surface normals','WEIGHTED_NORMAL');normals.keep_sharp=True;normals.weight=50
        bpy.ops.object.modifier_apply(modifier=normals.name)
    bpy.data.objects.remove(cutter,do_unlink=True)
    box('floor_'+side+'_front_inset',(x,-.956,-.42),(2.48,.032,.29),'Teal Shadow',.028)
    box('floor_'+side+'_front_stripe',(x,-.984,-.38),(2.24,.018,.035),'Sea Glass',.01)
    for dx in [-.97,0,.97]:
        box('floor_'+side+'_tile_seam',(x+dx,0,.001),(.016,1.69,.003),'Paper',.002)
    for dx in [-1.02,1.02]:
        cyl('floor_'+side+'_rivet',(x+dx,-.986,-.45),.036,.015,'Brass','Y',16,w=.004)
    proxy('floor_'+side+'_main',(sign*2.74,0,-.22),(2.52,1.9,.44),root)
    for depth in [-.635,.635]:
        proxy('floor_'+side+'_shoulder_'+str(depth),(sign*1.29,depth,-.22),(.38,.63,.44),root)
    proxy('floor_'+side+'_pocket_bottom',(x,0,-.345),(2.9,1.9,.19),root)
    for dx in [-.85,.85]:box('floor_'+side+'_column',(x+dx,.14,-.86),(.31,1.28,.52),'Teal Shadow',.06)
    text3('floor_'+side+'_label','01' if side=='left' else '02',(x,-.991,-.46),.12,'Enamel Ivory')

# Visible cradles: recess top at Z=-.22, beam top ends flush at Z=0.
for side,x in [('left',-1.18),('right',1.18)]:
    root=module('support_'+side,(x,0,-.22))
    box('support_'+side+'_load_bearing_shelf',(x,0,-.36),(.58,1.04,.28),'Copper Orange',.055)
    box('support_'+side+'_cushion',(x,0,-.236),(.51,.52,.032),'Rubber',.01)
    for y in [-.4,.4]:
        box('support_'+side+'_channel_wall',(x,y,-.18),(.58,.17,.33),'Enamel Ivory',.05)
        box('support_'+side+'_channel_lip',(x,y,-.007),(.39,.1,.022),'Brass',.007)
        proxy('support_'+side+'_channel_'+str(y),(x,y,-.18),(.58,.17,.33),root)
    for y in [-.46,.46]:cyl('support_'+side+'_bolt',(x,y,-.09),.035,.07,'Copper Edge','Z',16,w=.005)
    proxy('support_'+side+'_shelf',(x,0,-.36),(.58,1.04,.28),root)
    anchor('ANCHOR_'+side+'_beam_contact',(x,0,-.22),root)

# The hero object: independent root, broad copper color, no upper parent.
beam=module('bridge_beam',(0,0,-.11))
beam['runtime_contract']='Independent root. Held world pose follows mechanism; detach once preserving pose before dynamics. No animation is physics.'
box('bridge_beam_copper_core',(0,0,-.11),(2.9,.35,.22),'Copper Orange',.032)
for x in [-1.35,1.35]:
    box('bridge_beam_enamel_endcap',(x,0,-.105),(.11,.36,.23),'Copper Edge',.025)
    for y in [-.115,.115]:cyl('bridge_beam_endcap_rivet',(x,y,.014),.022,.011,'Brass','Z',12,w=.002)
box('bridge_beam_top_grip',(0,0,.004),(2.47,.2,.008),'Copper Edge',.018)
for x in [i*.155 for i in range(-7,8)]:
    box('bridge_beam_grip_bar',(x,0,.011),(.022,.17,.009),'Copper Orange',.003,segments=1)
for y in [-.176,.176]:box('bridge_beam_edge_highlight',(0,y,-.083),(2.5,.012,.025),'Brass',.006)
proxy('bridge_beam',(0,0,-.11),(2.9,.35,.22),beam)
anchor('ANCHOR_beam_center',(0,0,-.11),beam)
for side,x in [('left',-1.3),('right',1.3)]:anchor('ANCHOR_beam_'+side+'_endpoint',(x,0,-.11),beam)

# Recovery basin is a real separate object well under the gap.
root=module('recovery_tray',(0,0,-.99))
box('recovery_tray_shell',(0,0,-1.01),(3.52,2.25,.22),'Sea Glass',.12)
box('recovery_tray_soft_pad',(0,0,-.882),(3.15,1.86,.06),'Rubber',.08)
for y in [-1.035,1.035]:box('recovery_tray_cream_lip',(0,y,-.73),(3.51,.15,.47),'Enamel Ivory',.07)
for x in [-1.68,1.68]:box('recovery_tray_end_lip',(x,0,-.74),(.15,1.97,.43),'Enamel Ivory',.065)
for x in [-1.35,-.9,-.45,0,.45,.9,1.35]:box('recovery_tray_pad_rib',(x,0,-.843),(.035,1.72,.026),'Deep Teal',.01)
text3('recovery_tray_label','SOFT LANDING',(0,-1.12,-.725),.125,'Deep Teal')
proxy('recovery_tray',(0,0,-1.01),(3.52,2.25,.22),root)
for y in [-1.035,1.035]:proxy('recovery_tray_lip_'+str(y),(0,y,-.73),(3.51,.15,.47),root)
anchor('ANCHOR_recovery_center',(0,0,-.85),root)

# A small optional practice curb is out of the central route lane.
root=module('practice_curb',(-3,.63,.055))
box('practice_curb_rounded',(-3,.63,.055),(.56,.36,.11),'Sea Glass',.045)
box('practice_curb_top',(-3,.63,.116),(.35,.21,.015),'Enamel Pale',.028)
proxy('practice_curb',(-3,.63,.055),(.56,.36,.11),root)

# Recessed workshop frame, deliberately separated from the rotating carrier.
root=module('workshop_frame')
for x in [-4.03,4.03]:
    box('frame_rear_pillar',(x,2.55,1.41),(.24,.28,2.86),'Deep Teal',.075)
    box('frame_copper_cap',(x,2.55,2.91),(.33,.37,.15),'Copper Orange',.065)
box('rear_wall_lavender',(0,2.62,1.18),(7.86,.16,2.46),'Dusk Lavender',.1)
box('rear_wall_cream_top',(0,2.62,2.4),(8.19,.35,.2),'Enamel Ivory',.075)
for x in [-2.85,2.85]:
    box('rear_window_frame',(x,2.512,1.5),(1.68,.08,1.27),'Deep Teal',.085)
    box('rear_window_glass',(x,2.46,1.5),(1.42,.035,1.03),'Window Dark',.07)
    for yoff in [-.28,.28]:
        box('rear_window_warm_pane',(x+yoff,2.435,1.6),(.4,.018,.49),'Lamp Peach',.065)
    box('rear_window_mullion',(x,2.414,1.5),(.065,.028,1.02),'Deep Teal',.015)
    box('rear_window_sill',(x,2.4,.81),(1.85,.44,.13),'Enamel Ivory',.04)
box('rear_center_panel',(0,2.504,1.31),(2.62,.06,1.95),'Teal Shadow',.08)
for x in [-.78,0,.78]:
    box('rear_panel_groove',(x,2.464,1.05),(.027,.01,1.02),'Deep Teal',.007)
box('shop_sign_plate',(0,2.36,2.63),(2.58,.2,.7),'Enamel Ivory',.13)
text3('shop_sign_FOLD_FETCH','FOLD & FETCH',(0,2.247,2.68),.25,'Deep Teal')
text3('shop_sign_subtitle','ROOFTOP REPAIR CLUB',(0,2.239,2.44),.078,'Copper Edge')
for x in [-1.15,1.15]:cyl('shop_sign_screw',(x,2.239,2.68),.028,.014,'Copper Edge','Y',12,w=.002)
for x in [-1.75,1.75]:
    box('fixed_hinge_wall_mount',(x,2.53,2.51),(.28,.35,.38),'Deep Teal',.07)
    path('fixed_hinge_support',[(x,2.49,2.57),(x,2.18,2.98),(x,1.2,3)],.085,'Deep Teal')

# Railings and rail-end lights are separate static modules.
root=module('roof_rails')
for x in [-4.08,4.08]:
    for y in [-.5,.5,1.5,2.1]:
        cyl('railing_upright',(x,y,.48),.047,.94,'Enamel Ivory',vertices=16,w=.013)
        cyl('railing_base',(x,y,.05),.095,.13,'Copper Orange',vertices=16,w=.016)
    path('rounded_roof_side_rail',[(x,-.62,.83),(x,-.62,1.03),(x,2.28,1.03)],.052,'Enamel Ivory')
    path('roof_secondary_rail',[(x,-.48,.4),(x,2.22,.4)],.027,'Deep Teal')

# Hinge carrier. Origin is its true X rotation axis. All meshes parented to it.
H=Vector((0,1.2,3.0))
hinge=module('upper_chute',tuple(H));hinge['hinge_axis_source']='X';hinge['hinge_axis_game']='X'
hinge['pose_note']='0 degrees is intended design play alignment, not a calibrated device angle.'
for x in [-1.75,1.75]:
    path('chute_swept_cream_arm',[(x,1.2,3),(x,1.02,2.8),(x,.0,2.0)],.09,'Enamel Ivory')
    cyl('chute_hinge_copper_hub',(x,1.2,3),.205,.15,'Copper Orange','X',24,w=.015)
    cyl('chute_hinge_teal_inset',(x+(-.085 if x<0 else .085),1.2,3),.126,.022,'Deep Teal','X',24,w=.01)
    cyl('chute_hinge_bolt',(x+(-.105 if x<0 else .105),1.2,3),.046,.025,'Brass','X',12,w=.004)
box('chute_rear_crossbar',(0,.37,2.06),(3.64,.24,.25),'Deep Teal',.075)
box('chute_rear_soft_inset',(0,.229,2.08),(3.26,.052,.1),'Sea Glass',.025)
for x in [-1.59,1.59]:
    box('chute_end_guide',(x,0,1.94),(.15,.63,.42),'Enamel Ivory',.055)
    box('chute_end_copper_pin',(x,0,2.163),(.1,.28,.036),'Copper Orange',.013)
box('chute_overhead_cowling',(0,.095,2.41),(3.32,.6,.25),'Deep Teal',.11)
box('chute_cowling_ivory_face',(0,-.222,2.42),(2.58,.06,.16),'Enamel Ivory',.045)
text3('chute_face_label','ALIGN  •  RELEASE',(0,-.259,2.428),.097,'Deep Teal')
for x in [-1.37,1.37]:uv('chute_status_lens',(x,-.21,2.42),(.047,.025,.047),'Signal Cyan',12,6)
anchor('ANCHOR_hinge_axis',H,hinge)
anchor('ANCHOR_held_beam_center',(0,0,1.75),hinge)
anchor('ANCHOR_release_point',(0,0,1.64),hinge)
# Simple guide colliders do not fill open underside; their sweep is unverified.
for x in [-1.59,1.59]:proxy('chute_end_guide',(x,0,1.94),(.15,.63,.42),hinge)

# Gate origin lies on a real X pivot. Gate is separate but follows chute.
gate=module('release_gate',(0,.27,1.6));gate.parent=hinge;gate.matrix_world=Matrix.Translation((0,.27,1.6))
gate['gate_axis']='X';gate['open_reference_degrees']=72
box('release_gate_copper_bar',(0,0,1.59),(3.25,.2,.12),'Copper Orange',.045)
for x in [-1.5,1.5]:
    box('release_gate_support_finger',(x,.13,1.61),(.1,.31,.075),'Copper Edge',.025)
    cyl('release_gate_pivot_pin',(x,.27,1.6),.07,.19,'Brass','X',16,w=.008)
cyl('release_gate_pull_switch',(1.84,.27,1.6),.11,.27,'Copper Orange','X',20,w=.02)
uv('release_gate_pull_tip',(2,.27,1.6),(.11,.12,.12),'Enamel Ivory',16,8)
proxy('release_gate',(0,0,1.59),(3.25,.2,.12),gate)
anchor('ANCHOR_release_gate_pivot',(0,.27,1.6),gate)

# Clear exit bell, dog toy, and little receiving arch.
root=module('exit_bell',(3.3,.05,0))
box('exit_bell_base',(3.3,.36,.055),(.89,.72,.11),'Sea Glass',.085)
for x in [2.98,3.62]:
    box('exit_arch_post',(x,.45,.6),(.105,.12,1.15),'Enamel Ivory',.045)
path('exit_arch_top',[(2.98,.45,1.13),(3.05,.45,1.36),(3.55,.45,1.36),(3.62,.45,1.13)],.061,'Enamel Ivory')
box('exit_label',(3.3,.36,1.36),(.58,.12,.28),'Deep Teal',.08)
text3('exit_label_letters','HOME',(3.3,.288,1.36),.11,'Enamel Pale')
cyl('exit_bell_stem',(3.3,.44,1.04),.025,.19,'Copper Edge',vertices=12,w=.004)
# Lathed bell profile, soft and legible.
def lathe(name,loc,profile,mat,parent=None,segments=32):
    vs=[];fs=[]
    for z,r in profile:
        for i in range(segments):
            a=2*math.pi*i/segments;vs.append((r*math.cos(a),r*math.sin(a),z))
    for j in range(len(profile)-1):
        for i in range(segments):
            a=j*segments+i;b=j*segments+(i+1)%segments;fs.append((a,b,b+segments,a+segments))
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update()
    o=bpy.data.objects.new(name,me);visible.objects.link(o);o.location=loc
    for p in me.polygons:p.use_smooth=True
    return attach(o,name,mat,parent)
lathe('exit_bell_brass_body',(3.3,.44,.65),[(0,.245),(.04,.25),(.09,.19),(.26,.14),(.32,.085),(.34,.02)],'Brass')
torus('exit_bell_rolled_rim',(3.3,.44,.673),.228,.027,'Copper Orange')
uv('exit_bell_clapper',(3.3,.44,.633),(.046,.046,.067),'Copper Edge',12,6)
anchor('ANCHOR_exit_goal',(3.3,0,.15),root)
root=module('goal_toy',(3.2,-.22,.19))
uv('goal_ball',(3.2,-.22,.19),(.19,.19,.19),'Sea Glass',24,12)
torus('goal_ball_copper_band',(3.2,-.22,.19),.187,.012,'Copper Orange','X')
uv('goal_ball_cream_spot',(3.2,-.403,.21),(.077,.016,.075),'Enamel Pale',12,6)
proxy('goal_toy',(3.2,-.22,.19),(.38,.38,.38),root)

# Repair bench and readable small tools tucked in the rear left nook.
root=module('repair_bench',(-2.85,1.75,0))
for x in [-3.55,-2.15]:
    box('bench_leg',(x,1.73,.43),(.12,.61,.84),'Deep Teal',.035)
box('bench_worktop',(-2.85,1.72,.87),(1.85,.88,.16),'Enamel Ivory',.09)
box('bench_drawer',(-2.86,1.73,.62),(1.47,.63,.25),'Copper Orange',.05)
box('bench_drawer_pull',(-2.86,1.396,.62),(.39,.035,.06),'Deep Teal',.023)
box('bench_mint_cutting_mat',(-2.85,1.64,.959),(1.15,.56,.018),'Sea Glass',.033)
for x in [-3.08,-2.58]:
    box('bench_spare_block',(x,1.66,1.012),(.19,.2,.1),'Copper Orange',.025)
box('bench_tool_handle',(-2.84,1.47,1.018),(.34,.057,.061),'Copper Edge',.02)
cyl('bench_tool_head',(-2.64,1.47,1.02),.074,.05,'Brass',vertices=12,w=.009)
box('bench_under_crate',(-2.87,1.7,.21),(.88,.57,.42),'Sea Glass',.06)
for x in [-3.16,-2.87,-2.58]:box('bench_crate_slat',(x,1.4,.23),(.018,.024,.26),'Deep Teal',.006)

# Three grouped planters, lush curved leaves without faceting.
root=module('planters')
def plant(name,x,y,z,s=1):
    lathe(name+'_pot',(x,y,z),[(0,.2*s),(.035*s,.245*s),(.39*s,.28*s),(.42*s,.29*s),(.45*s,.285*s)],'Copper Orange',segments=24)
    cyl(name+'_soil',(x,y,z+.425*s),.25*s,.025*s,'Ink',vertices=24,w=.008)
    torus(name+'_pot_rim',(x,y,z+.44*s),.273*s,.029*s,'Enamel Ivory')
    for i in range(8):
        a=i*2.4; r=(.08+.035*(i%3))*s
        lo=Vector((x+math.cos(a)*r,y+math.sin(a)*r,z+(.67+.07*(i%3))*s))
        leaf=uv(name+'_leaf',lo,(.104*s,.067*s,(.23+.027*(i%3))*s),'Plant Mint' if i%3==0 else 'Plant Jade',12,8)
        leaf.rotation_euler=(.4*math.sin(a),.55*math.cos(a),a)
        path(name+'_stem',[(x,y,z+.42*s),tuple(lo)],.012*s,'Plant Jade')
for name,x,y,z,s in [('left_fern',-3.72,1.25,.06,.76),('right_fern',3.67,1.57,.06,1),('window_sprout',2.88,2.39,.91,.63)]:plant(name,x,y,z,s)

# Warm practical lamps, service pipes and one looping roof cable.
root=module('workshop_lamps')
for x in [-3.48,3.48]:
    cyl('lamp_wall_mount',(x,2.46,2.29),.11,.08,'Deep Teal','Y',20,w=.02)
    path('lamp_curved_arm',[(x,2.39,2.29),(x,2.13,2.51),(x,1.91,2.27)],.03,'Copper Edge')
    lathe('lamp_cream_shade',(x,1.91,2.1),[(0,.22),(.04,.215),(.2,.09),(.22,.045)],'Enamel Ivory',segments=24)
    uv('lamp_warm_bulb',(x,1.91,2.09),(.11,.11,.066),'Lamp Peach',16,8)
    data=bpy.data.lights.new('warm_practical','POINT');data.energy=12;data.color=(1,.65,.33);data.shadow_soft_size=.35
    ob=bpy.data.objects.new('warm_practical',data);stage.objects.link(ob);ob.location=(x,1.91,2.02)
root=module('service_cables')
path('copper_side_service_pipe',[(-4.16,2.2,-.7),(-4.16,1.9,-.65),(-4.16,1.9,1.2),(-4.16,2.65,1.35)],.062,'Copper Edge')
path('soft_cable_swag',[(-4,2.29,2.54),(-2.3,2.25,2.85),(0,2.23,2.92),(2.4,2.23,2.85),(4,2.29,2.54)],.024,'Ink')
for x in [-3.35,-2.1,2.1,3.35]:
    uv('cable_amber_bead',(x,2.255,2.75),(.05,.048,.073),'Lamp Peach',12,6)
box('utility_cabinet',(2.08,1.91,.6),(.58,.49,1.07),'Deep Teal',.08)
box('utility_cabinet_door',(2.08,1.642,.63),(.41,.05,.79),'Sea Glass',.04)
for z in [.81,.72,.63]:box('utility_cabinet_louver',(2.08,1.61,z),(.25,.022,.027),'Deep Teal',.012)
cyl('utility_cabinet_latch',(2.21,1.6,.43),.026,.027,'Brass','Y',12,w=.003)

# Designed night skyline geometry: restrained contrast, no photographic backdrop.
root=module('distant_city')
buildings=[(-5.1,5.7,2.9,.88),(-4.2,6.2,4.1,1.02),(-3.2,5.5,2.4,.78),(-2.2,6,3.4,.91),(-1.1,5.8,4.7,.88),(.05,6.5,3.3,1.01),(1.2,6,4.2,.87),(2.3,5.8,3.05,.91),(3.35,6.2,4.5,1.08),(4.55,5.7,3.3,.92),(5.4,6.4,2.7,.74)]
for i,(x,y,h,w) in enumerate(buildings):
    box('city_building_%02d'%i,(x,y,h/2-1.1),(w,.8,h),'Sky Ink' if i%2 else 'Window Dark',.08,segments=2)
    box('city_rooftop_%02d'%i,(x,y,h-1.05),(w*.68,.62,.13),'Dusk Lavender',.035,segments=2)
    for row in range(int(h/.47)-1):
        for col in range(2):
            if (row*7+col*3+i)%5 in [0,1]:
                box('city_window_%02d'%i,(x+(-.18 if col==0 else .18)*w,y-.411,-.63+row*.43),(.10,.018,.19),'Lamp Peach' if i%3 else 'Sea Glass',.02,segments=1)
    if i%3==0:cyl('city_antenna',(x+.1,y,h-.73),.017,.6,'Dusk Lavender',vertices=8,w=0)

# Named global anchors and metadata.
current=None
anchor('ANCHOR_corgi_start',(-3.35,0,0))
anchor('ANCHOR_route_forward',(4,0,0))
anchor('ANCHOR_gap_center',(0,0,0))
anchor('ANCHOR_world_origin',(0,0,0))
for o in anchors.objects:o.hide_render=True
for o in coll.objects:o.hide_render=True

# Studio stage and intentionally sharp cameras.
ground=box('preview_shadow_ground',(0,0,-1.86),(200,200,.12),'Sky Ink',0,collection=stage)
bpy.context.preferences.filepaths.save_version=0
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.12,.16,.25,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.45
def area(name,loc,power,size,color,target=(0,.6,0)):
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;d.color=color
    o=bpy.data.objects.new(name,d);stage.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
area('warm_key',(-4,-5,10),1700,7,(1,.78,.56))
area('lavender_fill',(6,0,7),1300,7,(.6,.73,1))
area('soft_roof_rim',(0,5,9),1400,6,(1,.61,.43))
def camera(name,loc,target,scale):
    d=bpy.data.cameras.new(name);d.type='ORTHO';d.ortho_scale=scale;d.lens=45;d.dof.use_dof=False
    o=bpy.data.objects.new(name,d);stage.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o
cam=camera('CAM_workshop_main',(10,-15,10),(0,1.0,.7),12.9)
cameras={
 'workshop-main':cam,
 'workshop-detail-bridge':camera('CAM_bridge_detail',(5.7,-8,5),(0,-.07,.15),6.15),
 'workshop-detail-rooftop':camera('CAM_rooftop_detail',(6,-7,4.6),(2.25,1.5,1.05),4.8),
 'layout-top':camera('CAM_layout_top',(0,.4,16),(0,.4,0),10.5),
 'layout-side':camera('CAM_layout_side',(12,.7,1),(0,.7,1),8.7),
 'layout-front':camera('CAM_layout_front',(0,-16,1.1),(0,0,1.1),10.3),
 'fold':camera('CAM_fold_reference',(8,-12,7),(0,.85,1.2),10.8)
}
scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True
try:
    prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
    for device in prefs.devices:device.use=device.type=='METAL'
    if any(d.type=='METAL' for d in prefs.devices):scene.cycles.device='GPU'
except (TypeError,RuntimeError):scene.cycles.device='CPU'
scene.cycles.max_bounces=6;scene.cycles.diffuse_bounces=3;scene.cycles.glossy_bounces=3
scene.render.resolution_x=2160;scene.render.resolution_y=1440;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
scene.render.use_motion_blur=False
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast'
scene.render.image_settings.color_mode='RGBA'
scene['design_only']='DESIGN PREVIEW. Not simulator footage. No working physics or live fold input.'
scene['coordinate_contract']='Source Blender (X,Y,Z) -> game and GLB/USD (X,Z,-Y), meters.'

# Generate a palette atlas with actual PNG colors and use material fallback colors.
img=bpy.data.images.new('Workshop_Palette',width=512,height=128,alpha=True);img.use_fake_user=True
colors=list(palette.values());pixels=[]
for py in range(128):
    for px in range(512):
        c=colors[min(len(colors)-1,int(px/512*len(colors)))];pixels.extend([int(c[i:i+2],16)/255 for i in (1,3,5)]+[1])
img.pixels=pixels;img.filepath_raw=str(TEXTURE/'workshop-palette.png');img.file_format='PNG';img.save();img.pack()
(TEXTURE/'workshop-palette.json').write_text(json.dumps(palette,indent=2))

# Build data counts and dimensions before export.
def tris(o): return sum(len(p.vertices)-2 for p in o.data.polygons) if o.type=='MESH' else 0
module_info={}
for name,root in modules.items():
    objects=[o for o in visible.objects if o==root or root in ancestors(o)]
    # The gate is an independent module despite following the upper chute in source.
    if name=='upper_chute':objects=[o for o in objects if o!=gate and gate not in ancestors(o)]
    module_info[name]={'triangles':sum(tris(o) for o in objects),'mesh_count':sum(o.type=='MESH' for o in objects),
                       'assembly_origin_blender':list(root.matrix_world.translation),
                       'assembly_origin_game':[root.matrix_world.translation.x,root.matrix_world.translation.z,-root.matrix_world.translation.y]}
report={
 'asset':'Original Fold & Fetch rooftop workshop','blender_version':bpy.app.version_string,
 'visible_triangles':sum(tris(o) for o in visible.objects),'collision_triangles':sum(tris(o) for o in coll.objects),
 'material_count':len(M),'modules':module_info,
 'source_axis':'Z up, X route, -Y front; meters', 'export_axis':'Y up, X route, +Z front; meters',
 'beam_dimensions_m':[2.9,.22,.35], 'gap_m':2.2,
 'platform_extent_gap_m':2.2,'route_centerline_opening_with_pockets_m':2.96,'pocket_end_clearance_m':.03,'pocket_bottom_clearance_m':.03,
 'hinge_game':[0,3,-1.2], 'hinge_axis':'X',
 'verified':['All mesh scales applied at construction','Blender geometry generated reproducibly','No camera DOF or scene motion blur'],
 'unverified':['SceneKit/RealityKit import','Mobile frame time','Physics stability','Live fold/device angle mapping','Collision response'],
 'pose_reference_only':True}
report['visible_without_city_triangles']=report['visible_triangles']-module_info['distant_city']['triangles']
report['runtime_meshes']=len(modules)
report['runtime_optimization']='One joined multi-material mesh per module; editable component meshes remain in source.'
(VALID/'workshop-geometry.json').write_text(json.dumps(report,indent=2))

# Save original editable scene, with visible collision outlines available in collection.
bpy.ops.object.select_all(action='DESELECT')
for ob in coll.objects:ob.hide_set(True)
scene.camera=cam
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE/'fold-and-fetch-workshop.blend'))

def select_objects(obs):
    bpy.ops.object.select_all(action='DESELECT')
    for o in obs:
        o.hide_set(False);o.select_set(True)
def export_set(name,obs):
    select_objects(obs)
    bpy.ops.export_scene.gltf(filepath=str(EXPORT/(name+'.glb')),export_format='GLB',use_selection=True,
      export_yup=True,export_apply=True,export_animations=False,export_cameras=False,export_lights=False,
      export_extras=True,export_materials='EXPORT')
    bpy.ops.wm.usd_export(filepath=str(EXPORT/(name+'.usdc')),selected_objects_only=True,
      export_animation=False,export_hair=False,export_materials=True,export_normals=True,
      generate_preview_surface=True,generate_materialx_network=False,convert_orientation=True,
      export_global_forward_selection='NEGATIVE_Z',export_global_up_selection='Y',
      export_textures_mode='KEEP',export_lights=False,export_cameras=False,
      triangulate_meshes=True,root_prim_path='/Workshop',export_custom_properties=True)

# Consolidate each runtime piece while retaining every editable source component.
runtime={}
for name,root in modules.items():
    parts=[o for o in visible.objects if o.type=='MESH' and root in ancestors(o)]
    if name=='upper_chute':parts=[o for o in parts if gate not in ancestors(o)]
    copies=[]
    for part in parts:
        copy=part.copy();copy.data=part.data.copy();visible.objects.link(copy);copies.append(copy)
    select_objects(copies);bpy.context.view_layer.objects.active=copies[0]
    bpy.ops.object.join();joined=bpy.context.object
    joined.data.transform(root.matrix_world.inverted() @ joined.matrix_world)
    joined.parent=root;joined.matrix_parent_inverse=Matrix.Identity(4);joined.matrix_basis=Matrix.Identity(4)
    joined.name=name+'_mesh';runtime[name]=joined

# Whole assembly excludes render-only lighting, ground and cameras.
export_set('workshop-assembled',list(modules.values())+list(runtime.values())+list(anchors.objects))
for name,root in modules.items():
    obs=[root,runtime[name]]
    obs += [o for o in anchors.objects if o.parent==root]
    if name=='upper_chute':obs=[o for o in obs if o!=gate and gate not in ancestors(o)]
    old_parent=root.parent;old_world=root.matrix_world.copy()
    # Temporarily put piece pivot at file origin; preserve all relative mesh transforms.
    root.parent=None;root.matrix_world=Matrix.Identity(4);bpy.context.view_layer.update()
    export_set(name,obs)
    root.parent=old_parent;root.matrix_world=old_world;bpy.context.view_layer.update()
# Collision collection is exported separately, never baked into visible GLBs.
for ob in coll.objects:ob.hide_render=False
export_set('workshop-collision-proxies',list(coll.objects)+list(modules.values()))
for ob in coll.objects:ob.hide_render=True
for ob in coll.objects:ob.hide_set(True)
for ob in runtime.values():bpy.data.objects.remove(ob,do_unlink=True)
print('WORKSHOP_EXPORTS_COMPLETE',report['visible_triangles'],flush=True)

# Render routes can be selected from the CLI after --; default preview draft only.
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if '--no-render' in args:
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE/'fold-and-fetch-workshop.blend'));sys.exit(0)
all_renders='--all-renders' in args
draft='--draft' in args
if draft:scene.render.resolution_percentage=55;scene.cycles.samples=20
overlay_objects=[]
caption_mat=material('Preview typography','#E6E7DE',0,.8,1)
backing_mat=material('Preview backing','#17292F',0,.8,1)
for mat in [caption_mat,backing_mat]:
    color=mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value[:]
    mat.node_tree.nodes.clear();em=mat.node_tree.nodes.new('ShaderNodeEmission');em.inputs[0].default_value=color
    out=mat.node_tree.nodes.new('ShaderNodeOutputMaterial');mat.node_tree.links.new(em.outputs[0],out.inputs[0])
def overlay_text(body,xy,size=.14,color='Preview typography'):
    cam=scene.camera;cu=bpy.data.curves.new('preview_caption','FONT');cu.body=body;cu.size=size
    cu.align_x='LEFT';cu.align_y='CENTER';cu.space_character=1.12
    ob=bpy.data.objects.new('PREVIEW_ONLY_'+body[:20],cu);stage.objects.link(ob);ob.parent=cam
    ob.location=(xy[0],xy[1],-6);ob.data.materials.append(M[color]);overlay_objects.append(ob)
    bpy.context.view_layer.update()
    xmin=min(v[0] for v in ob.bound_box)-size*.35;xmax=max(v[0] for v in ob.bound_box)+size*.35
    ymin=min(v[1] for v in ob.bound_box)-size*.35;ymax=max(v[1] for v in ob.bound_box)+size*.35
    mesh=bpy.data.meshes.new('preview_caption_backing')
    mesh.from_pydata([(xmin,ymin,0),(xmax,ymin,0),(xmax,ymax,0),(xmin,ymax,0)],[],[(0,1,2,3)])
    card=bpy.data.objects.new('PREVIEW_ONLY_caption_backing',mesh);stage.objects.link(card);card.parent=cam
    card.location=(xy[0],xy[1],-6.006);card.data.materials.append(backing_mat);overlay_objects.append(card)
    for item in [ob,card]:
        item.visible_shadow=False;item.visible_diffuse=False;item.visible_glossy=False
    return ob
def clear_overlays():
    for ob in overlay_objects:bpy.data.objects.remove(ob,do_unlink=True)
    overlay_objects.clear()
titles={
 'workshop-main':'FOLD & FETCH  /  ROOFTOP REPAIR CLUB',
 'workshop-main-draft':'FOLD & FETCH  /  ROOFTOP REPAIR CLUB',
 'workshop-detail-bridge':'COPPER BRIDGE  /  GAP & RECOVERY CRADLES',
 'workshop-detail-rooftop':'THE WARM CORNER  /  BRASS BELL & WORKSHOP',
 'layout-top':'TOP PLAN  /  METERS  /  UPPER CARRIER HIDDEN FOR ROUTE CLARITY',
 'layout-side':'RIGHT PROFILE  /  METERS  /  FOLD ROTATES ABOUT X',
 'layout-front':'FRONT ELEVATION  /  METERS  /  BEAM SPANS X',
 'fold-01-open':'01  /  OPEN REFERENCE  /  HINGE OFFSET -28 DEG',
 'fold-02-play':'02  /  INTENDED PLAY ALIGNMENT  /  HINGE OFFSET 0 DEG',
 'fold-03-more-folded':'03  /  MORE FOLDED REFERENCE  /  HINGE OFFSET +28 DEG',
}
def render(name,camera_name):
    scene.camera=cameras[camera_name];scene.render.filepath=str(PREVIEW/(name+'.png'))
    clear_overlays();width=scene.camera.data.ortho_scale;height=width*scene.render.resolution_y/scene.render.resolution_x
    overlay_text(titles.get(name,name),(-width*.465,height*.455),width*.011)
    overlay_text('DESIGN PREVIEW  /  NOT A SIMULATOR CAPTURE',(-width*.465,-height*.455),width*.009)
    if name.startswith('fold-'):
        offset=(beam.matrix_world.translation.y,beam.matrix_world.translation.z)
        overlay_text('SAME GEOMETRY  /  HELD POSE ONLY  /  NO PHYSICS',(-width*.465,-height*.418),width*.009)
    if name=='layout-front':
        overlay_text('START',(-3.65,-1.43),.12);overlay_text('EXIT',(3.17,-1.43),.12)
        overlay_text('OPTIONAL PRACTICE CURB',(-3.82,-.88),.082)
        overlay_text('RECOVERY TRAY',(-.48,-2.53),.095)
        overlay_text('2.20 m BETWEEN PLATFORM EXTENTS',(-1.16,-1.75),.105)
        overlay_text('2.90 m beam  /  deck top Y = 0',(-1.2,-2.04),.11)
        overlay_text('POCKETS / 2.96 m CENTERLINE OPENING',(-1.24,-2.27),.095)
        overlay_text('HINGE AXIS X  /  Y = 3.00 m',(-1.6,2.14),.11)
    if name=='layout-top':
        overlay_text('OPTIONAL PRACTICE CURB',(-3.88,.35),.085)
        overlay_text('START / +X ROUTE',(-3.87,-1.11),.11)
        overlay_text('EXIT BELL',(2.68,-1.11),.11)
        overlay_text('CRADLE',(-1.62,-1.11),.1);overlay_text('CRADLE',(.86,-1.11),.1)
        overlay_text('RECOVERY TRAY',(-.62,-1.08),.1)
        overlay_text('2.20 m PLATFORM EXTENT GAP',(-1.14,-1.4),.11)
        overlay_text('2.96 m CENTERLINE OPENING / 2.90 m BEAM',(-1.45,-1.64),.092)
        overlay_text('BEAM CENTER / RELEASE DEPTH Z = 0',(-1.55,-1.88),.1)
    if name=='layout-side':
        overlay_text('X AXIS POINTS TOWARD VIEWER',(-3.42,1.81),.09)
        overlay_text('HINGE  /  Y 3.00  /  Z -1.20',(-3.4,1.6),.1)
        overlay_text('HELD BEAM ANCHOR  /  Y 1.75  /  Z 0',(-3.4,1.4),.1)
        overlay_text('LANDED BEAM TOP  /  Y 0',(-3.4,-1.53),.1)
    bpy.ops.render.render(write_still=True);print('RENDER_COMPLETE',name,flush=True)
render('workshop-main-draft' if draft else 'workshop-main','workshop-main')
if all_renders:
    for name in ['workshop-detail-bridge','workshop-detail-rooftop']:render(name,name)
    city_parts=[o for o in visible.objects if modules['distant_city'] in ancestors(o)]
    upper_parts=[o for o in visible.objects if hinge in ancestors(o)]
    for ob in city_parts:ob.hide_render=True
    for ob in upper_parts:ob.hide_render=True
    render('layout-top','layout-top')
    for ob in upper_parts:ob.hide_render=False
    render('layout-side','layout-side');render('layout-front','layout-front')
    for ob in city_parts:ob.hide_render=False
    beam.matrix_world.translation=(0,0,1.75)
    for name,angle in [('fold-01-open',-28),('fold-02-play',0),('fold-03-more-folded',28)]:
        hinge.rotation_euler.x=math.radians(angle);bpy.context.view_layer.update()
        beam.matrix_world=hinge.matrix_world @ Matrix.Translation((0,-1.2,-1.25))
        render(name,'fold')
    hinge.rotation_euler.x=0;beam.matrix_world=Matrix.Translation((0,0,-.11));bpy.context.view_layer.update()
clear_overlays()
scene.camera=cam;scene.render.resolution_percentage=100;scene.cycles.samples=32
bpy.ops.object.select_all(action='DESELECT');bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE/'fold-and-fetch-workshop.blend'))
print('WORKSHOP_DONE',flush=True)
