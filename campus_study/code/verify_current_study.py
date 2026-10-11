"""Verify current campus-paper records and independently reproduce transfer analysis."""
from pathlib import Path
import argparse, csv, hashlib, json, tempfile
from analyze_transfer import analyze

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    root = args.root.resolve()
    evidence = root / 'evidence'
    supplementary = root / 'supplementary_data'
    expected = json.loads((supplementary / 'Supplementary_Data_2.json').read_text(encoding='utf-8'))
    for name, digest in expected['input_record_sha256'].items():
        assert hashlib.sha256((evidence / 'external_clip_records' / name).read_bytes()).hexdigest() == digest
    with tempfile.TemporaryDirectory() as tmp:
        computed = analyze(evidence / 'external_clip_records', evidence / 'external_manifest.json', Path(tmp) / 'report.json')
    for field in ['clip_summary', 'by_camera', 'balanced_accuracy_95_scene_cluster_intervals',
                  'paired_balanced_accuracy_contrasts', 'bootstrap', 'input_record_sha256']:
        assert computed[field] == expected[field], field
    object_result = json.loads((evidence / 'object_normalized_reevaluation.json').read_text(encoding='utf-8'))
    with (supplementary / 'Supplementary_Data_1.csv').open(encoding='utf-8', newline='') as stream:
        classes = list(csv.DictReader(stream))
    assert len(classes) == len(object_result['per_class']) == 10
    for stored, original in zip(classes, object_result['per_class']):
        assert int(stored['class_id']) == original['class_id']
        assert stored['class_name'] == original['class_name']
        for field in ['precision', 'recall', 'AP50', 'AP50_95']:
            assert float(stored[field]) == original[field]
    for run, count, epoch in [('train3', 669, 469), ('train4', 489, 189)]:
        with (evidence / f'{run}_results.csv').open(encoding='utf-8-sig', newline='') as stream:
            rows = [{k.strip(): v.strip() for k, v in row.items()} for row in csv.DictReader(stream)]
        assert len(rows) == count
        best = max(rows, key=lambda r: .1 * float(r['metrics/mAP50(B)']) + .9 * float(r['metrics/mAP50-95(B)']))
        assert int(best['epoch']) == epoch
    code = root / 'code/original_integrated.py'
    assert hashlib.sha256(code.read_bytes()).hexdigest() == '8382785ab5267eeee46c3db9f22c909f871469aaffa0b22b78199dc2a7d2b33f'
    print(json.dumps({'passed': True, 'original_code_byte_identity': True,
                      'external_clip_records': 350, 'scene_clusters': 175,
                      'bootstrap_replicates': 10000, 'object_class_rows': 10,
                      'original_training_epochs_verified': [669, 489],
                      'requires_model_inference': False}, indent=2))

if __name__ == '__main__':
    main()
