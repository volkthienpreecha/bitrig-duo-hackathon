"""Build six neon world asset variants, Japanese mesh signage and matched colliders.
Blender -b --python stages_build.py -- [--stage 1|2|3] [--draft] [--no-render]
Art and measured geometry only; not submission/game code.
"""
import bpy,math,json,sys
from pathlib import Path
from mathutils import Matrix,Vector
BASE=Path(__file__).resolve().parents[1]; ROOT=BASE/'NeonExpansion'
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ids=[int(args[args.index('--stage')+1])] if '--stage' in args else [1,2,3,4,5,6]
CONFIG=[
 dict(id=1,kind=1,slug='01-workshop',title='Rooftop Repair Club',jp='修理工房',depth=0.,accent='#4D9B91'),
 dict(id=2,kind=2,slug='02-garden',title='Moonleaf Garden',jp='屋上庭園',depth=.32,accent='#6F9D83'),
 dict(id=3,kind=3,slug='03-terrace',title='Starlight Terrace',jp='喫茶',depth=-.28,accent='#597D98'),
 dict(id=4,kind=1,slug='04-night-market',title='Midnight Repair Market',jp='夜市',depth=.16,accent='#806E95'),
 dict(id=5,kind=2,slug='05-lantern-garden',title='Lantern Garden',jp='屋上庭園',depth=-.14,accent='#568D86'),
 dict(id=6,kind=3,slug='06-stargazer',title='Stargazer Tea Deck',jp='星見',depth=.46,accent='#697CA0')]

def anc(o):
 a=[];p=o.parent
 while p:a.append(p);p=p.parent
 return a
def bounds(o):
 ps=[o.matrix_world@Vector(v) for v in o.bound_box];return [[min(v[i] for v in ps) for i in range(3)],[max(v[i] for v in ps) for i in range(3)]]
def game(v):return [v[0],v[2],-v[1]]
def select(obs):
 bpy.ops.object.select_all(action='DESELECT')
 for o in obs:o.hide_set(False);o.select_set(True)
 if obs:bpy.context.view_layer.objects.active=obs[0]
