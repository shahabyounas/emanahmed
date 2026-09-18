# -*- coding: utf-8 -*-
"""
Chart primitives -> inline SVG.

Charts are rendered at build time into the HTML, not drawn by JavaScript. That
keeps them readable by crawlers and answer engines, visible with JS disabled,
and free of layout shift. A small script adds the hover layer on top.

Every figure ships three things: the plot, a `<details>` data table with the
underlying numbers, and a provenance line saying where the numbers came from.

Colour comes from CSS custom properties (--v1..--v4, status, grid, ink) so the
dark theme swaps without re-rendering. The categorical order is fixed and never
cycled; past four series, fold or facet.
"""
import math, html

PROV = {
    "measured":  ("Measured", "Values measured in the published work."),
    "reported":  ("Reported", "Values exactly as published; see the source note."),
    "computed":  ("Computed", "Computed from theory for this page, not measured data."),
    "schematic": ("Schematic", "A diagram of the method, not a data plot."),
}


def esc(s):
    return html.escape(str(s), quote=True)


def fmt(v, dp=None):
    if isinstance(v, str):
        return v
    if dp is not None:
        return f"{v:,.{dp}f}"
    if isinstance(v, int) or float(v).is_integer():
        return f"{int(v):,}"
    return f"{v:,.2f}"


# --- scales ---------------------------------------------------------------

class Lin:
    def __init__(s, d0, d1, r0, r1):
        s.d0, s.d1, s.r0, s.r1 = d0, d1, r0, r1
    def __call__(s, v):
        if s.d1 == s.d0: return s.r0
        return s.r0 + (v - s.d0) / (s.d1 - s.d0) * (s.r1 - s.r0)

class Log:
    def __init__(s, d0, d1, r0, r1):
        s.a, s.b, s.r0, s.r1 = math.log10(d0), math.log10(d1), r0, r1
    def __call__(s, v):
        return s.r0 + (math.log10(v) - s.a) / (s.b - s.a) * (s.r1 - s.r0)


def nice_ticks(lo, hi, n=5):
    if hi <= lo: return [lo]
    raw = (hi - lo) / n
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        if raw <= m * mag:
            step = m * mag
            break
    start = math.ceil(lo / step) * step
    out, v = [], start
    while v <= hi + step * 1e-9:
        out.append(round(v, 10)); v += step
    return out


def log_ticks(lo, hi):
    out = []
    e = math.floor(math.log10(lo))
    while 10 ** e <= hi * 1.0001:
        if 10 ** e >= lo * 0.9999:
            out.append(10 ** e)
        e += 1
    return out


# --- figure shell ---------------------------------------------------------

def figure(fid, title, sub, svg, table, prov, source=None, legend=None, note=None):
    kind, default = PROV[prov]
    legend_html = f'<div class="fig__legend">{legend}</div>' if legend else ""
    note_html = f'<p class="fig__note">{note}</p>' if note else ""
    return f'''<figure class="fig" id="{fid}">
  <figcaption class="fig__head">
    <h3 class="fig__title">{title}</h3>
    <p class="fig__sub">{sub}</p>
  </figcaption>
  <div class="fig__plot">{svg}</div>
  {legend_html}
  {note_html}
  <details class="fig__data">
    <summary>Show the numbers</summary>
    {table}
  </details>
  <p class="fig__prov"><span class="fig__badge fig__badge--{prov}">{kind}</span>
  {source or default}</p>
</figure>'''


def table(headers, rows, caption=None):
    th = "".join(f"<th scope=\"col\">{h}</th>" for h in headers)
    tr = "".join("<tr>" + "".join(
        (f'<th scope="row">{c}</th>' if i == 0 else f"<td>{c}</td>")
        for i, c in enumerate(r)) + "</tr>" for r in rows)
    cap = f"<caption>{caption}</caption>" if caption else ""
    return f'<div class="fig__tablewrap"><table class="fig__table">{cap}<thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def legend_items(items):
    """items: [(css_var_or_class, label)]"""
    return '<ul class="lg">' + "".join(
        f'<li class="lg__i"><span class="lg__k" style="background:var({v})"></span>{l}</li>'
        for v, l in items) + "</ul>"


def svg_open(w, h, title, desc=""):
    d = f"<desc>{esc(desc)}</desc>" if desc else ""
    return (f'<svg class="viz" viewBox="0 0 {w} {h}" role="img" preserveAspectRatio="xMidYMid meet" '
            f'aria-label="{esc(title)}">{d}')


def grid_line(x1, y1, x2, y2):
    return f'<line class="viz__grid" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>'


def axis_line(x1, y1, x2, y2):
    return f'<line class="viz__axis" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>'


