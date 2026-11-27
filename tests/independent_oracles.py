"""Independent, stdlib-only Python oracles against the JavaScript implementation.
Synthetic deterministic cases, plus fixed-seed independent stochastic comparisons.
No scientific/industrial certification. Run from any directory with Node installed.
"""
import json, math, random, statistics as st, subprocess
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
cases=[]
def add(model,args,expected,abs_tol=1e-10,rel_tol=1e-9):
    cases.append((model,args,expected,abs_tol,rel_tol))
def compare(actual,expected,a,r):
    if isinstance(expected,dict):
        for k,v in expected.items(): compare(actual[k],v,a,r)
    elif isinstance(expected,list):
        assert len(actual)==len(expected)
        for x,y in zip(actual,expected):compare(x,y,a,r)
    elif isinstance(expected,(int,float)) and not isinstance(expected,bool):
        assert isinstance(actual,(int,float)) and not isinstance(actual,bool) and math.isclose(actual,expected,abs_tol=a,rel_tol=r),(actual,expected)
    else: assert type(actual)==type(expected) and actual==expected,(actual,expected)
rng=random.Random(713)
# Independent formula in fractions, including all 4 Mini models.
for i in range(20):
    t=rng.randint(1,1440);c=rng.randint(1,300);a=rng.randint(0,100);q=rng.randint(0,100);d=rng.randint(1,10000)
    th=F(60*t,c);good=th*F(a*q,10000)
    add('M01',[t,c,a,q],{'theoretical':float(th),'good':float(good),'effective':float(th*F(a,100))})
    rates=[rng.randint(1,1000) for _ in range(4)];minimum=min(rates)
    add('M02',[rates,t],{'total':float(F(minimum*t,60)),'bottlenecks':[j+1 for j,x in enumerate(rates) if x==minimum]})
    x=[rng.randint(-100,100) for _ in range(6)];y=[rng.randint(-100,100) for _ in range(7)]
    add('M03',[' '.join(map(str,x)),' '.join(map(str,y))],{'A':{'mean':st.mean(x),'sd':st.stdev(x)},'B':{'mean':st.mean(y),'sd':st.stdev(y)},'delta':st.mean(y)-st.mean(x)})
    add('M04',[t,d,c,a,q],{'takt':60*t/d,'good':float(good),'gap':float(good-d),'meets':good>=d,'impossible':a*q==0})
    change=rng.randint(0,90)
    add('R01',[t,c,a,q,change],[{'good':float(good*F(100,100+p))} for p in [-change,0,change]])
    lam=rng.randint(0,99);mu=100;gap=mu-lam
    add('R02',[lam,mu],{'stable':True,'L':lam/gap,'Lq':lam**2/(mu*gap),'W':60/gap,'Wq':60*lam/(mu*gap)})
    # Centered two-pass Python statistics, unlike the JS online algorithm.
    measurements=[rng.randint(-1000,1000) for _ in range(9)]
    add('R06',[' '.join(map(str,measurements))],{'mean':st.mean(measurements),'sd':st.stdev(measurements),'se':st.stdev(measurements)/math.sqrt(len(measurements))})
    pairs=[[j,rng.randint(-100,100)] for j in range(1,10)]
    xx,yy=zip(*pairs);fit=st.linear_regression(xx,yy);res=[v-(fit.intercept+fit.slope*u) for u,v in pairs]
    add('R08',[pairs],{'slope':fit.slope,'intercept':fit.intercept,'r':st.correlation(xx,yy),'r2':st.correlation(xx,yy)**2,'rmse':math.sqrt(st.mean([z*z for z in res]))})
    rates=[rng.randint(1,50)/100 for _ in range(3)];t=rng.randint(1,100)
    probs=[math.exp(-rate*t) for rate in rates]
    add('R09',[rates,t],{'series':math.prod(probs),'parallel':1-math.prod(1-p for p in probs),'seriesMTTF':1/sum(rates)})
