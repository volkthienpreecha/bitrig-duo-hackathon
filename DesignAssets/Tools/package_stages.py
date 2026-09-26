"""Bundle only current assets; excludes rejected characters, private photos and app code."""
from pathlib import Path
import json,hashlib,zipfile
B=Path(__file__).resolve().parents[1];O=B.parent/'outputs';O.mkdir(exist_ok=True)
def allowed(p):return p.is_file() and p.suffix not in ['.blend1','.pyc'] and p.name not in ['.DS_Store','kaprao-rodin-inspected.blend'] and 'MotionFrames' not in p.parts and '__pycache__' not in p.parts
def files(paths):return sorted(set(p for q in paths for p in ([q] if q.is_file() else q.rglob('*')) if allowed(p)))
toolnames=['package_execution_kit.py','verify_preparation.py','stages_build.py','stages_validate.py','stages_native_validate.swift','stages_design.py','stages_render_design.cjs','package_stages.py','workshop_build.py','ui_assets.py','ui_render.cjs','convert_scenekit.swift','kaprao_refine_v3.py','kaprao_inspect_v3.py','kaprao_validate_v3.py','kaprao_source_validate_v3.py','kaprao_preview_clips_v3.py','package_kaprao_v3.py','probe_scenekit_animation.swift']
full=files([B/'Stages',B/'Revisions/Kaprao-v3',B/'UI',B/'Palette',B/'Licenses',B/'Runtime/Audio',B/'Source/Workshop',B/'README.md',B/'INTEGRATION.md',B/'ART-DIRECTION.md',B/'DEMO-ASSET-CHECKLIST.md',B/'Concepts/kaprao-authoritative-furred-reference.png']+[B/'Tools'/t for t in toolnames])
runtime=files([B/'Revisions/Kaprao-v3/Runtime/Kaprao',B/'Runtime/Audio',B/'Licenses',B/'Stages/runtime-setup.txt']+list((B/'Stages').glob('0*/Runtime'))+list((B/'Stages').glob('0*/Validation/geometry.json')))
results=[]
for label,selected in [('Full',full),('Runtime',runtime)]:
 out=O/f'FoldAndFetch-ThreeStages-{label}.zip'
 manifest=[{'path':str(p.relative_to(B)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in selected]
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  z.writestr('START-HERE.txt','Fold & Fetch / three-stage asset handoff\n\nChoose one stage visual SCN and matching collider SCN under DesignAssets/Stages.\nUse the shared Kaprao v3 SCNs under DesignAssets/Revisions/Kaprao-v3/Runtime/Kaprao.\nSpawn at ANCHOR_corgi_start, visual scale 0.72, lift 0.007m.\nThe stage beam is 0.54m deep; old 0.35m colliders do not match.\nRuntime uses embedded materials/textures. Do not bundle this whole archive as app resources.\nNative asset tests pass; gameplay and connected Duo projection are not implemented here.\n')
  z.writestr('MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
  for p in selected:z.write(p,Path('DesignAssets')/p.relative_to(B))
 with zipfile.ZipFile(out) as z:
  assert z.testzip() is None
  assert len(z.namelist())==len(set(z.namelist()))
  assert len([n for n in z.namelist() if n.endswith('.scn')])==11
  assert not any('/Kaprao-v2/' in n or '/Source/Kaprao/' in n and '/Kaprao-v3/' not in n or '/References/' in n for n in z.namelist())
 results.append({'archive':out.name,'bytes':out.stat().st_size,'files':len(selected),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'crc':'pass','native_scenes':11})
(O/'FoldAndFetch-ThreeStages-verification.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