def txt(x, y, s, cls="viz__lbl", anchor="middle", dy=0):
    return (f'<text class="{cls}" x="{x:.1f}" y="{y + dy:.1f}" '
            f'text-anchor="{anchor}">{s}</text>')


# =========================================================================
# Line / curve chart  (Guinier, Kratky, P(r), parity)
# =========================================================================

def linechart(series, *, w=680, h=380, xlabel="", ylabel="", xlog=False, ylog=False,
              xdom=None, ydom=None, xfmt=None, yfmt=None, bands=None, marks=None,
              title="", desc="", pad=None, xticks_n=5, yticks_n=5):
    """series: [{'name','pts':[(x,y)],'var':'--v1','label_at':idx|None,'dash':bool}]"""
    m = pad or dict(l=64, r=22, t=18, b=48)
    x0, x1 = m["l"], w - m["r"]
    y0, y1 = h - m["b"], m["t"]

    xs = [p[0] for s in series for p in s["pts"]]
    ys = [p[1] for s in series for p in s["pts"]]
    xd = xdom or (min(xs), max(xs))
    yd = ydom or (min(ys), max(ys))
    if not ylog and not ydom:
        span = yd[1] - yd[0] or 1
        yd = (yd[0] - span * 0.06, yd[1] + span * 0.10)

    X = (Log if xlog else Lin)(xd[0], xd[1], x0, x1)
    Y = (Log if ylog else Lin)(yd[0], yd[1], y0, y1)

    xt = log_ticks(*xd) if xlog else nice_ticks(*xd, xticks_n)
    yt = log_ticks(*yd) if ylog else nice_ticks(*yd, yticks_n)
    xfmt = xfmt or (lambda v: f"{v:g}")
    yfmt = yfmt or (lambda v: f"{v:g}")

    o = [svg_open(w, h, title, desc)]

    # shaded bands sit below the grid
    for b in (bands or []):
        bx0, bx1 = X(b["x0"]), X(b["x1"])
        o.append(f'<rect class="viz__band" x="{min(bx0,bx1):.1f}" y="{y1:.1f}" '
                 f'width="{abs(bx1-bx0):.1f}" height="{y0-y1:.1f}"/>')
        if b.get("label"):
            o.append(txt(min(bx0, bx1) + 6, y1 + 14, b["label"], "viz__bandlbl", "start"))

    for t in yt:
        yy = Y(t)
        if y1 - 1 <= yy <= y0 + 1:
            o.append(grid_line(x0, yy, x1, yy))
            o.append(txt(x0 - 10, yy + 4, yfmt(t), "viz__tick", "end"))
    for t in xt:
        xx = X(t)
        if x0 - 1 <= xx <= x1 + 1:
            o.append(txt(xx, y0 + 20, xfmt(t), "viz__tick"))
    o.append(axis_line(x0, y0, x1, y0))
    o.append(axis_line(x0, y0, x0, y1))

    # extra reference marks (vertical rules, points of interest)
    for mk in (marks or []):
        if mk["type"] == "vline":
            xx = X(mk["x"])
            o.append(f'<line class="viz__rule" x1="{xx:.1f}" y1="{y1:.1f}" x2="{xx:.1f}" y2="{y0:.1f}"/>')
            if mk.get("label"):
                near_right = xx > x1 - 90
                o.append(txt(xx + (-6 if near_right else 6),
                             y1 + 4 + mk.get("label_dy", 10), mk["label"],
                             "viz__rulelbl", "end" if near_right else "start"))
        elif mk["type"] == "hline":
            yy = Y(mk["y"])
            o.append(f'<line class="viz__rule" x1="{x0:.1f}" y1="{yy:.1f}" x2="{x1:.1f}" y2="{yy:.1f}"/>')
            if mk.get("label"):
                o.append(txt(x1 - 6, yy - 7, mk["label"], "viz__rulelbl", "end"))
        elif mk["type"] == "diag":
            o.append(f'<line class="viz__rule" x1="{X(xd[0]):.1f}" y1="{Y(xd[0]):.1f}" '
                     f'x2="{X(xd[1]):.1f}" y2="{Y(xd[1]):.1f}"/>')

    for s in series:
        pts = [(X(px), Y(py)) for px, py in s["pts"]]
        d = "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in pts)
        dash = ' stroke-dasharray="5 4"' if s.get("dash") else ""
        o.append(f'<path class="viz__line" d="{d}" style="stroke:var({s["var"]})"{dash}/>')
        li = s.get("label_at")
        if li is not None:
            px, py = pts[li]
            anch = s.get("anchor") or ("end" if li >= len(pts) - 2 else "start")
            off = -8 if anch == "end" else 8
            dy = s.get("label_dy", -9)
            o.append(f'<text class="viz__slbl" x="{px+off:.1f}" y="{py+dy:.1f}" '
                     f'text-anchor="{anch}" style="fill:var({s["var"]})">{s["name"]}</text>')

    o.append(txt((x0 + x1) / 2, h - 8, xlabel, "viz__axlbl"))
    o.append(f'<text class="viz__axlbl" transform="translate(15 {(y0+y1)/2}) rotate(-90)" '
             f'text-anchor="middle">{ylabel}</text>')
    o.append("</svg>")
    return "".join(o)


