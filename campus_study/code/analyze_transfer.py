"""Recompute original-detector AIRTLab transfer results from saved clip scores.

No training, inference, threshold fitting, or hardware measurements are performed.
Usage: python analyze_transfer.py --records PATH --manifest PATH --output PATH
"""
from pathlib import Path
from collections import defaultdict
import argparse, hashlib, json, math, random
from datetime import datetime, timezone

RULES = ('object_proxy', 'behavior', 'OR', 'AND')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def summarize(rows):
    out = {}
    for rule in RULES:
        counts = dict.fromkeys(('TP', 'FP', 'FN', 'TN'), 0)
        for row in rows:
            truth, pred = bool(row['label']), row['scores'][rule] >= .5
            counts['TP' if truth and pred else 'FN' if truth else 'FP' if pred else 'TN'] += 1
        tp, fp, fn, tn = (counts[k] for k in ('TP', 'FP', 'FN', 'TN'))
        positives = [row['scores'][rule] for row in rows if row['label'] == 1]
        negatives = [row['scores'][rule] for row in rows if row['label'] == 0]
        auc = sum((p > n) + .5 * (p == n) for p in positives for n in negatives) / (len(positives) * len(negatives))
        out[rule] = {**counts, 'precision': tp / (tp + fp) if tp + fp else None,
                     'recall': tp / (tp + fn), 'false_positive_fraction': fp / (fp + tn),
                     'F1': 2 * tp / (2 * tp + fp + fn),
                     'balanced_accuracy': .5 * (tp / (tp + fn) + tn / (fp + tn)),
                     'ROC_AUC': auc}
    return out

def percentile(values, q):
    values = sorted(values)
    pos = q * (len(values) - 1)
    lo = math.floor(pos)
    return values[lo] + (values[min(lo + 1, len(values) - 1)] - values[lo]) * (pos - lo)

