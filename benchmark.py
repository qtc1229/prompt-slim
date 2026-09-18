"""Run real local compression. No cloud calls. Quality must be reviewed separately."""
import argparse
import json
import time
from pathlib import Path
from app import compress

parser=argparse.ArgumentParser()
parser.add_argument('--model',default='qwen3:4b')
parser.add_argument('--output',default='evals/results.json')
args=parser.parse_args()
cases=json.loads(Path('evals/cases.json').read_text(encoding='utf-8'))
rows=[]
for case in cases:
    start=time.monotonic()
    try:
        result=compress({'text':case['text'],'model':args.model,'protected':'\n'.join(case['protected'])})
        rows.append(dict(case, result=result, wall_seconds=round(time.monotonic()-start,2), semantic_review='pending'))
        print(case['id'],result['original_tokens'],result['compressed_tokens'],'fallback',result['fallback'],flush=True)
    except Exception as error:
        rows.append(dict(case,error=str(error)))
        print(case['id'],'ERROR',str(error),flush=True)
    Path(args.output).write_text(json.dumps({'model':args.model,'encoding':'o200k_base','quality_claim':'No downstream quality evaluation; literal checks only.','cases':rows},ensure_ascii=False,indent=2),encoding='utf-8')