# =========================================================================
# Dot plot on a log axis  (magnitudes spanning orders -- never log bars)
# =========================================================================

def dotplot_log(rows, *, w=680, xlabel="", title="", desc="", highlight=None):
    """rows: [(label, value, sublabel)]"""
    rowh, top, bot = 40, 16, 54
    h = top + rowh * len(rows) + bot
    m = dict(l=214, r=60)
    x0, x1 = m["l"], w - m["r"]
    lo = 10 ** math.floor(math.log10(min(r[1] for r in rows)))
    hi = 10 ** math.ceil(math.log10(max(r[1] for r in rows)))
    X = Log(lo, hi, x0, x1)
    o = [svg_open(w, h, title, desc)]
    for t in log_ticks(lo, hi):
        xx = X(t)
        o.append(grid_line(xx, top - 4, xx, top + rowh * len(rows)))
        e = int(round(math.log10(t)))
        lbl = "1" if e == 0 else ("10" if e == 1 else f"10{_sup(e)}")
        o.append(txt(xx, top + rowh * len(rows) + 22, lbl, "viz__tick"))
    for i, (lab, val, sub) in enumerate(rows):
        yy = top + rowh * i + rowh / 2
        var = "--v1" if (highlight is None or i == highlight) else "--v-dim"
        o.append(f'<line class="viz__stem" x1="{x0:.1f}" y1="{yy:.1f}" x2="{X(val):.1f}" y2="{yy:.1f}"/>')
        o.append(f'<circle class="viz__dot" cx="{X(val):.1f}" cy="{yy:.1f}" r="6" '
                 f'style="fill:var({var})"><title>{esc(lab)}: {fmt(val)}</title></circle>')
        o.append(txt(x0 - 14, yy - 2, esc(lab), "viz__rowlbl", "end"))
        o.append(txt(x0 - 14, yy + 12, esc(sub), "viz__rowsub", "end"))
        o.append(txt(X(val) + 12, yy + 4, fmt(val), "viz__val", "start"))
    o.append(txt((x0 + x1) / 2, h - 8, xlabel, "viz__axlbl"))
    o.append("</svg>")
    return "".join(o)


_SUPS = {"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
         "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"}
def _sup(n):
    return "".join(_SUPS[c] for c in str(n))


# =========================================================================
# Horizontal bars  (few values, common linear scale, zero baseline)
# =========================================================================

def barh(rows, *, w=680, xlabel="", xdom=None, title="", desc="", ref=None, xfmt=None, dots=False):
    """rows: [(label, value, var, sublabel)]

    dots=True renders a stem-and-dot instead of a filled bar. Use it whenever the
    axis does not start at a true zero: a bar's length would then imply a ratio
    the data does not support, while a dot only claims a position."""
    rowh, top, bot = 46, 14, 52
    h = top + rowh * len(rows) + bot
    x0, x1 = 232, w - 74
    lo, hi = xdom or (0, max(r[1] for r in rows) * 1.12)
    X = Lin(lo, hi, x0, x1)
    xfmt = xfmt or (lambda v: f"{v:g}")
    o = [svg_open(w, h, title, desc)]
    for t in nice_ticks(lo, hi, 5):
        xx = X(t)
        o.append(grid_line(xx, top - 2, xx, top + rowh * len(rows)))
        o.append(txt(xx, top + rowh * len(rows) + 22, xfmt(t), "viz__tick"))
    if ref:
        xx = X(ref["x"])
        o.append(f'<line class="viz__rule" x1="{xx:.1f}" y1="{top-2:.1f}" x2="{xx:.1f}" '
                 f'y2="{top + rowh*len(rows):.1f}"/>')
        o.append(txt(xx, top - 4, ref["label"], "viz__rulelbl"))
    bh = 16
    for i, (lab, val, var, sub) in enumerate(rows):
        yy = top + rowh * i + rowh / 2 - bh / 2
        if dots:
            o.append(f'<line class="viz__stem" x1="{X(lo):.1f}" y1="{yy+bh/2:.1f}" '
                     f'x2="{X(val):.1f}" y2="{yy+bh/2:.1f}"/>')
            o.append(f'<circle class="viz__dot" cx="{X(val):.1f}" cy="{yy+bh/2:.1f}" r="6.5" '
                     f'style="fill:var({var})"><title>{esc(lab)}: {xfmt(val)}</title></circle>')
        else:
            o.append(f'<rect class="viz__bar" x="{X(lo):.1f}" y="{yy:.1f}" '
                     f'width="{max(0, X(val)-X(lo)):.1f}" height="{bh}" rx="4" '
                     f'style="fill:var({var})"><title>{esc(lab)}: {xfmt(val)}</title></rect>')
        o.append(txt(x0 - 14, yy + 7, esc(lab), "viz__rowlbl", "end"))
        if sub:
            o.append(txt(x0 - 14, yy + 21, esc(sub), "viz__rowsub", "end"))
        o.append(txt(X(val) + 10, yy + 12, xfmt(val), "viz__val", "start"))
    o.append(txt((x0 + x1) / 2, h - 8, xlabel, "viz__axlbl"))
    o.append("</svg>")
    return "".join(o)


