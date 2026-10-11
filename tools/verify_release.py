"""Verify original code/data records without loading or executing detector models."""
from pathlib import Path
import ast, hashlib, json
ROOT = Path(__file__).resolve().parents[1]
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    manifest = json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    for name, expected in manifest['sha256'].items():
        assert sha(ROOT/name) == expected, name
    expected = '8382785ab5267eeee46c3db9f22c909f871469aaffa0b22b78199dc2a7d2b33f'
    assert sha(ROOT/'implementation/main.py') == expected
    assert sha(ROOT/'campus_study/code/original_integrated.py') == expected
    scripts = sorted(ROOT.rglob('*.py'))
    for path in scripts:
        ast.parse(path.read_text(encoding='utf-8-sig'),filename=str(path))
    for branch,run in [('object','train3'),('behavior','train4')]:
        for name,mirror in [('args.yaml',f'{run}_args.yaml'),('results.csv',f'{run}_results.csv')]:
            assert sha(ROOT/f'training/{branch}/{name}') == sha(ROOT/f'campus_study/evidence/{mirror}')
    datasets = json.loads((ROOT/'datasets/export_manifest.json').read_text())
    assert [(r['image_count'],r['label_count']) for r in datasets] == [(11762,11762),(1149,1149)]
    assert not (ROOT/'paper').exists()
    forbidden = [p for p in ROOT.rglob('*') if p.is_file() and p.suffix.lower() in {'.tex','.bib','.bst','.cls','.pdf','.jpg','.mp4','.avi'}]
    assert not forbidden, forbidden
    print(json.dumps({'passed':True,'source_files':len(manifest['sha256']),
                      'original_code_byte_identity':True,'python_sources_parsed':len(scripts),
                      'manuscript_files_hosted':False,'dataset_pixels_hosted':False,
                      'model_execution_performed':False},indent=2))
if __name__ == '__main__':
    main()
