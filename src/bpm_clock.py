"""Deterministic master clock shared by visual and audio pipelines."""
import math, random

def smooth(x):
    x=max(0.,min(1.,x)); return x*x*(3-2*x)

def bpm(t):
    if t<1.9: return 70.
    if t<2.4: return 70+280*((t-1.9)/.5)**2
    if t<4: return 350.
    if t<4.6: return 350-280*smooth((t-4)/.6)
    if t<10: return 70.
    if t<17: return 70+120*smooth((t-10)/7)
    if t<19: return 190+160*smooth((t-17)/2)
    if t<55: return 350.
    if t<56: return 350-280*smooth(t-55)
    return 70.

def beats():
    # Accumulating the instantaneous clock phase keeps counter, ECG and sound coupled.
    rng=random.Random(514); t=.3; result=[]
    while t<60:
        result.append(t)
        interval=60/bpm(t)
        if 39<=t<47: interval*=rng.uniform(.6,1.4)
        t+=interval
    # Return to a calm loop rhythm with an intentionally placed closing beat.
    result=[x for x in result if x<56]
    result += [56.2714286,57.1285714,57.9857143,58.8428571,59.7]
    return result
BEATS=beats()

def phase(t):
    import bisect
    i=bisect.bisect_right(BEATS,t)-1
    if i<0: return 1.
    return min(1.,(t-BEATS[i])/(BEATS[i+1]-BEATS[i])) if i+1<len(BEATS) else min(1.,(t-BEATS[i])/(60/70))