# =========================================================================
# Dot matrix  (which method is used where -- presence, not magnitude)
# =========================================================================

def dotmatrix(cols, rows, cells, *, w=680, title="", desc="", collab="", rowlab=""):
    """cells: {(row_i, col_i): 1} marks a filled cell."""
    left, top = 210, 96
    cw, rh = (w - left - 24) / len(cols), 40
    h = top + rh * len(rows) + 30
    o = [svg_open(w, h, title, desc)]
    for j, c in enumerate(cols):
        cx = left + cw * (j + 0.5)
        o.append(f'<text class="viz__colhdr" transform="translate({cx:.1f} {top-14}) rotate(-38)" '
                 f'text-anchor="start">{esc(c)}</text>')
    for i, r in enumerate(rows):
        cy = top + rh * i + rh / 2
        if i % 2 == 0:
            o.append(f'<rect class="viz__zebra" x="{left-200:.1f}" y="{top+rh*i:.1f}" '
                     f'width="{w-left+176-24:.1f}" height="{rh}"/>')
        o.append(txt(left - 16, cy + 4, esc(r), "viz__rowlbl", "end"))
        for j in range(len(cols)):
            cx = left + cw * (j + 0.5)
            if cells.get((i, j)):
                o.append(f'<circle class="viz__cell" cx="{cx:.1f}" cy="{cy:.1f}" r="7" '
                         f'style="fill:var(--v1)"><title>{esc(rows[i])} · {esc(cols[j])}</title></circle>')
            else:
                o.append(f'<circle class="viz__cellempty" cx="{cx:.1f}" cy="{cy:.1f}" r="2.5"/>')
    o.append("</svg>")
    return "".join(o)


# =========================================================================
# Tolerance strip -- a published accept/flag decision rule, no invented points
# =========================================================================

def tolerance_strip(*, w=680, h=176, tol=20, title="", desc=""):
    x0, x1, yc = 60, w - 60, 88
    X = Lin(-45, 45, x0, x1)
    o = [svg_open(w, h, title, desc)]
    o.append(f'<rect class="viz__zoneflag" x="{X(-45):.1f}" y="{yc-30}" '
             f'width="{X(-tol)-X(-45):.1f}" height="60" rx="3"/>')
    o.append(f'<rect class="viz__zoneflag" x="{X(tol):.1f}" y="{yc-30}" '
             f'width="{X(45)-X(tol):.1f}" height="60" rx="3"/>')
    o.append(f'<rect class="viz__zoneok" x="{X(-tol):.1f}" y="{yc-30}" '
             f'width="{X(tol)-X(-tol):.1f}" height="60" rx="3"/>')
    for t in (-40, -30, -20, -10, 0, 10, 20, 30, 40):
        xx = X(t)
        o.append(f'<line class="viz__axis" x1="{xx:.1f}" y1="{yc+30:.1f}" x2="{xx:.1f}" y2="{yc+36:.1f}"/>')
        o.append(txt(xx, yc + 52, f"{t:+d}%" if t else "0", "viz__tick"))
    # stop the rule above the zone label rather than striking through it
    o.append(f'<line class="viz__rule" x1="{X(0):.1f}" y1="{yc-30}" x2="{X(0):.1f}" y2="{yc-8}"/>')
    o.append(f'<line class="viz__rule" x1="{X(0):.1f}" y1="{yc+12}" x2="{X(0):.1f}" y2="{yc+30}"/>')
    o.append(txt(X(0), yc - 40, "BIFT Dₘₐₓ", "viz__rulelbl"))
    o.append(txt((X(-tol) + X(tol)) / 2, yc + 6, "✓  accepted, shown green", "viz__zonelbl"))
    o.append(txt((X(-45) + X(-tol)) / 2, yc + 6, "⚠ flagged", "viz__zonelbl"))
    o.append(txt((X(tol) + X(45)) / 2, yc + 6, "⚠ flagged", "viz__zonelbl"))
    o.append(txt((x0 + x1) / 2, h - 8,
                 "Deviation of the model's predicted Dₘₐₓ from the BIFT value", "viz__axlbl"))
    o.append("</svg>")
    return "".join(o)