def aim(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
def srgb(v):return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4
for cfg in CONFIG:
 if cfg['id'] not in ids:continue
 d=ROOT/cfg['slug']
 for f in ['Source','Exports','Runtime','Previews','Validation']: (d/f).mkdir(parents=True,exist_ok=True)
 bpy.ops.wm.open_mainfile(filepath=str(BASE/'Source/Workshop/fold-and-fetch-workshop.blend'))
 scene=bpy.context.scene;scene['stage_id']=cfg['id'];scene['stage_title']=cfg['title']
 visible=bpy.data.collections['00_WORKSHOP_VISIBLE'];coll=bpy.data.collections['90_COLLISION_PROXIES_NONRENDER'];anchors=bpy.data.collections['80_NAMED_ANCHORS'];studio=bpy.data.collections['99_DESIGN_PREVIEW_ONLY']
 modules={o.name:o for o in visible.objects if o.type=='EMPTY' and o.get('asset_role')}
 # Shared source helpers create rounded props with the existing material library.
 source=(BASE/'Tools/workshop_build.py').read_text();M={m.name:m for m in bpy.data.materials};current=None
 helpers=source[source.index('def relink('):source.index('# STATIC ISLAND:')]
 exec(compile(helpers,'workshop_prop_helpers','exec'))
 # Lower route and every associated collider/anchor share a fixed depth lane.
 route=['floor_left','floor_right','support_left','support_right','bridge_beam','recovery_tray','practice_curb','exit_bell','goal_toy']
 for name in route:modules[name].location.y-=cfg['depth']
 for name in ['ANCHOR_corgi_start','ANCHOR_route_forward','ANCHOR_gap_center']:
  bpy.data.objects[name].location.y-=cfg['depth']
 # Widen all beam visual details and its collider together; preserve unit-scale nodes.
 beam_root=modules['bridge_beam'];bpy.context.view_layer.update()
 stretch=beam_root.matrix_world @ Matrix.Diagonal((1,.54/.35,1,1)) @ beam_root.matrix_world.inverted()
 for o in list(visible.objects)+list(coll.objects):
  if o.type=='MESH' and beam_root in anc(o):o.data.transform(o.matrix_world.inverted() @ stretch @ o.matrix_world)
 # Keep all loose scenery outside the shifted lower route, not as an alternate bridge.
 color=cfg['accent'];rgba=tuple(srgb(int(color[i:i+2],16)/255) for i in (1,3,5))+(1,)
 M['Sea Glass'].node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=rgba;M['Sea Glass'].diffuse_color=rgba
 if cfg['kind']==2:
  current=modules['planters'];
  # Only the helper definition, before bench construction.
  # Extract lathe function directly; its following block is bench construction.
  start=source.index('def lathe(');end=source.index('\n',source.index('    return ',start))+1
  exec(compile(source[start:end],'lathe_helper','exec'))
  start=source.index('def plant(');end=source.index('\nfor name,x,y,z,s',start)
  exec(compile(source[start:end],'plant_helper','exec'))
  for name,x,y,z,s in [('garden_left',-2.0,1.4,.06,1.15),('garden_right',2.65,1.1,.06,1.12),('garden_back',.9,2.1,.06,1.25),('garden_high',-2.8,2.34,.91,.75)]:plant(name,x,y,z,s)
  # Low trellis at back: no gameplay collider.
  current=modules['workshop_frame']
  for x in [-1.0,-.5,0,.5,1.0]:box('garden_trellis',(x,2.38,1.4),(.035,.035,1.5),'Copper Edge',.012)
  for z in [.85,1.3,1.8]:box('garden_crossbar',(0,2.36,z),(2.2,.035,.035),'Copper Edge',.012)
 if cfg['kind']==3:
  # Remove the opaque backdrop while retaining structural posts, hinge mounts and sign.
  for o in list(visible.objects):
   if o.parent==modules['workshop_frame'] and o.name.startswith(('rear_wall_lavender','rear_window','rear_center_panel','rear_panel_groove')):bpy.data.objects.remove(o,do_unlink=True)
  current=modules['workshop_frame']
  box('terrace_rear_low_rail',(0,2.6,.49),(7.8,.12,.12),'Enamel Ivory',.04)
  for x in [-3,-1.75,1.75,3]:box('terrace_rear_post',(x,2.6,.27),(.06,.08,.5),'Deep Teal',.025)
  for o in visible.objects:
   if o.name.startswith('window_sprout'):o.location.z-=.85
  modules['distant_city'].location.y+=1.5
  current=modules['repair_bench']
  # Small mug and warm reading lamp add lived-in detail using existing materials.
  cyl('terrace_tea_cup',(-2.85,1.6,.99),.075,.15,'Enamel Ivory',w=.015)
  torus('terrace_cup_handle',(-2.75,1.6,1.0),.055,.014,'Enamel Ivory',axis='X')
 # Exportable neon meshes, outside the traversable route. No additional light objects.
 current=module('neon_signage')
 for name,color in [('Neon Cyan',(0.03,.8,1,1)),('Neon Pink',(1,.08,.42,1)),('Neon Amber',(1,.48,.06,1))]:
  mat=bpy.data.materials.new(name);mat.use_nodes=True
  bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=color
  bs.inputs['Emission Color'].default_value=color;bs.inputs['Emission Strength'].default_value=1.8
  bs.inputs['Roughness'].default_value=.4;M[name]=mat
 fontpath=next(Path('/System/Library/Fonts').glob('*丸*W4.ttc'))
 font=bpy.data.fonts.load(str(fontpath))
 def japanese(name,body,loc,size,material):
  cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.font=font;cu.size=size;cu.align_x='CENTER';cu.align_y='CENTER';cu.extrude=.003;cu.resolution_u=5
  o=bpy.data.objects.new(name,cu);visible.objects.link(o);o.location=loc;o.rotation_euler=(math.pi/2,0,0)
  select([o]);bpy.ops.object.convert(target='MESH');o=bpy.context.object;attach(o,name,material)
  assert len(o.data.vertices)>100, 'Japanese text failed to convert'
 # Back-wall sign replaces the English subtitle; raised panels remain above the puzzle.
 box('neon_shop_backplate',(-2.7,2.13,2.12),(1.55,.09,.63),'Deep Teal',.1)
 japanese('neon_shop_japanese',cfg['jp'],(-2.7,2.072,2.12),.28,'Neon Pink')
 for z in [1.81,2.43]:box('shop_neon_border',(-2.7,2.05,z),(1.48,.028,.024),'Neon Cyan',.011)
 box('neon_exit_backplate',(3.35,2.13,1.95),(.65,.09,.48),'Deep Teal',.07)
 japanese('neon_exit_japanese','出口',(3.35,2.07,1.95),.25,'Neon Amber')
 # Freestanding blade signs make the cyberpunk layer readable at gameplay scale.
 box('blade_sign_left',(-4.12,.85,1.6),(.5,.12,1.42),'Deep Teal',.09)
 for j,char in enumerate('修理'):
  japanese('blade_repair_'+str(j),char,(-4.12,.775,1.9-j*.48),.38,'Neon Pink')
 for x in [-4.35,-3.89]:box('blade_left_edge',(x,.77,1.6),(.025,.025,1.25),'Neon Cyan',.01)
 box('blade_sign_right',(4.12,1.1,1.62),(.5,.12,1.42),'Deep Teal',.09)
 for j,char in enumerate('夜市'):
  japanese('blade_market_'+str(j),char,(4.12,1.025,1.92-j*.48),.38,'Neon Cyan')
 for x in [3.89,4.35]:box('blade_right_edge',(x,1.02,1.62),(.025,.025,1.25),'Neon Pink',.01)
 # Visible foundation trim is decorative, below all collision surfaces.
 for x in [-4.27,4.27]:box('neon_foundation_side',(x,.8,-1.05),(.032,4.7,.033),'Neon Cyan',.015)
 box('neon_foundation_front',(0,-1.97,-1.08),(8.35,.03,.038),'Neon Pink',.017)
 for x in [-3.75,3.75]:
  box('neon_rear_upright',(x,2.22,1.2),(.028,.032,1.6),'Neon Cyan',.012)
 # A separate hanging lantern row varies with each arrangement.
 for i in range(5):
  x=-1.5+i*.75;z=2.7+.08*math.cos(i+cfg['id'])
  box('lantern_mount',(x,2.32,z+.18),(.017,.017,.25),'Copper Edge',.005)
  box('neon_lantern',(x,2.32,z),(.14,.14,.19),'Neon Amber' if i%2 else 'Neon Pink',.05)
 current=modules['workshop_frame']
 # Each scene has a native named spawn; Kaprao is linked separately at runtime.
 spawn=bpy.data.objects['ANCHOR_corgi_start'];spawn['character_scale']=1.0;spawn['character_visual_lift_m']=.007
 # Display title changes via new editable text meshes, preserving original sign position.
 old=bpy.data.objects.get('shop_sign_subtitle')
 if old:bpy.data.objects.remove(old,do_unlink=True)
 current=modules['workshop_frame'];text3('stage_subtitle',cfg['title'].upper(),(0,2.239,2.44),.078,'Copper Edge')
 bpy.context.view_layer.update()
 # Analytical held-beam aim reference, solving X-axis rotation for route depth.
 lo,hi=-.6,.6
 for _ in range(70):
  mid=(lo+hi)/2;y=1.2-1.2*math.cos(mid)+1.25*math.sin(mid)
  if y < -cfg['depth']:lo=mid
  else:hi=mid
 play=(lo+hi)/2
 hinge=modules['upper_chute'];beam=modules['bridge_beam'];held=bpy.data.objects['ANCHOR_held_beam_center']
 # This geometry check deliberately does not claim physics qualification.
 beamlo,beamhi=bounds(bpy.data.objects['COL_bridge_beam']);clear=[]
 for o in coll.objects:
  if o.name.startswith('COL_floor'):
   l,h=bounds(o);over=[min(beamhi[i],h[i])-max(beamlo[i],l[i]) for i in range(3)]
   assert not all(v>1e-6 for v in over),(o.name,over)
   clear.append({'name':o.name,'signed_overlap_source_xyz':over})
 assert abs(bpy.data.objects['COL_support_left_shelf'].matrix_world.translation.y+cfg['depth'])<1e-5
 # Export one merged mesh per module; all editable component geometry stays in .blend.
 runtime={}
 for name,root in modules.items():
  parts=[o for o in visible.objects if o.type=='MESH' and root in anc(o) and (name!='upper_chute' or modules['release_gate'] not in anc(o))]
  if not parts:continue
  copies=[]
  for part in parts:
   cp=part.copy();cp.data=part.data.copy();visible.objects.link(cp);copies.append(cp)
  select(copies);bpy.ops.object.join();joined=bpy.context.object
  joined.data.transform(root.matrix_world.inverted()@joined.matrix_world);joined.parent=root;joined.matrix_parent_inverse=Matrix.Identity(4);joined.matrix_basis=Matrix.Identity(4);joined.name=name+'_mesh';runtime[name]=joined
 def export(name,obs):
  select(obs)
  hidden=[(o,o.hide_render) for o in obs]
  for o in obs:o.hide_render=False
  bpy.ops.export_scene.gltf(filepath=str(d/'Exports'/(name+'.glb')),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_animations=False,export_cameras=False,export_lights=False,export_extras=True)
  bpy.ops.wm.usd_export(filepath=str(d/'Exports'/(name+'.usdc')),selected_objects_only=True,export_animation=False,export_materials=True,export_normals=True,generate_preview_surface=True,generate_materialx_network=False,convert_orientation=True,export_global_forward_selection='NEGATIVE_Z',export_global_up_selection='Y',export_textures_mode='KEEP',export_lights=False,export_cameras=False,triangulate_meshes=True,root_prim_path='/Stage',export_custom_properties=True)
  for o,was_hidden in hidden:o.hide_render=was_hidden
 export(cfg['slug']+'-assembled',list(modules.values())+list(runtime.values())+list(anchors.objects))
 for ob in coll.objects:ob.hide_render=False
 export(cfg['slug']+'-colliders',list(coll.objects)+list(modules.values()))
 for ob in coll.objects:ob.hide_render=True;ob.hide_set(True)
 for ob in runtime.values():bpy.data.objects.remove(ob,do_unlink=True)
 # Character remains a separately supplied sprite; previews show world geometry only.
 scene.frame_set(1);bpy.context.view_layer.update()
 scene.render.engine='CYCLES';scene.cycles.samples=8 if '--draft' in args else 32;scene.cycles.use_denoising=True
 try:
  prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
  for device in prefs.devices:device.use=device.type=='METAL'
  if any(o.type=='METAL' for o in prefs.devices):scene.cycles.device='GPU'
 except Exception:scene.cycles.device='CPU'
 scene.render.resolution_x=1920;scene.render.resolution_y=1280;scene.render.resolution_percentage=55 if '--draft' in args else 100
 scene.render.use_motion_blur=False;scene.render.image_settings.file_format='PNG'
 scene.world.node_tree.nodes['Background'].inputs[1].default_value=.38
 scene.camera=bpy.data.objects['CAM_workshop_main'];scene.camera.data.ortho_scale=13.5
 for n in ['warm_key','lavender_fill','soft_roof_rim']:
  o=bpy.data.objects.get(n)
  if o:o.data.energy*=.88 if n=='lavender_fill' else 1
 # Make the editable file self-contained. A shared native character remains the runtime path.
 for im in bpy.data.images:
  if im.source=='FILE' and not im.packed_file:
   try:im.pack()
   except Exception:pass
 bpy.context.preferences.filepaths.save_version=0
 bpy.ops.wm.save_as_mainfile(filepath=str(d/'Source'/(cfg['slug']+'.blend')))
 reports={'stage':cfg,'axis':'meters; runtime Y up, +X forward; Blender (X,Y,Z) maps to (X,Z,-Y)','character':{'source':'../../KapraoSprite/Runtime','scale':1.0,'visual_lift_m':.007,'runtime_separate':True},'anchors_game':{o.name:game(o.matrix_world.translation) for o in anchors.objects},'beam_core_game_dimensions_m':[2.9,.22,.54],'collider_boxes':len(coll.objects),'floor_clearance':clear,'play_reference_offset_degrees':math.degrees(play),'fold_reference_only':True,'physics_tested':False,'visual_triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in visible.objects if o.type=='MESH'),'module_count':len(modules),'fold_poses':[]}
 for i,offset in enumerate([play-math.radians(20),play,play+math.radians(20)],1):
  release=game((0,1.2-1.2*math.cos(offset)+1.25*math.sin(offset),3-1.2*math.sin(offset)-1.25*math.cos(offset)))
  reports['fold_poses'].append({'view':i,'offset_degrees':math.degrees(offset),'held_center_game':release,'depth_error_m':release[2]-cfg['depth']})
 if '--no-render' not in args:
  def render(name,cam):
   scene.camera=cam;scene.render.filepath=str(d/'Previews'/(name+'.png'));bpy.ops.render.render(write_still=True)
  render('hero',bpy.data.objects['CAM_workshop_main'])
 (d/'Validation/geometry.json').write_text(json.dumps(reports,indent=2)+'\n')
 print('STAGE_COMPLETE',cfg['slug'],flush=True)
