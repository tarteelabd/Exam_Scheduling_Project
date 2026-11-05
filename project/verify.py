"""Verify feasibility, raw objectives, reference bounds, histories and summaries."""
from pathlib import Path
import argparse,itertools,json,statistics,math,hashlib
import numpy as np
from exams import neighbors,first_fit,exact_small
from optimizers import solve,SETTINGS
ROOT=Path(__file__).resolve().parent
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--rerun',action='store_true');ap.add_argument('--results',type=Path,default=ROOT/'results');args=ap.parse_args()
    data=json.loads((args.results/'experiment.json').read_text())
    cases={c['id']:c for c in data['cases']}
    for name,digest in data['metadata']['source_sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
    for case in cases.values():
        adj=neighbors(case)
        expected=sorted({(a,b) for exams in case['students'] for i,a in enumerate(exams) for b in exams[i+1:]})
        assert expected==[tuple(e) for e in case['edges']]
        clique=case['clique'];assert len(clique)==len(set(clique))
        assert all(b in adj[a] for a,b in itertools.combinations(clique,2))
        if case['reference']['kind']=='exact':
            # A valid coloring plus an equally large clique is an independent optimality certificate.
            colors=case['reference']['colors'];opt=case['reference']['value']
            assert max(colors)+1==opt and all(colors[a]!=colors[b] for a,b in expected)
            if len(clique)==opt:assert len(clique)==opt
            else:assert exact_small(adj)['value']==opt
        else:assert case['reference']['value']==len(clique)
    for row in data['runs']:
        case=cases[row['case']]
        colors,order=row['colors'],row['order']
        assert sorted(order)==list(range(case['n']))
        assert len(colors)==case['n'] and all(isinstance(x,int) and x>=0 for x in colors)
        assert all(colors[a]!=colors[b] for a,b in case['edges'])
        assert max(colors)+1==row['objective']
        # Independent first-fit replay on the stored order.
        replay=[-1]*case['n']
        for v in order:
            banned={replay[b] for a,b in case['edges'] if a==v and replay[b]>=0}|{replay[a] for a,b in case['edges'] if b==v and replay[a]>=0}
            color=0
            while color in banned:color+=1
            replay[v]=color
        assert colors==replay
        assert case['reference']['value']<=row['objective']<=case['baseline']
        assert row['evaluations']==SETTINGS['population']*(SETTINGS['iterations']+1)
        assert len(row['history'])==SETTINGS['iterations']+1
        assert row['history'][-1]==row['objective']
        assert all(b<=a for a,b in zip(row['history'],row['history'][1:]))
        ref=case['reference']['value'];objective=row['objective']
        assert math.isclose(row['gap_pct'],100*(objective-ref)/ref,abs_tol=1e-10)
        assert row['seconds']>=0
        if args.rerun and row['trial']==0:
            fresh=solve(case,row['algorithm'],row['seed'])
            for key in ['order','colors','objective','history','evaluations']:assert fresh[key]==row[key],(row['case'],row['algorithm'],key)
    for summary in data['summary']:
        rows=[x for x in data['runs'] if x['size']==summary['size'] and x['algorithm']==summary['algorithm']]
        ids=sorted({x['case'] for x in rows})
        expected={'runs':len(rows),'mean_objective':statistics.mean(x['objective'] for x in rows),
                  'best_objective':min(x['objective'] for x in rows),
                  'mean_gap_pct':statistics.mean(x['gap_pct'] for x in rows),
                  'mean_seconds':statistics.mean(x['seconds'] for x in rows),
                  'mean_within_case_sd':statistics.mean(statistics.stdev(x['objective'] for x in rows if x['case']==cid) for cid in ids)}
        for key,val in expected.items():assert math.isclose(summary[key],val,abs_tol=1e-10)
    print('PASS:',len(cases),'cases,',len(data['runs']),'runs; constraints, bounds, traces and summaries verified'+('; first runs reproduced' if args.rerun else ''))
if __name__=='__main__':main()
