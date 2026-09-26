"""Check the preparation contract and refresh local UI evidence; no game tests."""
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'DesignAssets'


def check():
    master_path = ROOT / 'Preparation/FoldAndFetch-Bitrig/Master-Prompt.md'
    master = master_path.read_text()
    assert 'Version 1.4' in master
    assert 'No second level/puzzle' not in master
    for phrase in ['seated display pose', 'empty gap', 'Optional progression gate',
                   '0.045 m', 'labeled **Retry**', 'lower-right', 'Toy reached!',
                   'FoldAndFetch-OneShot.zip']:
        assert phrase in master, phrase
    for target in re.findall(r'\]\(([^)]+)\)', master):
        if '://' not in target:
            assert (master_path.parent / target.split('#')[0]).exists(), target

    required = []
    for slug in ['01-workshop', '02-garden', '03-terrace']:
        folder = ASSETS / 'Stages' / slug
        for suffix in ['assembled', 'colliders']:
            required.append(folder / 'Runtime' / f'{slug}-{suffix}.scn')
        geometry = json.loads((folder / 'Validation/geometry.json').read_text())
        assert geometry['beam_core_game_dimensions_m'] == [2.9, .22, .54]
        assert geometry['character']['scale'] == .72
        assert geometry['physics_tested'] is False
    for clip in ['static', 'Idle_Look', 'Walk_InPlace', 'Jump_Fall', 'Celebrate']:
        required.append(ASSETS / 'Revisions/Kaprao-v3/Runtime/Kaprao' / f'kaprao-{clip}.scn')
    for name in ['step_soft', 'jump', 'land_soft', 'dash_down', 'mechanism_release',
                 'bridge_land', 'success', 'retry']:
        required.append(ASSETS / 'Runtime/Audio' / f'{name}.wav')
    assert all(p.is_file() and p.stat().st_size > 0 for p in required)

    def walk(nodes):
        for node in nodes:
            yield node
            yield from walk(node.get('children', []))

    def bounds(nodes, width, height):
        for n in nodes:
            w = n.get('w', len(n.get('text', '')) * n.get('size', 16) * .52)
            h = n.get('h', n.get('size', 16) * 1.25)
            assert 0 <= n.get('x', 0) and 0 <= n.get('y', 0), n['name']
            assert n.get('x', 0) + w <= width + .01, n['name']
            assert n.get('y', 0) + h <= height + .01, n['name']
            if 'action' in n['name'] or 'control' in n['name']:
                assert w >= 44 and h >= 44, n['name']
            bounds(n.get('children', []), w, h)

    shared = json.loads((ASSETS / 'UI/ui-spec.json').read_text())
    stages = json.loads((ASSETS / 'UI/Stages/stage-ui-spec.json').read_text())
    results = []
    for name, state in list(shared['states'].items()) + list(stages['states'].items()):
        nodes = state['overlay']
        bounds(nodes, 1080, 720)
        labels = [n.get('text') for n in walk(nodes)]
        if name.endswith('gameplay'):
            assert 'Retry' in labels and 'Release' in labels, name
            retry = next(n for n in nodes if n['name'] == 'Retry action')
            release = next(n for n in nodes if n['name'] == 'Release action')
            assert release['x'] - (retry['x'] + retry['w']) >= 8
        if name == 'completion':
            assert 'Toy reached!' in labels and 'Replay rooftop' in labels
        if name == 'pause':
            assert 'Replay rooftop' in labels and 'Restart' not in labels
        results.append({'state': name, 'reference_bounds_and_targets': 'pass',
                        'actual_device_safe_regions_tested': False})
    svg_files = list((ASSETS / 'UI').rglob('*.svg'))
    for path in svg_files:
        ET.parse(path)
    assert all(v >= 4.5 for v in json.loads((ASSETS / 'Validation/ui-contrast.json').read_text())['ratios'].values())

    report = {'scope': 'Preparation files only; no build, physics or simulator tests run',
              'master_version': '1.4', 'runtime_files': len(required),
              'master_local_links': 'pass', 'ui_svg_xml_files': len(svg_files),
              'states': results, 'gameplay_verified': False}
    (ROOT / 'Preparation/FoldAndFetch-Bitrig/Review/preparation-readiness.json').write_text(json.dumps(report, indent=2) + '\n')
    (ASSETS / 'UI/Stages/validation.json').write_text(json.dumps({
        'scope': report['scope'], 'states': results[3:], 'xml': 'pass',
        'visual_review': 'See preparation-readiness.md for separate visual inspection.',
        'figma': 'No live sync attempted; previous quota limitation remains historical evidence.'
    }, indent=2) + '\n')
    manifest_path = ASSETS / 'UI/Stages/figma-import-manifest.json'
    manifest = json.loads(manifest_path.read_text())
    for entry in manifest['files']:
        entry['sha256'] = hashlib.sha256((manifest_path.parent / entry['file']).read_bytes()).hexdigest()
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    check()