# =========================================================================
# MLP architecture  (the published 4 x 32 regressor)
# =========================================================================

def mlp_diagram(*, w=680, h=290, hidden=4, units=32, shown=5, title="", desc=""):
    cols = 2 + hidden
    gap = (w - 130) / (cols - 1)
    o = [svg_open(w, h, title, desc)]
    layers = []
    for c in range(cols):
        x = 65 + gap * c
        n = shown if 0 < c < cols - 1 else (5 if c == 0 else 1)
        ys = [h / 2 + (i - (n - 1) / 2) * 26 for i in range(n)]
        layers.append((x, ys))
    for c in range(cols - 1):
        x1_, ys1 = layers[c]; x2_, ys2 = layers[c + 1]
        for a in ys1:
            for b in ys2:
                o.append(f'<line class="viz__edge" x1="{x1_:.1f}" y1="{a:.1f}" x2="{x2_:.1f}" y2="{b:.1f}"/>')
    for c, (x, ys) in enumerate(layers):
        var = "--v2" if c == 0 else ("--v3" if c == cols - 1 else "--v1")
        for y in ys:
            o.append(f'<circle class="viz__node" cx="{x:.1f}" cy="{y:.1f}" r="7" style="fill:var({var})"/>')
        if 0 < c < cols - 1:
            o.append(txt(x, ys[0] - 20, "⋮", "viz__nodelbl"))
            o.append(txt(x, ys[-1] + 30, "⋮", "viz__nodelbl"))
            o.append(txt(x, h - 30, f"{units}", "viz__nodeval"))
            o.append(txt(x, h - 16, "units", "viz__nodelbl"))
    o.append(txt(layers[0][0], h - 30, "features", "viz__nodelbl"))
    o.append(txt(layers[0][0], 26, "scattering", "viz__nodelbl"))
    o.append(txt(layers[0][0], 40, "features", "viz__nodelbl"))
    o.append(txt(layers[-1][0], 26, "predicted", "viz__nodelbl"))
    o.append(txt(layers[-1][0], 40, "Dₘₐₓ", "viz__nodelbl"))
    o.append(txt(layers[-1][0], h - 30, "1", "viz__nodeval"))
    o.append(txt(layers[-1][0], h - 16, "output", "viz__nodelbl"))
    o.append("</svg>")
    return "".join(o)


# =========================================================================
# Detector image -- rings computed from the same I(q) as the curves
# =========================================================================

def detector(q, iq, *, size=420, beamstop=34, rings=150, decades=4.0, gamma=1.7,
             title="", desc=""):
    """Isotropic solution scattering: intensity at radius r maps to I(q).
    The dark rings ARE the form-factor minima of the modelled particle."""
    c = size / 2
    rmax = c - 10
    # Displayed on a windowed log scale, as a real detector image is: four decades
    # below the strongest ring. Without the window the whole plate saturates.
    lmax = math.log10(max(iq))
    lmin = lmax - decades
    o = [svg_open(size, size, title, desc)]
    o.append(f'<rect class="det__bg" x="0" y="0" width="{size}" height="{size}" rx="6"/>')
    step = (rmax - beamstop) / rings
    for k in range(rings):
        r = beamstop + step * k
        frac = k / (rings - 1)
        qi = min(len(q) - 1, int(frac * (len(q) - 1)))
        v = (math.log10(iq[qi]) - lmin) / (lmax - lmin)
        v = max(0.0, min(1.0, v))
        o.append(f'<circle class="det__ring" cx="{c}" cy="{c}" r="{r + step/2:.2f}" '
                 f'stroke-width="{step + 0.8:.2f}" opacity="{v**gamma:.3f}"/>')
    o.append(f'<circle class="det__stop" cx="{c}" cy="{c}" r="{beamstop}"/>')
    o.append(f'<line class="det__arm" x1="{c}" y1="0" x2="{c}" y2="{c-beamstop}"/>')
    o.append(f'<circle class="det__sweep" cx="{c}" cy="{c}" r="{rmax}"/>')
    o.append(f'<text class="det__lbl" x="10" y="{size-10}">q →</text>')
    o.append("</svg>")
    return "".join(o)


# =========================================================================
# Workflow flow diagram
# =========================================================================

