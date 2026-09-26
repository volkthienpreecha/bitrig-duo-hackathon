"""Package the v3 replacement without rejected characters or personal photographs."""
from pathlib import Path
import hashlib,json,zipfile
assets=Path(__file__).resolve().parents[1];root=assets/'Revisions/Kaprao-v3'
outputs=assets.parent/'outputs';outputs.mkdir(exist_ok=True)
files=[]
for p in root.rglob('*'):
    if not p.is_file() or 'MotionFrames' in p.parts or p.suffix in ('.blend1','.pyc') or p.name=='.DS_Store':continue
    if p.name in ('kaprao-rodin-inspected.blend','package-content.json'):continue
    files.append(p)
tools=['kaprao_refine_v3.py','kaprao_inspect_v3.py','kaprao_preview_clips_v3.py','kaprao_validate_v3.py','kaprao_source_validate_v3.py','convert_scenekit.swift','probe_scenekit_animation.swift','package_kaprao_v3.py']
files.extend(assets/'Tools'/n for n in tools)
manifest=[{'path':str(p.relative_to(assets)), 'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)]
(root/'Validation/package-content.json').write_text(json.dumps(manifest,indent=2)+'\n')
files.append(root/'Validation/package-content.json')
out=outputs/'FoldAndFetch-Kaprao-v3.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    z.writestr('START-HERE.txt','Kaprao v3 replacement\n\nRead DesignAssets/Revisions/Kaprao-v3/README.md.\nUse its Runtime/Kaprao SCN files instead of the rejected character in the original asset ZIP.\nThe existing workshop, UI and sounds remain unchanged.\nSource/Kaprao/kaprao.blend is editable; Previews contains actual model renders and motion GIFs.\nVerification covers native simulator asset loading/rendering, not final gameplay or physical-device performance.\n')
    for p in sorted(files):z.write(p,Path('DesignAssets')/p.relative_to(assets))
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    assert any(n.endswith('/kaprao.blend') for n in z.namelist())
    assert len([n for n in z.namelist() if n.endswith('.scn')])==5
    assert not any('/Kaprao-v2/' in n or '/MotionFrames/' in n for n in z.namelist())
report={'archive':str(out),'bytes':out.stat().st_size,'entries':len(files)+1,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'crc':'pass'}
(outputs/'FoldAndFetch-Kaprao-v3-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
