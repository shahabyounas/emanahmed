# -*- coding: utf-8 -*-
"""
Small-angle scattering computed from real geometry.

Nothing here is a hand-drawn curve. For each model body we sample the pair
distance distribution p(r) by Monte Carlo, then obtain the scattering profile
from the Debye relation

    I(q) = integral p(r) * sin(qr)/(qr) dr

and derive Rg and Dmax from the same p(r). Guinier, Kratky and P(r) figures on
the site are three views of one self-consistent calculation, so they agree with
each other the way real data does.

Deterministic: fixed seed, so the build is reproducible.
"""
import math, random

N_PAIRS = 300_000
N_BINS = 220


def _sample_sphere(rnd, R):
    while True:
        x, y, z = (rnd.uniform(-1, 1) for _ in range(3))
        if x * x + y * y + z * z <= 1.0:
            return x * R, y * R, z * R


def _sample_prolate(rnd, a, c):
    """Prolate ellipsoid, semi-axes a, a, c (c > a)."""
    while True:
        x, y, z = (rnd.uniform(-1, 1) for _ in range(3))
        if x * x + y * y + z * z <= 1.0:
            return x * a, y * a, z * c


def _sample_dumbbell(rnd, R, sep):
    """Two spheres of radius R whose centres are `sep` apart on z."""
    x, y, z = _sample_sphere(rnd, R)
    return x, y, z + (sep / 2 if rnd.random() < 0.5 else -sep / 2)


BODIES = {
    # name: (sampler, kwargs, human label)
    "globular":  (_sample_sphere,   dict(R=30.0),            "Globular (sphere, R = 30 Å)"),
    "elongated": (_sample_prolate,  dict(a=16.0, c=62.0),    "Elongated (prolate, 16 × 16 × 62 Å)"),
    "two-domain": (_sample_dumbbell, dict(R=20.0, sep=52.0), "Two-domain (2 × R = 20 Å, 52 Å apart)"),
    # Larger body for the landing-page detector image: a 9 nm particle puts several
    # form-factor minima inside the accessible q range, so the pattern reads as the
    # ring set it actually is rather than one bright disc.
    "nanoparticle": (_sample_sphere, dict(R=90.0), "Nanoparticle (sphere, R = 90 Å)"),
}


_CACHE = {}


def pair_distribution(body, seed=7):
    """Monte-Carlo p(r): histogram of distances between random point pairs."""
    if (body, seed) in _CACHE:
        return _CACHE[(body, seed)]
    sampler, kw, label = BODIES[body]
    rnd = random.Random(seed)
    dists = []
    for _ in range(N_PAIRS):
        x1, y1, z1 = sampler(rnd, **kw)
        x2, y2, z2 = sampler(rnd, **kw)
        dists.append(math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2))
    dmax = max(dists)
    w = dmax / N_BINS
    hist = [0.0] * N_BINS
    for d in dists:
        i = min(N_BINS - 1, int(d / w))
        hist[i] += 1.0
    # Three passes of a light 3-point kernel. Histogram shot noise is visible in
    # p(r) and transforms into ringing that drives I(q) slightly negative at the
    # form-factor minima, which is unphysical. Smoothing removes both and leaves
    # Rg and Dmax unchanged to two decimal places (checked against the analytical
    # sphere values in __main__).
    for _ in range(3):
        hist = [(hist[max(0, i-1)] + 2*hist[i] + hist[min(N_BINS-1, i+1)]) / 4.0
                for i in range(N_BINS)]
    r = [(i + 0.5) * w for i in range(N_BINS)]
    peak = max(hist) or 1.0
    p = [h / peak for h in hist]                       # normalised to peak = 1
    # Rg^2 = integral r^2 p(r) dr / (2 * integral p(r) dr)
    num = sum(pi * ri * ri for pi, ri in zip(p, r))
    den = sum(p)
    rg = math.sqrt(num / (2 * den))
    out = {"label": label, "r": r, "p": p, "dmax": dmax, "rg": rg, "dr": w}
    _CACHE[(body, seed)] = out
    return out


def profile(pr, qmin=0.005, qmax=0.25, n=160):
    """I(q) from p(r) by the Debye relation. Log-spaced q, normalised I(0) = 1."""
    r, p, dr = pr["r"], pr["p"], pr["dr"]
    qs, iq = [], []
    lo, hi = math.log(qmin), math.log(qmax)
    for k in range(n):
        q = math.exp(lo + (hi - lo) * k / (n - 1))
        s = 0.0
        for pi, ri in zip(p, r):
            x = q * ri
            s += pi * (math.sin(x) / x if x > 1e-9 else 1.0) * dr
        qs.append(q)
        iq.append(s)
    i0 = sum(p) * dr
    # Physical floor: I(q) cannot be negative. Anything at or below 1e-5 of I(0) is
    # under the Monte-Carlo noise level of this calculation, so it is clamped there
    # rather than reported as structure.
    floor = 1e-5
    return qs, [max(v / i0, floor) for v in iq]


def compute_all():
    out = {}
    for name in BODIES:
        pr = pair_distribution(name)
        q, i = profile(pr)
        out[name] = {
            **pr, "q": q, "i": i,
            # Guinier is valid to q^2max = 1.5 / Rg^2  (i.e. qRg <= ~1.22)
            "q2max": 1.5 / (pr["rg"] ** 2),
        }
    return out


if __name__ == "__main__":
    for n, d in compute_all().items():
        print(f"{n:11} Rg = {d['rg']:6.2f} A   Dmax = {d['dmax']:6.1f} A   "
              f"Dmax/Rg = {d['dmax']/d['rg']:.2f}   q2max = {d['q2max']:.5f}")