def flow(steps, *, w=680, title="", desc=""):
    """steps: [(label, sublabel)] rendered as a left-to-right chain."""
    n = len(steps)
    bw, gap, h = (w - 24 - (n - 1) * 26) / n, 26, 140
    o = [svg_open(w, h, title, desc)]
    for k, (lab, sub) in enumerate(steps):
        x = 12 + k * (bw + gap)
        o.append(f'<rect class="flow__box" x="{x:.1f}" y="30" width="{bw:.1f}" height="74" rx="4"/>')
        o.append(f'<text class="flow__n" x="{x+10:.1f}" y="50">{k+1}</text>')
        for li, line in enumerate(_wrap(lab, int(bw / 6.4))):
            o.append(txt(x + bw / 2, 68 + li * 13, esc(line), "flow__lbl"))
        o.append(txt(x + bw / 2, 96, esc(sub), "flow__sub"))
        if k < n - 1:
            ax = x + bw + 6
            o.append(f'<path class="flow__arrow" d="M{ax:.1f} 67 L{ax+13:.1f} 67 M{ax+9:.1f} 63 '
                     f'L{ax+13:.1f} 67 L{ax+9:.1f} 71"/>')
    o.append("</svg>")
    return "".join(o)


def _wrap(s, n):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 <= n:
            cur = (cur + " " + wd).strip()
        else:
            lines.append(cur); cur = wd
    if cur: lines.append(cur)
    return lines[:2]


# =========================================================================
# Hero: the design-build-test-learn loop, drawn with the three instruments
# =========================================================================

def _hp_label(o, x, y, k, c):
    o.append(f'<text class="hp__k" x="{x}" y="{y}">{k}</text>')
    o.append(f'<text class="hp__c" x="{x}" y="{y+18}">{c}</text>')


def _hp_plate(o, x, y, cols, rows, pitch, r, hits, d0=0.0):
    for rr in range(rows):
        for cc in range(cols):
            cx, cy = x + r + cc * pitch, y + r + rr * pitch
            o.append(f'<circle class="hp__well" cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}"/>')
            v = 0.12 + (cc / (cols - 1)) ** 1.5 * 0.74
            hit = (rr, cc) in hits
            if hit: v = 1.0
            o.append(f'<circle class="hp__read{" hp__read--hit" if hit else ""}" '
                     f'cx="{cx:.1f}" cy="{cy:.1f}" r="{r-1.3:.1f}" '
                     f'style="--o:{v:.2f};--d:{d0 + cc*0.045 + rr*0.012:.2f}s"/>')


def _hp_rings(o, cx, cy, r0, stop, n, q, iq, d0, decades=5.0):
    lmax = math.log10(max(iq)); lmin = lmax - decades
    step = (r0 - stop) / n
    o.append(f'<circle class="hp__detbg" cx="{cx}" cy="{cy}" r="{r0+6}"/>')
    for k in range(n):
        rr = stop + step * k
        qi = min(len(q) - 1, int(k / (n - 1) * (len(q) - 1)))
        v = max(0.0, min(1.0, (math.log10(iq[qi]) - lmin) / (lmax - lmin)))
        o.append(f'<circle class="hp__ring" cx="{cx}" cy="{cy}" r="{rr+step/2:.2f}" '
                 f'stroke-width="{step+0.9:.2f}" style="--o:{v:.3f};--d:{d0 + k*0.0035:.2f}s"/>')
    o.append(f'<circle class="hp__stop" cx="{cx}" cy="{cy}" r="{stop}"/>')
    o.append(f'<circle class="hp__sweep" cx="{cx}" cy="{cy}" r="{r0}" '
             f'style="transform-origin:{cx}px {cy}px"/>')


def _hp_model(o, x, y, mw, mh, curve_pts, ny, d0):
    xs = [p[0] for p in curve_pts]; ys = [p[1] for p in curve_pts]
    X = Lin(min(xs), max(xs), x, x + mw)
    Y = Lin(min(ys), max(ys) * 1.06, y + mh, y)
    d = "M" + " L".join(f"{X(a):.1f} {Y(b):.1f}" for a, b in curve_pts)
    o.append(f'<line class="hp__ax" x1="{x}" y1="{y+mh}" x2="{x+mw}" y2="{y+mh}"/>')
    o.append(f'<path class="hp__curve" pathLength="1" style="--d:{d0}s" d="{d}"/>')
    nx0, ngap = x + 8, (mw - 16) / 3
    cols = [[ny - 18, ny, ny + 18], [ny - 27, ny - 9, ny + 9, ny + 27], [ny]]
    for ci in range(len(cols) - 1):
        for a in cols[ci]:
            for b in cols[ci + 1]:
                o.append(f'<line class="hp__edge" x1="{nx0+ngap*ci:.1f}" y1="{a}" '
                         f'x2="{nx0+ngap*(ci+1):.1f}" y2="{b}"/>')
    for ci, col in enumerate(cols):
        for yy in col:
            o.append(f'<circle class="hp__node" cx="{nx0+ngap*ci:.1f}" cy="{yy}" r="4.5" '
                     f'style="--d:{d0 + 0.3 + ci*0.12:.2f}s"/>')
    o.append(txt(nx0 + ngap * 2, ny + 24, "predicted structure", "hp__c"))


