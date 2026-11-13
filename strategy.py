"""Experiment 161: soybean delivery-month commercial roll reversal.
Mechanism: first-notice delivery and elevator position rolls create temporary futures
pressure at start of delivery months; commercial buying reverses prior session direction.
Known month calendar, US grain hours. Falsifier: PnL<=0 or any era<=0.
"""
import numpy as np,pandas as pd
FAMILY='grains-soy-delivery-month-commercial-roll-reversal'
PARAMS={'entry_ct_sec':30600,'exit_ct_sec':46800,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZS':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();gs=list(d.groupby('session',sort=False).indices.values());r=np.array([c[g[-1]]-c[g[0]] for g in gs]);dt=pd.to_datetime(d.session.iloc[[g[0] for g in gs]].astype(str).str[:10])
   for k in range(1,len(gs)):
    if dt.iloc[k].month in [1,3,5,7,8,9,11] and dt.iloc[k].day<=5:
     g=gs[k];o[g[(t[g]>=30600)&(t[g]<46800)]]=-int(np.sign(r[k-1]))
  a[s]=o
 return a
