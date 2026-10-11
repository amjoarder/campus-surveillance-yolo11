"""Reproduce joint-cue counts from saved outputs; no detector inference."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def main():
    rows = [json.loads(path.read_text()) for path in sorted((ROOT / 'campus_study/evidence/external_clip_records').glob('*.json'))]
    counts = {label:dict(object_only=0, behavior_only=0, both_somewhere=0, neither=0, same_frame_subset=0)
              for label in ['violent', 'nonviolent']}
    for row in rows:
        key = 'violent' if row['label'] else 'nonviolent'
        obj = row['scores']['object_proxy'] >= .5
        behavior = row['scores']['behavior'] >= .5
        state = 'both_somewhere' if obj and behavior else 'object_only' if obj else 'behavior_only' if behavior else 'neither'
        counts[key][state] += 1
        counts[key]['same_frame_subset'] += int(row['scores']['AND'] >= .5)
    assert len(rows) == 350
    assert counts == {'violent':{'object_only':30,'behavior_only':74,'both_somewhere':14,'neither':112,'same_frame_subset':6},
                      'nonviolent':{'object_only':4,'behavior_only':50,'both_somewhere':2,'neither':64,'same_frame_subset':2}}
    print(json.dumps({'passed':True, 'joint_cue_counts':counts,
                      'OR_minus_behavior_sensitivity_pp':100*30/230,
                      'OR_minus_behavior_false_positive_fraction_pp':100*4/120,
                      'violent_both_at_different_sampled_times_only':8,
                      'model_execution_performed':False}, indent=2))

if __name__ == '__main__':
    main()
