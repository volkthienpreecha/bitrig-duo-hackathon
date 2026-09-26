"""Package completed asset deliverables; exclude personal references and intermediates."""
from pathlib import Path
import hashlib,json,zipfile
root=Path(__file__).resolve().parents[1]
out=root.parent/'outputs';out.mkdir(exist_ok=True)
excluded={'References','MotionFrames','__pycache__'}
names={'duo-initial.png','duo-loaded.png','workshop-main-draft.png'}
files=sorted(p for p in root.rglob('*') if p.is_file() and not any(s in excluded for s in p.relative_to(root).parts) and p.name not in names and not p.name.endswith(('.blend1','.pyc','.DS_Store')))
manifest=[]
for p in files:
 if p.name=='runtime-manifest.json':continue
 if 'Runtime' in p.relative_to(root).parts and p.suffix in {'.scn','.wav'}:
  manifest.append({'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
mp=root/'Validation/runtime-manifest.json';mp.write_text(json.dumps({'files':manifest,'total_bytes':sum(x['bytes'] for x in manifest)},indent=2)+'\n')
files=sorted(set(files+[mp]))
z=out/'FoldAndFetch-DesignAssets.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
 for p in files:archive.write(p,Path('DesignAssets')/p.relative_to(root))
with zipfile.ZipFile(z) as archive:
 assert archive.testzip() is None
 assert not any('/References/' in n or '/MotionFrames/' in n for n in archive.namelist())
result={'archive':str(z),'entries':len(files),'bytes':z.stat().st_size,'sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'crc':'pass','runtime_files':len(manifest),'runtime_bytes':sum(x['bytes'] for x in manifest)}
(out/'FoldAndFetch-DesignAssets-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