# Independent LP: project onto x, y is the minimum of upper affine bounds.
# For a nonnegative objective the maximum lies at an endpoint or a crossing.
def lp_oracle(v,a,b):
    v=list(map(lambda z:F(str(z)),v));a=[list(map(lambda z:F(str(z)),row)) for row in a];b=list(map(lambda z:F(str(z)),b))
    xmax=min(limit/row[0] for row,limit in zip(a,b) if row[0]>0)
    lines=[(limit/row[1],-row[0]/row[1]) for row,limit in zip(a,b) if row[1]>0]
    xs={F(0),xmax}
    if len(lines)==2 and lines[0][1]!=lines[1][1]:
        x=(lines[1][0]-lines[0][0])/(lines[0][1]-lines[1][1])
        if 0<=x<=xmax:xs.add(x)
    return max(v[0]*x+v[1]*min(k+m*x for k,m in lines) for x in xs)
for i in range(60):
    scale=[1e-6,.001,1,1000,1e5][i%5]
    a=[[round(scale*rng.randint(1,10),12) for _ in range(2)] for _ in range(2)]
    b=[rng.randint(0,1000)*.001,rng.randint(0,1000)*.001];v=[rng.randint(0,100),rng.randint(0,100)]
    add('R04',[v,a,b],{'best':{'objective':float(lp_oracle(v,a,b))}},abs_tol=1e-12)
add('R04',[[1e6,0],[[1e6,0],[0,1]],[.001,1]],{'best':{'x':1e-9,'objective':.001}},abs_tol=1e-18)
# Independent stochastic engine: Lindley recurrence, Python Mersenne Twister;
# compare independently simulated means to the known stationary mean.
def queue_sample(lam,mu,seed):
    r=random.Random(seed);wait=0.;work=r.expovariate(mu);out=[]
    for i in range(22000):
        wait=max(0.,wait+work-r.expovariate(lam));work=r.expovariate(mu)
        if i>=2000:out.append(wait*60)
    return st.mean(out)
for lam in (2,4,6):
    mu=10;theory=60*lam/(mu*(mu-lam));tolerance=.20*theory
    py=st.mean(queue_sample(lam,mu,713+j) for j in range(8))
    assert abs(py-theory)<tolerance,(py,theory)
    add('R03',[lam,mu,2000,20000,8,42],{'wait':{'mean':py}},abs_tol=2*tolerance,rel_tol=0)
    add('R03',[lam,mu,2000,20000,8,42],{'theoryWait':theory,'wait':{'mean':theory}},abs_tol=tolerance,rel_tol=0)
for lo,mode,hi,target in [(0,0,3,1),(80,100,140,100),(0,3,3,2)]:
    rr=random.Random(731);samples=[rr.triangular(lo,hi,mode) for _ in range(50000)]
    theoretical=(lo+mode+hi)/3
    assert abs(st.mean(samples)-theoretical)<.015*(hi-lo)
    add('R07',[lo,mode,hi,50000,42,target],{'mean':st.mean(samples)},abs_tol=.03*(hi-lo),rel_tol=0)
    add('R07',[lo,mode,hi,50000,42,target],{'mean':theoretical},abs_tol=.015*(hi-lo),rel_tol=0)
    # Independent analytic survival probability.
    prob=1-(target-lo)**2/((hi-lo)*(mode-lo)) if target<mode else (hi-target)**2/((hi-lo)*(hi-mode))
    add('R07',[lo,mode,hi,50000,42,target],{'probability':prob},abs_tol=.015,rel_tol=0)
# R05 validates schema and trimmed field semantics (not scientific truth).
add('R05',[{'title':' T ','question':' Q ','method':' M '}],{'schema':'rubedo.research.protocol.v1','title':'T','question':'Q','method':'M','hypothesis':''})
payload=json.dumps([{'model':m,'args':args} for m,args,*_ in cases])
out=json.loads(subprocess.check_output(['node',str(ROOT/'tests/oracle_bridge.js')],input=payload,text=True))
assert len(out)==len(cases)
counts={}
for i,((model,args,expected,a,r),actual) in enumerate(zip(cases,out)):
    try:compare(actual,expected,a,r)
    except AssertionError as e:raise AssertionError((i,model,args,e)) from e
    counts[model]=counts.get(model,0)+1
print('Independent Python oracle comparisons:',json.dumps(counts,sort_keys=True))
print(f'{len(cases)} independent oracle comparisons passed (synthetic; no industrial validation)')
