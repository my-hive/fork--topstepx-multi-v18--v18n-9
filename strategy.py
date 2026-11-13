"""Experiment 181: Nasdaq contract-roll gap continuation.
Mechanism: institutional roll transfer conveys durable index positioning; when current
session contract differs from prior completed session, overnight direction continues cash open.
No signal uses future data. Falsifier PnL/era <=0 or roll artifact detected.
"""
import numpy as np
FAMILY='index-nasdaq-contract-roll-gap-continuation'
PARAMS={'observe_ct_sec':7200,'entry_ct_sec':30600,'exit_ct_sec':43200,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='NQ':
   c,t,con=d.close.to_numpy(),d.ct_sec.to_numpy(),d.contract.astype(str).to_numpy();gs=list(d.groupby('session',sort=False).indices.values())
   for k in range(1,len(gs)):
    g=gs[k];prev=gs[k-1];x=g[t[g]==7200];y=g[t[g]==30600]
    if len(x)and len(y)and con[g[0]]!=con[prev[-1]]:o[g[(t[g]>=30600)&(t[g]<43200)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
