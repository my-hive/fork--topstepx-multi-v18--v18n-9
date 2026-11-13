"""Friday diversified index basket-flow capacity audit.
Shared Friday MES/MNQ opening flow; one of each actual micro contract, no synthetic scaling.
Falsify if entry risk, primary, or economics fail.
"""
import numpy as np
import pandas as pd
FAMILY='equity-friday-opening-flow-portfolio-capacity-audit'
PARAMS={'entry':32400,'exit':50400,'mnq_stop':100.,'mes_stop':10.}
def entry_risk(panel):
 return {s:np.full(len(d),205. if s=='MNQ' else 55. if s=='MES' else 301.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s not in ('MNQ','MES'):continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy();stop=PARAMS['mnq_stop'] if s=='MNQ' else PARAMS['mes_stop']
  for sess,ix in d.groupby('session',sort=False).indices.items():
   if pd.Timestamp(sess).day_of_week!=4:continue
   a=np.where(t[ix]==30540)[0];b=np.where(t[ix]==PARAMS['entry']-60)[0]
   if not len(a) or not len(b):continue
   side=int(np.sign(c[ix[b[0]]]-c[ix[a[0]]]));ref=c[ix[b[0]]]
   if side:
    for r in ix[b[0]+1:]:
     if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-stop:break
     out[s][r]=side
 return out