def analyze(records_path, manifest_path, output_path, raw_video_root=None):
    paths = sorted(records_path.glob('*.json'))
    assert len(paths) == 350
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    identities = {row['path']: row for row in manifest['files']}
    assert len(identities) == 350
    rows, groups, receipts = [], defaultdict(list), {}
    for path in paths:
        row = json.loads(path.read_text(encoding='utf-8'))
        rel = Path(row['repository_path'])
        assert row['repository_path'] in identities
        assert row['video_sha256'] == identities[row['repository_path']]['sha256']
        assert row['label'] == int('non-violent' not in rel.parts)
        assert row['camera'] == rel.parent.name and row['camera'] in ('cam1', 'cam2')
        assert row['scene'] == f"{row['label']}_{rel.stem}"
        assert row['policy'] == 'original_stretch'
        assert row['settings'] == {'object': '640_fp32', 'behavior': '640_fp32'}
        assert len(row['samples']) == 3
        n = row['frame_count']
        # The historic script used numpy.rint(linspace(0, n-1, 3)).
        assert [s['frame'] for s in row['samples']] == [0, round((n - 1) / 2), n - 1]
        calculated = {'object_proxy': max(s['object'] for s in row['samples']),
                      'behavior': max(s['behavior'] for s in row['samples']),
                      'OR': max(max(s['object'], s['behavior']) for s in row['samples']),
                      'AND': max(min(s['object'], s['behavior']) for s in row['samples'])}
        assert calculated == row['scores']
        assert all(0 <= value <= 1 for value in calculated.values())
        if raw_video_root is not None:
            video = raw_video_root / row['repository_path']
            assert video.is_file() and sha(video) == row['video_sha256']
        rows.append(row)
        groups[row['scene']].append(row)
        receipts[path.name] = sha(path)
    assert len({row['repository_path'] for row in rows}) == 350
    assert len(groups) == 175 and all({r['camera'] for r in g} == {'cam1', 'cam2'} and len(g) == 2 for g in groups.values())
    by_label = {label: [g for g in groups.values() if g[0]['label'] == label] for label in (0, 1)}
    assert len(by_label[1]) == 115 and len(by_label[0]) == 60
    summary = summarize(rows)
    group_rates = {label: [[sum(row['scores'][rule] >= .5 for row in group) / 2 for rule in RULES]
                           for group in by_label[label]] for label in (0, 1)}
    rng = random.Random(20261011)
    resamples = {rule: [] for rule in RULES}
    contrasts = {'OR_minus_behavior': [], 'OR_minus_object_proxy': [], 'AND_minus_behavior': []}
    for _ in range(10000):
        sampled = {label: [group_rates[label][rng.randrange(len(group_rates[label]))] for _ in group_rates[label]] for label in (0, 1)}
        values = [.5 * (sum(r[k] for r in sampled[1]) / 115 + 1 - sum(r[k] for r in sampled[0]) / 60) for k in range(4)]
        for rule, value in zip(RULES, values):
            resamples[rule].append(value)
        contrasts['OR_minus_behavior'].append(values[2] - values[1])
        contrasts['OR_minus_object_proxy'].append(values[2] - values[0])
        contrasts['AND_minus_behavior'].append(values[3] - values[1])
    intervals = {rule: [percentile(values, .025), percentile(values, .975)] for rule, values in resamples.items()}
    differences = {name: {'difference_pp': 100 * (summary['OR' if name.startswith('OR') else 'AND']['balanced_accuracy'] - summary['behavior' if name.endswith('behavior') else 'object_proxy']['balanced_accuracy']),
                         'percentile_95_interval_pp': [100 * percentile(values, .025), 100 * percentile(values, .975)]}
                   for name, values in contrasts.items()}
    record = {'analysis_utc': datetime.now(timezone.utc).isoformat(),
              'scope': 'Secondary analysis of existing 3 October 2026 original-stretch detector outputs; no new inference or training.',
              'dataset': 'AIRTLab', 'repository': manifest['repository'], 'revision': manifest['revision'],
              'clips': 350, 'positive_clips': 230, 'negative_clips': 120, 'paired_scene_clusters': 175,
              'frames_per_clip': 3, 'threshold': .5, 'policy': 'original_stretch',
              'score_rules': {'object_proxy': 'maximum object confidence over the three frames', 'behavior': 'maximum behavior confidence over the three frames',
                              'OR': 'maximum framewise maximum of object and behavior confidence', 'AND': 'maximum framewise minimum of object and behavior confidence'},
              'clip_summary': summary, 'by_camera': {cam: summarize([r for r in rows if r['camera'] == cam]) for cam in ('cam1', 'cam2')},
              'balanced_accuracy_95_scene_cluster_intervals': intervals,
              'paired_balanced_accuracy_contrasts': differences,
              'bootstrap': {'replicates': 10000, 'seed': 20261011, 'method': 'Label-stratified percentile bootstrap of the 115 positive and 60 negative scene pairs; both camera views kept together; all four rules evaluated on the same resample.',
                            'limitation': 'Conditional on known scene grouping; unknown actor/session dependence and original training-source overlap remain unresolved. No recording-level campus generalization interval is inferred.'},
              'raw_video_hashes_verified': raw_video_root is not None, 'input_record_sha256': receipts,
              'external_manifest_sha256': sha(manifest_path), 'analysis_code_sha256': sha(Path(__file__)),
              'interpretation': 'Clip-label screening, not actor box AP, actor-object association, event localization, or false alerts per camera-hour. Object proxy is a baseline cue, not a definition of violence. No threshold fitting on AIRTLab.'}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(record, indent=2), encoding='utf-8')
    return record

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--records', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--verify-video-root', type=Path)
    args = parser.parse_args()
    report = analyze(args.records, args.manifest, args.output, args.verify_video_root)
    print(json.dumps({key: report[key] for key in ('clip_summary', 'balanced_accuracy_95_scene_cluster_intervals', 'paired_balanced_accuracy_contrasts', 'raw_video_hashes_verified')}, indent=2))

if __name__ == '__main__':
    main()
