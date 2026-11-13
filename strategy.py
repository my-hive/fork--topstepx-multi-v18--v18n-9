"""v18n-9 analyst clean-room audit of v18n-3 exp25 description (source unpublished).
FAMILY: energy-crude-turn-of-month-window
Mechanism: refinery scheduling / producer hedging cluster at month boundary; prior
5-session CL trend continues during last 3 and first 3 business days of month.
Hypothesis: sign(last completed session close - close 5 sessions earlier), traded
08:00-12:00 CT on window days, 1 CL, close-based $250 stop from first in-window close.
Falsify: nonpositive stressed PnL, any negative era, <70% years, or prefix mismatch.
ponytail: business-day calendar uses weekdays only (no exchange holidays); window known in advance.
"""
import numpy as np
import pandas as pd

FAMILY = "energy-crude-turn-of-month-window"
PARAMS = {"lookback_sessions": 5, "edge_bdays": 3, "entry_sec": 28800, "exit_sec": 43200, "stop_dollars": 250}
CL_PV = 1000.0


def _window(day):
    d = day.normalize()
    left = np.busday_count(d.date(), (d + pd.offsets.BMonthEnd(0)).date())
    done = np.busday_count(d.replace(day=1).date(), d.date())
    return left < PARAMS["edge_bdays"] or done < PARAMS["edge_bdays"]


def signals(panel):
    ans = {s: np.zeros(len(d), dtype=np.int64) for s, d in panel.items()}
    if "CL" not in panel:
        return ans
    df, out = panel["CL"], ans["CL"]
    c, sec = df.close.to_numpy(), df.ct_sec.to_numpy()
    groups = list(df.groupby("session", sort=False).indices.values())
    ends = [c[g[-1]] for g in groups]
    lb = PARAMS["lookback_sessions"]
    for k in range(lb, len(groups)):
        g = groups[k]
        if not _window(pd.Timestamp(df.session.iloc[g[0]])):
            continue
        side = int(np.sign(ends[k - 1] - ends[k - 1 - lb])) if k - 1 - lb >= 0 else 0
        bars = g[(sec[g] >= PARAMS["entry_sec"]) & (sec[g] < PARAMS["exit_sec"])]
        if not side or len(bars) < 2:
            continue
        ref = c[bars[0]]
        for i in bars:
            if side * (c[i] - ref) <= -PARAMS["stop_dollars"] / CL_PV:
                break
            out[i] = side
    return ans


def entry_risk(panel):
    return {s: np.full(len(d), 290.0 if s == "CL" else 0.0) for s, d in panel.items()}
