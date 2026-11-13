"""Experiment 155: micro Russell Friday opening institutional flow.
Mechanism: weekly ETF creation/redemption and index basket rebalance concentrates Friday
cash-open flow in small caps; first half-hour direction continues through morning.
Falsifier: stressed PnL <=0, any era <=0, or primary zero.
"""
import numpy as np,pandas as pd
FAMILY='equity-russell-friday-opening-institutional-flow'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':46800,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='M2K':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();friday=(pd.to_datetime(d.session.astype(str).str[:10]).dt.weekday==4).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==30600];y=g[t[g]==32400]
    if len(x)and len(y)and friday[g[0]]:o[g[(t[g]>=32400)&(t[g]<46800)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
