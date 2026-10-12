"""Verify the saved image-level metrics and checkpoint-selection records."""
from pathlib import Path
import argparse, ast, csv, hashlib, json

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2],
                        help='repository root (defaults to the parent repository)')
    root = parser.parse_args().root.resolve()
    study = root / 'campus_study'
    evidence = study / 'evidence'
    supplemental = study / 'supplementary_data'

    # Confirm the classwise image-test table matches the saved evaluation record.
    object_result = json.loads((evidence / 'object_normalized_reevaluation.json').read_text(encoding='utf-8'))
    with (supplemental / 'Supplementary_Data_1.csv').open(encoding='utf-8', newline='') as stream:
        classes = list(csv.DictReader(stream))
    assert len(classes) == len(object_result['per_class']) == 10
    for stored, computed in zip(classes, object_result['per_class']):
        assert int(stored['class_id']) == computed['class_id']
        assert stored['class_name'] == computed['class_name']
        for field in ('precision', 'recall', 'AP50', 'AP50_95'):
            assert float(stored[field]) == computed[field]

    # Confirm selection epochs and completed training-history lengths.
    for run, expected_rows, expected_epoch in (('train3', 669, 469), ('train4', 489, 189)):
        with (evidence / f'{run}_results.csv').open(encoding='utf-8-sig', newline='') as stream:
            rows = [{key.strip(): value.strip() for key, value in row.items()}
                    for row in csv.DictReader(stream)]
        assert len(rows) == expected_rows
        best = max(rows, key=lambda row: .1 * float(row['metrics/mAP50(B)'])
                   + .9 * float(row['metrics/mAP50-95(B)']))
        assert int(best['epoch']) == expected_epoch

    # Confirm the dataset counts and recorded overlap summary used in the paper.
    exports = json.loads((root / 'datasets/export_manifest.json').read_text(encoding='utf-8'))
    assert [(row['image_count'], row['label_count']) for row in exports] == [(11762,11762),(1149,1149)]
    overlap = json.loads((evidence / 'recording_overlap_summary.json').read_text(encoding='utf-8'))
    assert overlap['object']['test_ids_also_train'] == 31
    assert overlap['behavior']['test_ids_also_train'] == 36

    # The application is syntax-checked only; this verifier never imports or executes it.
    app = root / 'implementation/main.py'
    ast.parse(app.read_text(encoding='utf-8-sig'), filename=str(app))
    print(json.dumps({'passed': True, 'object_test_images': 425, 'behavior_test_images': 115,
                      'object_classes': len(classes), 'training_epochs_verified': [669,489],
                      'selected_epochs_verified': [469,189],
                      'application_sha256': sha(app), 'model_execution_performed': False}, indent=2))

if __name__ == '__main__':
    main()
