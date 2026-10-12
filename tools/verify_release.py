"""Generate or verify the release integrity manifest without running models."""
from pathlib import Path
import argparse, ast, hashlib, json, subprocess
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'SOURCE_MANIFEST.json'
EXCLUDED_DIRS = {'.git', '__pycache__', '.venv', '.pytest_cache'}
EXCLUDED_FILES = {'SOURCE_MANIFEST.json'}
FORBIDDEN_SUFFIXES = {'.tex', '.bib', '.bst', '.cls', '.pdf', '.jpg', '.jpeg', '.mp4', '.avi'}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def files_to_hash():
    tracked = subprocess.run(
        ['git', 'ls-files', '--cached', '--others', '--exclude-standard'],
        cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.splitlines()
    for name in sorted(tracked):
        path = ROOT / name
        if not path.is_file() or path.name in EXCLUDED_FILES or path.suffix.lower() == '.pyc':
            continue
        if any(part in EXCLUDED_DIRS for part in path.relative_to(ROOT).parts):
            continue
        yield path.relative_to(ROOT).as_posix(), path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-manifest', action='store_true',
                        help='refresh SOURCE_MANIFEST.json from the current source tree')
    args = parser.parse_args()
    inventory = list(files_to_hash())
    current = {name: sha(path) for name, path in inventory}
    if args.write_manifest:
        MANIFEST.write_text(json.dumps({'format':'sha256','sha256':current}, indent=2)+'\n',
                            encoding='utf-8', newline='\n')
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    assert manifest.get('sha256') == current, 'source integrity manifest is stale; rerun with --write-manifest'
    excluded_term = 'air' + 'tlab'
    for name, path in inventory:
        if path.suffix.lower() in {'.md','.py','.json','.yml','.cff'}:
            assert excluded_term not in path.read_text(encoding='utf-8-sig').lower(), name
    scripts = sorted(path for _, path in inventory if path.suffix.lower() == '.py')
    for path in scripts:
        ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
    for branch, run in (('object','train3'),('behavior','train4')):
        for name, mirror in (('args.yaml',f'{run}_args.yaml'),('results.csv',f'{run}_results.csv')):
            assert sha(ROOT/f'training/{branch}/{name}') == sha(ROOT/f'campus_study/evidence/{mirror}')
    datasets = json.loads((ROOT/'datasets/export_manifest.json').read_text(encoding='utf-8'))
    assert [(row['image_count'],row['label_count']) for row in datasets] == [(11762,11762),(1149,1149)]
    assert not (ROOT/'paper').exists()
    forbidden = [path for _, path in inventory if path.suffix.lower() in FORBIDDEN_SUFFIXES]
    assert not forbidden, forbidden
    print(json.dumps({'passed':True,'source_files':len(current),'python_sources_parsed':len(scripts),
                      'manuscript_files_hosted':False,'dataset_pixels_hosted':False,
                      'model_execution_performed':False}, indent=2))

if __name__ == '__main__':
    main()
