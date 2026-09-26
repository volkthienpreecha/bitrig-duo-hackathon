"""Build a current one-prompt context archive, not an app resource bundle."""
from pathlib import Path
import hashlib
import json
import zipfile
from verify_preparation import check

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'DesignAssets'
OUTPUT = ROOT / 'outputs'


def package():
    check()
    selected = set()

    def add(path):
        assert path.exists(), path
        for p in ([path] if path.is_file() else path.rglob('*')):
            if p.is_file() and p.name != '.DS_Store' and p.suffix != '.pyc' and '__pycache__' not in p.parts and not p.name.endswith('-concept.svg'):
                selected.add(p)

    for name in ['AGENTS.md', 'README.md', 'CONTRIBUTING.md', 'outputs/README.md']:
        add(ROOT / name)
    add(ROOT / 'Preparation/FoldAndFetch-Bitrig')
    # Include instruction documents, including clearly labeled historical context.
    for path in ASSETS.rglob('*.md'):
        if 'Kaprao-v2' not in path.parts and 'Kaprao-v4' not in path.parts:
            add(path)
    for name in ['Runtime/Audio', 'Licenses', 'UI', 'Palette',
                 'Revisions/Kaprao-v3/Runtime/Kaprao',
                 'Revisions/Kaprao-v3/Validation',
                 'Concepts/kaprao-authoritative-furred-reference.png',
                 'Revisions/Kaprao-v3/Previews/kaprao-hero.png',
                 'Revisions/Kaprao-v3/Previews/kaprao-turnaround.png',
                 'Stages/three-stages.png', 'Stages/runtime-setup.txt',
                 'Stages/validation-summary.json', 'Stages/native-validation.json',
                 'Tools/package_execution_kit.py', 'Tools/verify_preparation.py',
                 'Tools/ui_assets.py', 'Tools/ui_render.cjs',
                 'Tools/stages_design.py', 'Tools/stages_render_design.cjs']:
        add(ASSETS / name)
    for folder in sorted((ASSETS / 'Stages').glob('0*')):
        add(folder / 'Runtime')
        add(folder / 'Validation')
        for name in ['hero.png', 'fold-02.png', 'fold-storyboard.png',
                     'layout-top.png', 'layout-top.svg', 'layout-side.png', 'layout-side.svg']:
            add(folder / 'Previews' / name)
    files = sorted(selected)
    manifest = [{'path': p.relative_to(ROOT).as_posix(), 'bytes': p.stat().st_size,
                 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
    OUTPUT.mkdir(exist_ok=True)
    out = OUTPUT / 'FoldAndFetch-OneShot.zip'
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        archive.writestr('START-HERE.txt',
            'Corgi Crossroads / current execution context / master v1.4\n\n'
            'Extract this archive. Read AGENTS.md, then execute the exact\n'
            'Preparation/FoldAndFetch-Bitrig/Master-Prompt.md only when the user\n'
            'requests the build and the event coding window permits it.\n'
            'This is the same master as the repository, not a second prompt.\n'
            'Execution is on hold until the user gives a new explicit build signal.\n'
            'One coordinator; Workshop required, other stages conditional.\n'
            'Use v3 character and matched stage SCNs; never the old DesignAssets ZIP.\n'
            'Assembly beam is seated for display: initialize it held with an empty gap.\n'
            'This archive is build context, not a folder to bundle into the app.\n'
            'Blender/exchange sources and some historical evidence links remain\n'
            'repository-only. Editable overlay SVGs, specs and concept PNGs are included;\n'
            'large concept SVGs with duplicate embedded backgrounds are omitted.\n'
            'All selected runtime resources are here.\n'
            'Preparation checks do not establish a working game.\n')
        archive.writestr('MANIFEST.json', json.dumps(manifest, indent=2) + '\n')
        for p, record in zip(files, manifest):
            archive.write(p, record['path'])
    with zipfile.ZipFile(out) as archive:
        assert archive.testzip() is None
        names = archive.namelist()
        assert len(names) == len(set(names))
        assert len([n for n in names if n.endswith('.scn')]) == 11
        assert len([n for n in names if n.startswith('DesignAssets/Runtime/Audio/') and n.endswith('.wav')]) == 8
        assert not any('/Kaprao-v2/' in n or n.startswith('DesignAssets/Runtime/Kaprao/') for n in names)
        assert not any(n.endswith(('.blend', '.glb', '.usdc')) for n in names)
        for record in manifest:
            assert hashlib.sha256(archive.read(record['path'])).hexdigest() == record['sha256']
    result = {'archive': out.name, 'files': len(files), 'bytes': out.stat().st_size,
              'sha256': hashlib.sha256(out.read_bytes()).hexdigest(),
              'master_sha256': hashlib.sha256((ROOT / 'Preparation/FoldAndFetch-Bitrig/Master-Prompt.md').read_bytes()).hexdigest(),
              'crc_and_all_entry_hashes': 'pass', 'native_scenes': 11,
              'current_runtime_wavs': 8, 'gameplay_verified': False}
    (OUTPUT / 'FoldAndFetch-OneShot-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    package()