def _hp_arrow(o, x, y, delay, vertical=False):
    if vertical:
        d = f"M{x} {y} L{x} {y+30} M{x-6} {y+22} L{x} {y+30} L{x+6} {y+22}"
    else:
        d = f"M{x} {y} L{x+36} {y} M{x+28} {y-7} L{x+36} {y} L{x+28} {y+7}"
    o.append(f'<path class="hp__arrow" pathLength="1" style="--d:{delay}s" d="{d}"/>')


HP_TITLE = "The research loop: synthesise, measure, model, repeat"
HP_DESC = ("Three linked panels. A 96-well plate of polymer reactions, a solution-scattering "
           "detector image, and a scattering curve with a small neural network, joined by a "
           "return arrow back to the plate.")
HP_HITS = {(2, 9), (5, 10), (6, 7)}


def hero_pipeline(det_q, det_i, curve_pts, *, w=1140, h=316):
    """Wide layout: the three stages side by side."""
    o = [svg_open(w, h, HP_TITLE, HP_DESC), '<g class="hp">']
    px, py, pitch, r = 24, 56, 21, 7.6
    _hp_label(o, px, 22, "Synthesise", "96 polymer reactions, one plate")
    _hp_plate(o, px, py, 12, 8, pitch, r, HP_HITS)
    plate_w = 12 * pitch
    mid = py + 4 * pitch

    _hp_arrow(o, px + plate_w + 14, mid, 1.0)

    dx = px + plate_w + 74
    dcx, dr0, dstop = dx + 96, 92, 20
    _hp_label(o, dx, 22, "Measure", "solution scattering, ring by ring")
    _hp_rings(o, dcx, mid, dr0, dstop, 104, det_q, det_i, 1.15)

    _hp_arrow(o, dcx + dr0 + 22, mid, 1.9)

    mx = dcx + dr0 + 78
    _hp_label(o, mx, 22, "Model", "fit the curve, learn the rule")
    _hp_model(o, mx, 56, w - mx - 24, 108, curve_pts, 226, 2.0)

    lx0, lx1, ly = mx + (w - mx - 24) * 0.5, px + plate_w * 0.5, 292
    o.append(f'<path class="hp__loop" pathLength="1" d="M{lx0:.0f} 266 C{lx0:.0f} {ly} '
             f'{lx1:.0f} {ly} {lx1:.0f} 236 M{lx1-7:.0f} 246 L{lx1:.0f} 236 L{lx1+7:.0f} 246"/>')
    o.append(txt((lx0 + lx1) / 2, ly + 12, "the next ninety-six are chosen by the model", "hp__loopc"))
    o.append("</g></svg>")
    return "".join(o)


def hero_pipeline_stacked(det_q, det_i, curve_pts, *, w=364):
    """Narrow layout: the same three stages, stacked, with the loop down the left.

    Showing only one stage on a phone loses the whole point of the figure, so the
    panels stack rather than being dropped."""
    # Lay the stack out first, then size the viewBox to it -- a hardcoded height
    # let the return path and its caption spill onto the paragraph below.
    L = 44                       # left gutter reserved for the return path
    pitch = 25
    plate_bottom = 46 + 8 * pitch
    dtop = plate_bottom + 60
    dcy, dr0 = dtop + 130, 96
    mtop = dcy + dr0 + 64
    by = mtop + 190
    h = by + 66

    o = [svg_open(w, h, HP_TITLE, HP_DESC), '<g class="hp">']
    _hp_label(o, L, 16, "Synthesise", "96 polymer reactions, one plate")
    # 12 x 8 on the phone too: the caption says ninety-six, so the figure shows
    # ninety-six.
    _hp_plate(o, L, 46, 12, 8, pitch, 9.0, HP_HITS)
    plate_mid = 46 + 4 * pitch

    _hp_arrow(o, L + 6 * pitch, plate_bottom + 14, 1.0, vertical=True)

    _hp_label(o, L, dtop, "Measure", "solution scattering, ring by ring")
    dcx = L + 6 * pitch
    _hp_rings(o, dcx, dcy, dr0, 20, 104, det_q, det_i, 1.15)

    _hp_arrow(o, dcx, dcy + dr0 + 18, 1.9, vertical=True)

    _hp_label(o, L, mtop, "Model", "fit the curve, learn the rule")
    _hp_model(o, L, mtop + 26, w - L - 16, 82, curve_pts, mtop + 148, 2.0)

    # Return path runs down the left gutter and re-enters the plate at its mid
    # height -- entering at the top crossed the "Synthesise" caption.
    o.append(f'<path class="hp__loop" pathLength="1" d="M{dcx:.0f} {by} L{dcx:.0f} {by+16} '
             f'Q{dcx:.0f} {by+30} {dcx-30:.0f} {by+30} L26 {by+30} Q14 {by+30} 14 {by+18} '
             f'L14 {plate_mid+14:.0f} Q14 {plate_mid:.0f} 26 {plate_mid:.0f} '
             f'L{L-10:.0f} {plate_mid:.0f} M{L-18:.0f} {plate_mid-6:.0f} '
             f'L{L-10:.0f} {plate_mid:.0f} L{L-18:.0f} {plate_mid+6:.0f}"/>')
    o.append(txt(w / 2 + 10, by + 48, "the next ninety-six are chosen by the model", "hp__loopc"))
    o.append("</g></svg>")
    return "".join(o)


