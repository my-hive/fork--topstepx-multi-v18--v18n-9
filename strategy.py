"""Experiment 159: micro equity calendar-flow portfolio.
Mechanism: Friday MES basket/ETF opening flow and MNQ overnight-to-cash price discovery
are distinct timed institutional flows. Combining low-exposure micro legs may diversify
daily PnL and raise combine passes without altering each causal mechanism.
Falsifier: nonpositive primary statistic, any era loss, risk breach, or prefix failure.
"""
import numpy as np,pandas as pd
FAMILY='index-micro-friday-basket-plus-overnight-discovery'
PARAMS={'open_ct_sec':30600,'open_end_ct_sec':32400,'overnight_start_ct_sec':7200,'overnight_exit_ct_sec':37800,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64);c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
  if s=='MES':
   friday=(pd.to_datetime(d.session.astype(str).str[:10]).dt.weekday==4).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==30600];y=g[t[g]==32400]
    if len(x)and len(y)and friday[g[0]]:o[g[(t[g]>=32400)&(t[g]<46800)]]=int(np.sign(c[y[0]]-c[x[0]]))
  if s=='MNQ':
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==7200];y=g[t[g]==30600]
    if len(x)and len(y):o[g[(t[g]>=30600)&(t[g]<37800)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
