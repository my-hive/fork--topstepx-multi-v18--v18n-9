"""v18n-9 clean-room Friday opening-flow audit (NOT exact owner-board bytes).
Mechanism: Friday weekly ETF/basket hedges persist after cash opening auction.
Hypothesis: MNQ Friday completed 08:30-09:00 CT direction continues 09:00-14:00,
one contract, close-based $250 stop; signal close fills next minute open.
Falsifier: any negative era, fewer than 70% positive years, prefix mismatch, primary0.
ponytail: close stop not guaranteed $250 fill loss cap; diagnostic, not nomination.
"""
import numpy as np
import pandas as pd
FAMILY = "equity-friday-opening-flow-clean-room-audit"
PARAMS = {"observe_start":30600,"entry_sec":32400,"exit_sec":50400,"stop_dollars":250}

def signals(panel):
    out = {s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
    if "MNQ" not in panel:
        return out
    d=panel["MNQ"]
    c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
    sides={}
    for day,g in d.groupby('session',sort=False).indices.items():
        if pd.Timestamp(day).weekday()!=4:
            continue
        pre=g[(t[g]>=PARAMS['observe_start'])&(t[g]<PARAMS['entry_sec'])]
        if len(pre)>1:
            sides[pd.Timestamp(day)] = int(np.sign(c[pre[-1]]-c[pre[0]]))
    for s,d in panel.items():
        if s!='MNQ':
            continue
        c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
        pv=2.0
        for day,g in d.groupby('session',sort=False).indices.items():
            side=sides.get(pd.Timestamp(day),0)
            bars=g[(t[g]>=PARAMS['entry_sec'])&(t[g]<PARAMS['exit_sec'])]
            if not side or not len(bars):
                continue
            ref=c[bars[0]]
            for i in bars:
                if side*(c[i]-ref)<=-PARAMS['stop_dollars']/pv:
                    break
                out[s][i]=side
    return out

def entry_risk(panel):
    return {s:np.full(len(d),250.0 if s=='MNQ' else 0.0) for s,d in panel.items()}