# =========================================================================
# Area thumbnails -- compact, real, one per research area
# =========================================================================

def thumb_plate(w=250, h=96):
    pitch, r = 20, 7.2
    o = [svg_open(w, h, "A 96-well plate reading out, three wells scoring as hits")]
    for rr in range(4):
        for cc in range(12):
            cx, cy = 8 + r + cc * pitch, 12 + r + rr * pitch
            o.append(f'<circle class="hp__well" cx="{cx:.1f}" cy="{cy:.1f}" r="{r}"/>')
            v = 0.14 + (cc / 11) ** 1.5 * 0.72
            hit = (rr, cc) in {(1, 10), (3, 9)}
            o.append(f'<circle class="th__d{" th__d--hit" if hit else ""}" cx="{cx:.1f}" '
                     f'cy="{cy:.1f}" r="{r-1.2:.1f}" opacity="{1.0 if hit else v:.2f}"/>')
    o.append("</svg>")
    return "".join(o)


def thumb_scale(w=250, h=96):
    """The magnitude gap: what gets made against what could be made."""
    vals = [(112, "112"), (2500, "2.5k"), (2_100_000, "2.1M")]
    X = Log(60, 4_000_000, 20, w - 34)
    o = [svg_open(w, h, "Three dataset sizes on a log axis, from 112 to 2.1 million")]
    o.append(f'<line class="th__ax" x1="20" y1="54" x2="{w-34}" y2="54"/>')
    for i, (v, lab) in enumerate(vals):
        x = X(v)
        last = i == len(vals) - 1
        o.append(f'<circle class="th__d{"" if last else " th__d--dim"}" cx="{x:.1f}" cy="54" '
                 f'r="{7 if last else 5.5}" opacity="1"/>')
        o.append(txt(x, 34, lab, "th__lbl"))
    o.append(txt(20, 80, "made", "th__sub", "start"))
    o.append(txt(w - 34, 80, "possible", "th__sub", "end"))
    o.append("</svg>")
    return "".join(o)


def thumb_rings(q, iq, curve, w=250, h=96, decades=5.0, gamma=1.0):
    """Detector rings beside the curve pulled out of them."""
    cx, cy, r0, stop, n = 50, 48, 40, 8, 54
    o = [svg_open(w, h, "A scattering detector image beside the curve extracted from it")]
    lmax = math.log10(max(iq)); lmin = lmax - decades
    step = (r0 - stop) / n
    for k in range(n):
        rr = stop + step * k
        qi = min(len(q) - 1, int(k / (n - 1) * (len(q) - 1)))
        v = max(0.0, min(1.0, (math.log10(iq[qi]) - lmin) / (lmax - lmin)))
        o.append(f'<circle class="hp__ring" cx="{cx}" cy="{cy}" r="{rr+step/2:.2f}" '
                 f'stroke-width="{step+0.8:.2f}" opacity="{v**gamma:.3f}"/>')
    o.append(f'<circle class="hp__stop" cx="{cx}" cy="{cy}" r="{stop}"/>')
    o.append('<path class="th__arrow" d="M100 48 L120 48 M114 43 L120 48 L114 53"/>')
    XX = Lin(min(a for a, _ in curve), max(a for a, _ in curve), 134, w - 12)
    YY = Lin(0, max(b for _, b in curve) * 1.08, 84, 16)
    d = "M" + " L".join(f"{XX(a):.1f} {YY(b):.1f}" for a, b in curve)
    o.append(f'<path class="th__curve" d="{d}"/>')
    o.append("</svg>")
    return "".join(o)
