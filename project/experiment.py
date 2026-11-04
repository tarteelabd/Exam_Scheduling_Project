"""Run the documented experiment and save raw results before writing the report."""
from pathlib import Path
import argparse,csv,json,time,statistics,platform,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exams import make_case,neighbors,degree_order,first_fit,clique_bound,exact_small
from optimizers import solve,SETTINGS
ROOT=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--runs',type=int,default=10)
    parser.add_argument('--output',type=Path,default=ROOT/'results')
    args=parser.parse_args()
    if args.runs<2:parser.error('Use at least two independent runs')
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    cases,records=[],[]
    for size in ['Small','Medium','Large']:
        for replicate in [0,1]:
            case=make_case(size,replicate)
            adj=neighbors(case)
            case['baseline_colors'],case['baseline']=first_fit(degree_order(adj),adj)
            clique=clique_bound(adj)
            case['clique']=clique
            case['reference']=exact_small(adj) if case['n']<=16 else {'kind':'lower_bound','value':len(clique)}
            cases.append(case)
            for algorithm in ['GA','PSO','ACO']:
                for trial in range(args.runs):
                    seed=10000+100*len(cases)+trial
                    before=time.perf_counter()
                    result=solve(case,algorithm,seed)
                    elapsed=time.perf_counter()-before
                    ref=case['reference']['value']
                    objective=result['objective']
                    gap=100*(objective-ref)/ref
                    records.append({'case':case['id'],'size':size,'algorithm':algorithm,
                                    'trial':trial,'seed':seed,'seconds':elapsed,'gap_pct':gap,**result})
                print(case['id'],algorithm,'finished',flush=True)
    summary=[]
    for size in ['Small','Medium','Large']:
        ids=[c['id'] for c in cases if c['size']==size]
        for algorithm in ['GA','PSO','ACO']:
            rows=[r for r in records if r['size']==size and r['algorithm']==algorithm]
            within=[statistics.stdev(r['objective'] for r in rows if r['case']==cid) for cid in ids]
            summary.append({'size':size,'algorithm':algorithm,'runs':len(rows),
                            'mean_objective':statistics.mean(r['objective'] for r in rows),
                            'best_objective':min(r['objective'] for r in rows),
                            'mean_within_case_sd':statistics.mean(within),
                            'mean_gap_pct':statistics.mean(r['gap_pct'] for r in rows),
                            'mean_seconds':statistics.mean(r['seconds'] for r in rows)})
    metadata={'python':platform.python_version(),'numpy':np.__version__,'matplotlib':matplotlib.__version__,
              'runs_per_case':args.runs,'parameters':SETTINGS,
              'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('*.py')}}
    payload={'metadata':metadata,'cases':cases,'runs':records,'summary':summary}
    (out/'experiment.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    for name,rows in [('summary.csv',summary),('trials.csv',[{k:v for k,v in r.items() if not isinstance(v,list)} for r in records])]:
        with (out/name).open('w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    colors={'GA':'#2474A1','PSO':'#C55A28','ACO':'#32824A'}
    fig,axes=plt.subplots(1,3,figsize=(11,3.4))
    for ax,size in zip(axes,['Small','Medium','Large']):
        cid=next(c['id'] for c in cases if c['size']==size)
        for algorithm in ['GA','PSO','ACO']:
            traces=[r['history'] for r in records if r['case']==cid and r['algorithm']==algorithm]
            mean=np.mean(traces,axis=0)
            ax.plot(np.arange(len(mean)),mean,label=algorithm,color=colors[algorithm])
        ax.set(title=cid,xlabel='Iteration',ylabel='Number of exam periods');ax.grid(alpha=.2);ax.legend(fontsize=8)
    fig.tight_layout();fig.savefig(out/'convergence.png',dpi=180);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(10,3.4))
    for algorithm in ['GA','PSO','ACO']:
        ss=[r for r in summary if r['algorithm']==algorithm]
        axes[0].plot(['Small','Medium','Large'],[r['mean_gap_pct'] for r in ss],marker='o',label=algorithm,color=colors[algorithm])
        axes[1].plot(['Small','Medium','Large'],[r['mean_seconds'] for r in ss],marker='o',label=algorithm,color=colors[algorithm])
    axes[0].set(ylabel='Gap to reference (%)',title='Quality')
    axes[1].set(ylabel='Seconds per run',title='Search time')
    for ax in axes:ax.grid(alpha=.2);ax.legend(fontsize=8)
    fig.tight_layout();fig.savefig(out/'comparison.png',dpi=180);plt.close(fig)
    print('Saved',len(records),'runs to',out)
    return payload
if __name__=='__main__':main()
