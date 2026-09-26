"""Render existing workshop source, without rebuilding or rewriting exchange assets.
Blender -b --python workshop_render.py -- --all-renders [--remaining]
--remaining skips the already-completed wide/detail views and renders layouts/folds.
Uses Metal if available, otherwise leaves Cycles on CPU.
"""
import bpy,math,sys
from pathlib import Path
from mathutils import Matrix,Vector
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'Source'/'Workshop';PREVIEW=BASE/'Previews'/'Workshop'
bpy.ops.wm.open_mainfile(filepath=str(SOURCE/'fold-and-fetch-workshop.blend'))
scene=bpy.context.scene
try:
    prefs=bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type='METAL';prefs.get_devices()
    for device in prefs.devices:device.use=device.type=='METAL'
    if any(d.type=='METAL' for d in prefs.devices):scene.cycles.device='GPU'
except (TypeError,RuntimeError):scene.cycles.device='CPU'
visible=bpy.data.collections['00_WORKSHOP_VISIBLE']
modules={o.name:o for o in visible.objects if o.type=='EMPTY' and o.get('asset_role')}
beam=bpy.data.objects['bridge_beam'];hinge=bpy.data.objects['upper_chute']
cameras={key:bpy.data.objects[name] for key,name in {
 'workshop-main':'CAM_workshop_main','workshop-detail-bridge':'CAM_bridge_detail',
 'workshop-detail-rooftop':'CAM_rooftop_detail','layout-top':'CAM_layout_top',
 'layout-side':'CAM_layout_side','layout-front':'CAM_layout_front','fold':'CAM_fold_reference'}.items()}
cam=cameras['workshop-main'];stage=bpy.data.collections['99_DESIGN_PREVIEW_ONLY']
M={mat.name:mat for mat in bpy.data.materials}
def ancestors(o):
    result=[];p=o.parent
    while p:result.append(p);p=p.parent
    return result
# Reuse the exact authored materials and rendering annotations from the build script.
source=(BASE/'Tools/workshop_build.py').read_text()
helpers=source[source.index('def srgb('):source.index('for name,h in palette.items():')]
exec(compile(helpers,'workshop_material_helpers','exec'))
rendering=source[source.index('# Render routes can be selected'):]
rendering=rendering.replace("render('workshop-main-draft' if draft else 'workshop-main','workshop-main')", "if '--remaining' not in args and '--layout-labels-only' not in args:render('workshop-main-draft' if draft else 'workshop-main','workshop-main')")
rendering=rendering.replace("for name in ['workshop-detail-bridge','workshop-detail-rooftop']:render(name,name)", "for name in ([] if '--remaining' in args or '--layout-labels-only' in args else ['workshop-detail-bridge','workshop-detail-rooftop']):render(name,name)")
rendering=rendering.replace("render('layout-side','layout-side');render('layout-front','layout-front')", "if '--layout-labels-only' not in args:render('layout-side','layout-side')\n    render('layout-front','layout-front')")
rendering=rendering.replace("    beam.matrix_world.translation=(0,0,1.75)", "    if '--layout-labels-only' in args:clear_overlays();sys.exit(0)\n    beam.matrix_world.translation=(0,0,1.75)")
exec(compile(rendering,'workshop_render_views','exec'))
