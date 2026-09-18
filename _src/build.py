#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Static site generator for emanahmed.org.

    python3 _src/build.py

Writes HTML to the repository root. Edit _src/data.py, _src/notes.py or this
file -- never the generated .html, it will be overwritten.
"""
import json, os, random, re, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from data import SITE, PROFILE, EXPERTISE, PUBLICATIONS, PUBLISHED, AREAS, METHODS
from notes import NOTES

TODAY = datetime.date.today().isoformat()
P = PROFILE
M = P["metrics"]

# --------------------------------------------------------------------------
# Icons -- 1.5px stroke, 24px grid, currentColor
# --------------------------------------------------------------------------
I = {
 "ext":'<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><path d="M15 3h6v6"/><path d="M10 14 21 3"/>',
 "download":'<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
 "copy":'<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
 "mail":'<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/>',
 "cap":'<path d="M22 10v6"/><path d="m2 10 10-5 10 5-10 5z"/><path d="M6 12v5c3 2.5 9 2.5 12 0v-5"/>',
 "in":'<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-13h4v1.5"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>',
 "doc":'<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M8 13h8M8 17h5"/>',
 "sun":'<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
 "moon":'<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8"/>',
 "menu":'<path d="M3 6h18M3 12h18M3 18h18"/>',
 "flask":'<path d="M9 2v7.5L3.4 19a2 2 0 0 0 1.7 3h13.8a2 2 0 0 0 1.7-3L15 9.5V2"/><path d="M7.5 2h9"/><path d="M6.2 15h11.6"/><circle cx="10" cy="18" r=".6" fill="currentColor"/><circle cx="14.5" cy="17" r=".9" fill="currentColor"/>',
 "model":'<circle cx="5" cy="6" r="2"/><circle cx="5" cy="18" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="7" r="2"/><circle cx="19" cy="17" r="2"/><path d="M6.8 7 10.4 11M6.8 17 10.4 13M13.8 11.2 17.2 8M13.8 12.8 17.2 16"/>',
 "robot":'<rect x="4" y="8" width="16" height="12" rx="2"/><path d="M12 8V4M9 4h6"/><circle cx="9" cy="14" r="1.2" fill="currentColor"/><circle cx="15" cy="14" r="1.2" fill="currentColor"/><path d="M2 12v4M22 12v4"/>',
 "pin":'<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
 "code":'<path d="m8 6-6 6 6 6M16 6l6 6-6 6"/>',
}
def ico(n, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[n]}</svg>')

def esc(s):
    return (str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;"))

# --------------------------------------------------------------------------
# Navigation
# --------------------------------------------------------------------------
NAV = [("index.html","Home"), ("research.html","Research"), ("publications.html","Publications"),
       ("blog.html","Notes"), ("cv.html","CV"), ("teaching.html","Teaching"),
       ("collaborators.html","Lab"), ("contact.html","Contact")]

def rail(cur, up=""):
    links = "".join(
        f'<a class="rail__link" href="{up}{h}"{" aria-current=\"page\"" if h==cur else ""}>{t}</a>'
        for h, t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="rail">
  <div class="wrap rail__in">
    <a class="rail__id" href="{up}index.html">Eman Ahmed<span>Rutgers BME</span></a>
    <nav class="rail__nav" id="nav" aria-label="Main">{links}</nav>
    <div class="rail__tools">
      <button class="iconbtn" id="theme" type="button" aria-label="Switch colour theme">
        {ico("sun","theme__light")}{ico("moon","theme__dark")}
      </button>
      <button class="iconbtn rail__burger" id="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nav">{ico("menu")}</button>
    </div>
  </div>
</header>'''

def foot(up=""):
    navls = "".join(f'<li><a href="{up}{h}">{t}</a></li>' for h, t in NAV[1:5])
    navrs = "".join(f'<li><a href="{up}{h}">{t}</a></li>' for h, t in NAV[5:])
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="foot__grid">
      <div>
        <h2>Eman Ahmed</h2>
        <p>PhD candidate in biomedical engineering at Rutgers, working on high-throughput
        polymer chemistry, machine learning for biomaterials, and keeping enzymes alive in
        organic solvents. Based in the {P["lab"]}.</p>
        <p style="margin-bottom:0"><a href="mailto:{P["email"]}">{P["email"]}</a></p>
      </div>
      <div><h2>Sections</h2><ul>{navls}</ul></div>
      <div><h2>Elsewhere</h2><ul>
        <li><a href="{P["scholar"]}" rel="me noopener">Google Scholar</a></li>
        <li><a href="{P["linkedin"]}" rel="me noopener">LinkedIn</a></li>
        <li><a href="{P["lab_url"]}" rel="noopener">Gormley Lab</a></li>
        {navrs}
      </ul></div>
    </div>
    <div class="foot__base">
      <p>&copy; {datetime.date.today().year} Eman Ahmed. {P["city"]}, {P["region"]}, USA.</p>
      <p>Citation metrics from Google Scholar, {M["asof"]}.</p>
    </div>
  </div>
</footer>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script src="{up}js/main.js" defer></script>
</body>
</html>'''

# --------------------------------------------------------------------------
# <head>
# --------------------------------------------------------------------------
def head(title, desc, path, jsonld, extra="", up="", og_type="website", img="images/og-image.png"):
    url = f"{SITE}/{path}" if path != "index.html" else f"{SITE}/"
    blocks = "\n".join(
        '<script type="application/ld+json">%s</script>' % json.dumps(b, ensure_ascii=False, separators=(",", ":"))
        for b in jsonld)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="Eman Ahmed">
<link rel="canonical" href="{url}">

<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Eman Ahmed">
<meta property="og:locale" content="en_US">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Eman Ahmed, PhD candidate in biomedical engineering at Rutgers University">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}/{img}">
{extra}
<link rel="icon" type="image/svg+xml" href="{up}images/favicon.svg">
<link rel="apple-touch-icon" href="{up}images/apple-touch-icon.png">
<meta name="theme-color" content="#070D18" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#F6F8FB" media="(prefers-color-scheme: light)">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;450;500;550;600&display=swap">
<link rel="stylesheet" href="{up}css/styles.css">
<script>try{{var t=localStorage.getItem("theme");if(t)document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
{blocks}
</head>
<body>'''

# --------------------------------------------------------------------------
# JSON-LD building blocks
# --------------------------------------------------------------------------
PERSON_ID = f"{SITE}/#eman-ahmed"

def person_node():
    return {
        "@context": "https://schema.org", "@type": "Person", "@id": PERSON_ID,
        "name": P["name"], "givenName": P["given"], "familyName": P["family"],
        "jobTitle": P["role"], "url": SITE + "/",
        "image": {"@type": "ImageObject", "url": f"{SITE}/{P['photo']}",
                  "caption": "Eman Ahmed, PhD candidate in biomedical engineering at Rutgers University"},
        "email": f"mailto:{P['email']}",
        "description": ("PhD candidate in biomedical engineering at Rutgers University working on "
                        "high-throughput polymer chemistry, laboratory automation and machine learning "
                        "for biomaterials discovery and protein stabilization."),
        "affiliation": {"@type": "CollegeOrUniversity", "name": P["org"], "url": P["org_url"],
                        "department": {"@type": "Organization", "name": P["dept"], "url": P["dept_url"]}},
        "alumniOf": {"@type": "CollegeOrUniversity", "name": P["org"], "url": P["org_url"]},
        "worksFor": {"@type": "Organization", "name": P["dept"], "url": P["dept_url"],
                     "parentOrganization": {"@type": "CollegeOrUniversity", "name": P["org"]}},
        "address": {"@type": "PostalAddress", "addressLocality": P["city"],
                    "addressRegion": P["region"], "addressCountry": P["country"]},
        "knowsAbout": EXPERTISE,
        "sameAs": [P["scholar"], P["linkedin"]],
        "knowsLanguage": ["en"],
    }

def article_node(p, with_ctx=True):
    n = {
        "@type": "ScholarlyArticle",
        "@id": f"{SITE}/publications/{p['slug']}.html#article",
        "headline": p["title"], "name": p["title"],
        "url": f"{SITE}/publications/{p['slug']}.html",
        "author": [{"@type": "Person", "name": a,
                    **({"@id": PERSON_ID} if a == P["name"] else {})} for a in p["authors"]],
        "datePublished": p["date"],
        "isPartOf": {"@type": "PublicationIssue", "issueNumber": p.get("issue"),
                     "isPartOf": {"@type": "Periodical", "name": p["journal"]}},
        "publisher": {"@type": "Organization", "name": p["journal"]},
        "pagination": p.get("pages"),
        "abstract": p["abstract"],
        "keywords": ", ".join(p.get("keywords", [])),
        "identifier": [{"@type": "PropertyValue", "propertyID": "DOI", "value": p["doi"]}],
        "sameAs": f"https://doi.org/{p['doi']}",
        "inLanguage": "en",
    }
    if p.get("pmid"):
        n["identifier"].append({"@type": "PropertyValue", "propertyID": "PMID", "value": p["pmid"]})
    if p.get("volume"):
        n["isPartOf"]["isPartOf"]["volumeNumber"] = p["volume"]
    if with_ctx:
        n = {"@context": "https://schema.org", **n}
    return n

def crumbs_node(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": nm,
                                 **({"item": f"{SITE}/{u}"} if u else {})}
                                for i, (nm, u) in enumerate(items)]}

def website_node():
    return {"@context": "https://schema.org", "@type": "WebSite", "@id": f"{SITE}/#website",
            "url": SITE + "/", "name": "Eman Ahmed",
            "description": "Research site of Eman Ahmed, PhD candidate in biomedical engineering at Rutgers University.",
            "inLanguage": "en", "publisher": {"@id": PERSON_ID}}

def crumbs_html(items, up=""):
    out = []
    for i, (nm, u) in enumerate(items):
        if i: out.append('<span aria-hidden="true">/</span>')
        out.append(f'<a href="{up}{u}">{nm}</a>' if u else f"<span>{nm}</span>")
    return '<nav class="crumb" aria-label="Breadcrumb">' + "".join(out) + "</nav>"

# --------------------------------------------------------------------------
# 96-well plate: the hero. Wells read out column by column.
# --------------------------------------------------------------------------
def plate_svg():
    rnd = random.Random(1489)          # fixed seed: the plate is identical every build
    PITCH, R, PADX, PADY = 27, 10.5, 22, 20
    W = PADX + 12 * PITCH + 8
    H = PADY + 8 * PITCH + 8
    o = [f'<svg class="plate__svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-labelledby="plate-t"><title id="plate-t">A 96-well plate reading out: '
         f'signal rises across the columns, with four high-response wells highlighted.</title>']
    for c in range(12):
        o.append(f'<text class="plate__lbl" x="{PADX + R + c*PITCH}" y="12" text-anchor="middle">{c+1}</text>')
    for r in range(8):
        o.append(f'<text class="plate__lbl" x="10" y="{PADY + R + r*PITCH + 3}" text-anchor="middle">{"ABCDEFGH"[r]}</text>')
    hits = {(2, 9), (5, 10), (3, 11), (6, 8)}
    for r in range(8):
        for c in range(12):
            cx, cy = PADX + R + c * PITCH, PADY + R + r * PITCH
            o.append(f'<circle class="plate__well" cx="{cx}" cy="{cy}" r="{R}"/>')
            base = 0.10 + (c / 11) ** 1.5 * 0.72
            val = max(0.05, min(0.95, base + rnd.uniform(-0.13, 0.13)))
            hit = (r, c) in hits
            if hit: val = 0.95
            delay = c * 0.05 + r * 0.014
            o.append(
                f'<circle class="plate__read{" plate__read--hit" if hit else ""}" '
                f'cx="{cx}" cy="{cy}" r="{R - 1.5}" '
                f'style="--o:{val:.2f};animation-delay:{delay:.2f}s;'
                f'transform-origin:{cx}px {cy}px"/>')
    o.append("</svg>")
    return "".join(o)

# --------------------------------------------------------------------------
# Shared fragments
# --------------------------------------------------------------------------
def authors_html(p):
    return ", ".join(f"<b>{a}</b>" if a == P["name"] else a for a in p["authors"])

def venue_html(p):
    if p["status"] != "published":
        return "Manuscript in preparation"
    bits = f'{p["journal"]}'
    if p.get("volume"):
        bits += f' {p["volume"]}'
        if p.get("issue"): bits += f'({p["issue"]})'
        if p.get("pages"): bits += f', {p["pages"]}'
    return f'{bits} &middot; {p["year"]}'

def bibtex(p):
    key = f"{P['family'].lower()}{p['year']}{p['slug'].split('-')[0]}"
    au = " and ".join(f"{a.split()[-1]}, {' '.join(a.split()[:-1])}" for a in p["authors"])
    return (f"@article{{{key},\n"
            f"  title   = {{{p['title']}}},\n"
            f"  author  = {{{au}}},\n"
            f"  journal = {{{p['journal']}}},\n"
            f"  volume  = {{{p.get('volume','')}}},\n"
            f"  number  = {{{p.get('issue','')}}},\n"
            f"  pages   = {{{p.get('pages','')}}},\n"
            f"  year    = {{{p['year']}}},\n"
            f"  doi     = {{{p['doi']}}}\n}}")

def apa(p):
    names = []
    for a in p["authors"]:
        parts = a.split()
        names.append(f"{parts[-1]}, " + " ".join(x[0] + "." for x in parts[:-1]))
    au = ", ".join(names[:-1]) + (" & " + names[-1] if len(names) > 1 else "")
    v = f"{p['journal']}, {p.get('volume','')}({p.get('issue','')}), {p.get('pages','')}"
    return f"{au} ({p['year']}). {p['title']}. {v}. https://doi.org/{p['doi']}"

def pub_card(p, i, up=""):
    if p["status"] != "published":
        return f'''<article class="pub">
  <p class="pub__meta"><span class="pub__role">First author</span><span>In preparation</span></p>
  <h3 class="pub__t">{p["title"]}</h3>
  <p class="pub__au">{authors_html(p)}</p>
  <p class="pub__venue">Manuscript in preparation &middot; {P["lab"]}, Rutgers University</p>
  <p class="pub__sum">{p["plain"]}</p>
</article>'''
    role = "First author" if p["role"] == "first" else "Co-author"
    cites = (f'<span class="pub__cites">{p["citations"]} citations</span>' if p.get("citations") else "")
    return f'''<article class="pub{" pub--lead" if p["role"]=="first" else ""}">
  <p class="pub__meta"><span class="pub__role">{role}</span><span>{p["type"]}</span><span>{p["year"]}</span>{cites}</p>
  <h3 class="pub__t"><a href="{up}publications/{p["slug"]}.html">{p["title"]}</a></h3>
  <p class="pub__au">{authors_html(p)}</p>
  <p class="pub__venue">{venue_html(p)}</p>
  <p class="pub__sum">{p["plain"]}</p>
  <div class="pub__acts">
    <a class="chip" href="{up}publications/{p["slug"]}.html">Full record</a>
    <a class="chip" href="https://doi.org/{p["doi"]}" rel="noopener">{ico("ext")}doi.org/{p["doi"]}</a>
    <button class="chip" type="button" data-copy="{esc(apa(p))}">{ico("copy")}Copy citation</button>
  </div>
</article>'''

def area_block(a, up=""):
    tags = "".join(f'<li><span class="tag">{t}</span></li>' for t in a["tags"])
    body = "".join(f"<p>{x}</p>" for x in a["body"])
    return f'''<article class="area" id="{a["id"]}">
  <div class="area__mark">{ico(a["icon"])}</div>
  <div><h3 class="area__t">{a["title"]}</h3><p class="data" style="color:var(--ink-3);font-size:var(--t-xs);margin:0">{a["lede"]}</p></div>
  <div class="area__body">{body}<ul class="tags">{tags}</ul></div>
</article>'''

def byline(up="", aside=False):
    return f'''<div class="byline">
  <img src="{up}{P["photo"]}" width="152" height="152" loading="lazy"
       alt="Portrait of Eman Ahmed, PhD candidate in biomedical engineering at Rutgers University">
  <div>
    <p class="byline__t"><b>Eman Ahmed</b></p>
    <p class="byline__s">PhD candidate, {P["dept"]},<br>Rutgers University &middot; {P["lab"]}</p>
  </div>
</div>'''


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    return path

PAGES = []   # (path, lastmod, priority, changefreq)

# --------------------------------------------------------------------------
# Home
# --------------------------------------------------------------------------
def build_home():
    desc = ("PhD candidate at Rutgers building robot-run polymer chemistry and the machine learning that "
            "reads it: ML for biomaterials, photo-ATRP and SAXS.")
    ld = [person_node(), website_node(),
          {"@context": "https://schema.org", "@type": "ProfilePage",
           "@id": f"{SITE}/#profilepage", "url": SITE + "/", "name": "Eman Ahmed",
           "mainEntity": {"@id": PERSON_ID},
           "about": {"@id": PERSON_ID}, "dateModified": TODAY},
          {"@context": "https://schema.org", "@type": "ItemList",
           "name": "Publications by Eman Ahmed",
           "itemListElement": [{"@type": "ListItem", "position": i + 1,
                                "url": f"{SITE}/publications/{p['slug']}.html", "name": p["title"]}
                               for i, p in enumerate(PUBLISHED)]}]
    areas = "".join(area_block(a) for a in AREAS)
    pubs = "".join(pub_card(p, i) for i, p in enumerate(PUBLICATIONS))
    notes = "".join(f'''<article class="note">
  <p class="note__date"><time datetime="{n["date"]}">{n["date_h"]}</time></p>
  <div><h3 class="note__t"><a href="notes/{n["slug"]}.html">{n["title"]}</a></h3>
  <p class="note__d">{n["desc"]}</p></div>
</article>''' for n in NOTES[:2])

    body = f'''{rail("index.html")}
<main id="main">

<section class="hero">
  <div class="wrap hero__grid">
    <div>
      <h1>
        <span class="hero__name">Eman Ahmed &mdash; PhD candidate, Rutgers Biomedical Engineering</span>
        <span class="hero__line">Ninety-six polymers at a time.</span>
      </h1>
      <p class="hero__lede">I build <strong>high-throughput, robot-run polymer chemistry</strong> and the
      <strong>machine learning</strong> that reads what comes back &mdash; to find the polymers that keep enzymes
      soluble and working in solvents where they would normally fall apart.</p>
      <div class="hero__acts">
        <a class="btn btn--solid" href="research.html">Read the research</a>
        <a class="btn btn--line" href="publications.html">{ico("doc")}Publications</a>
        <a class="btn btn--line" href="{P["scholar"]}" rel="me noopener">{ico("cap")}Google Scholar</a>
      </div>
      <div class="readout">
        <div><span class="readout__v">{M["papers"]}</span><span class="readout__k">peer-reviewed papers, one as first author</span></div>
        <div><span class="readout__v">{M["citations"]}</span><span class="readout__k">citations</span></div>
        <div><span class="readout__v">{M["hindex"]}</span><span class="readout__k">h-index</span></div>
      </div>
      <p class="readout__note">Metrics from <a href="{P["scholar"]}" rel="noopener">Google Scholar</a>, {M["asof"]}.</p>
    </div>
    <figure class="plate">
      {plate_svg()}
      <figcaption><b>How the work runs.</b> One plate, ninety-six independent polymer formulations, every
      well measured the same way &mdash; including the ones that fail. Signal rises left to right across a
      composition gradient; four wells read out as hits.</figcaption>
    </figure>
  </div>
</section>

<section class="sec sec--sunk">
  <div class="wrap">
    <div class="sec__head sec__head--split">
      <h2>What I work on</h2>
      <p>Three connected problems: making enzymes survive outside water, generating enough polymer data
      to learn from, and building analysis that keeps pace with the synthesis.</p>
    </div>
    <div class="areas">{areas}</div>
    <p style="margin-top:var(--s6)"><a class="btn btn--line" href="research.html">Research in detail</a></p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec__head sec__head--split">
      <h2>Publications</h2>
      <p>Three peer-reviewed papers in <em>Tissue Engineering Part A</em>, <em>ACS Polymers Au</em> and
      <em>Biophysical Journal</em>, plus the doctoral manuscript in preparation. Each has a full record
      with the published abstract, citation formats and a link to the version of record.</p>
    </div>
    <div class="pubs">{pubs}</div>
  </div>
</section>

<section class="sec sec--sunk">
  <div class="wrap">
    <div class="sec__head sec__head--split">
      <h2>Research notes</h2>
      <p>Plain-language companions to the papers &mdash; what the method does, why it was built that way,
      and what it does not solve.</p>
    </div>
    <div class="notes">{notes}</div>
    <p style="margin-top:var(--s6)"><a class="btn btn--line" href="blog.html">All notes</a></p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="call">
      <h2>Working on something adjacent?</h2>
      <p>If you work on high-throughput polymer synthesis, machine learning for materials, SAXS analysis or
      enzyme stabilization, I would like to hear about it &mdash; whether that is a collaboration, a dataset
      worth combining, or a question about how one of these methods behaves in practice.</p>
      <div class="call__acts">
        <a class="btn btn--solid" href="contact.html">{ico("mail")}Get in touch</a>
        <a class="btn btn--line" href="assets/emancv.pdf" download>{ico("download")}Download CV</a>
      </div>
    </div>
  </div>
</section>

</main>'''
    write("index.html", head("Eman Ahmed | High-Throughput Polymer Chemistry &amp; ML",
                             desc, "index.html", ld) + body + foot())
    PAGES.append(("", TODAY, "1.0", "weekly"))

# --------------------------------------------------------------------------
# Publications index + one full record per paper
# --------------------------------------------------------------------------
def build_publications():
    desc = ("Papers by Eman Ahmed on machine learning for biomaterials, automated photo-ATRP and automated "
            "SAXS analysis. Abstracts, DOIs, BibTeX and APA citations.")
    ld = [crumbs_node([("Home", ""), ("Publications", "publications.html")]),
          {"@context": "https://schema.org", "@type": "CollectionPage",
           "url": f"{SITE}/publications.html", "name": "Publications | Eman Ahmed",
           "description": desc, "about": {"@id": PERSON_ID}, "dateModified": TODAY,
           "hasPart": [article_node(p, with_ctx=False) for p in PUBLISHED]}]
    pubs = "".join(pub_card(p, i) for i, p in enumerate(PUBLICATIONS))
    talks = [
        ("October 2025", "High-Throughput Approach for Evaluating Polymer-Enzyme Hybrids",
         "Biomedical Engineering Society (BMES) Annual Meeting, San Diego, California", "Oral presentation"),
        ("December 2024", "High-Throughput Approach for Evaluating Polymer-Enzyme Hybrids",
         "Biomedical Engineering Students Society (BESS) Symposium, Rutgers University", "Oral presentation"),
        ("October 2018", "Tension-Induced Rupture of Lipid Membranes",
         "Gulf Coast Undergraduate Research Symposium, Rice University, Houston, Texas", "Poster"),
        ("April 2018", "Tension-Induced Rupture of Lipid Membranes",
         "Aresty Undergraduate Research Symposium, Rutgers University", "Poster &middot; Honourable mention"),
    ]
    tl = "".join(f'''<div class="tl__item{" tl__item--on" if i==0 else ""}">
  <p class="tl__when">{w}</p><h3 class="tl__t">{t}</h3>
  <p class="tl__where">{v}</p><p class="data" style="color:var(--ink-3);font-size:var(--t-xs);margin:0">{k}</p>
</div>''' for i, (w, t, v, k) in enumerate(talks))

    body = f'''{rail("publications.html")}
<main id="main"><div class="wrap art">
  {crumbs_html([("Home","index.html"),("Publications",None)])}
  <div class="art__h">
    <h1>Publications</h1>
    <p class="hero__lede" style="margin-bottom:0">Three peer-reviewed papers and one manuscript in preparation,
    spanning machine learning for biomaterials discovery, automated polymer synthesis, and automated structural
    analysis. Every record below links to the version of record.</p>
  </div>

  <div class="readout" style="margin-bottom:var(--s8)">
    <div><span class="readout__v">{M["papers"]}</span><span class="readout__k">peer-reviewed papers</span></div>
    <div><span class="readout__v">{M["citations"]}</span><span class="readout__k">citations</span></div>
    <div><span class="readout__v">{M["hindex"]}</span><span class="readout__k">h-index</span></div>
  </div>

  <h2 class="sec__head" style="font-size:var(--t-xl);margin-bottom:var(--s5)">Journal articles</h2>
  <div class="pubs">{pubs}</div>

  <h2 style="font-size:var(--t-xl);margin:var(--s9) 0 var(--s5)">Conference presentations</h2>
  <div class="tl">{tl}</div>

  <div class="call" style="margin-top:var(--s9)">
    <h2>Citing this work</h2>
    <p>Each full record carries APA and BibTeX. For the complete, continuously updated list including
    citation counts, see the <a href="{P["scholar"]}" rel="noopener">Google Scholar profile</a>.</p>
  </div>
</div></main>'''
    write("publications.html", head("Publications | Eman Ahmed, Rutgers Biomedical Engineering",
                                    desc, "publications.html", ld) + body + foot())
    PAGES.append(("publications.html", TODAY, "0.9", "monthly"))

def build_pub_pages():
    for p in PUBLISHED:
        path = f"publications/{p['slug']}.html"
        desc = p.get("meta") or p["plain"][:155]
        # Highwire Press tags -- these are what Google Scholar actually reads.
        cm = [f'<meta name="citation_title" content="{esc(p["title"])}">']
        cm += [f'<meta name="citation_author" content="{esc(a)}">' for a in p["authors"]]
        cm += [
            f'<meta name="citation_publication_date" content="{p["date"].replace("-","/")}">',
            f'<meta name="citation_journal_title" content="{esc(p["journal"])}">',
            f'<meta name="citation_volume" content="{p.get("volume","")}">',
            f'<meta name="citation_issue" content="{p.get("issue","")}">',
            f'<meta name="citation_firstpage" content="{p.get("firstpage","")}">',
            f'<meta name="citation_lastpage" content="{p.get("lastpage","")}">',
            f'<meta name="citation_doi" content="{p["doi"]}">',
            f'<meta name="citation_abstract_html_url" content="https://doi.org/{p["doi"]}">',
            f'<meta name="citation_language" content="en">',
            f'<meta name="citation_keywords" content="{esc("; ".join(p.get("keywords",[])))}">',
        ]
        if p.get("pmid"):
            cm.append(f'<meta name="citation_pmid" content="{p["pmid"]}">')
        extra = "\n".join(cm)

        ld = [article_node(p),
              crumbs_node([("Home", ""), ("Publications", "publications.html"), (p["title"], path)])]

        why = "".join(f"<li>{x}</li>" for x in p.get("why", []))
        kw = "".join(f'<li><span class="tag">{k}</span></li>' for k in p.get("keywords", []))
        ids = [("DOI", f'<a href="https://doi.org/{p["doi"]}" rel="noopener">{p["doi"]}</a>')]
        if p.get("pmid"):
            ids.append(("PubMed", f'<a href="https://pubmed.ncbi.nlm.nih.gov/{p["pmid"]}/" rel="noopener">PMID {p["pmid"]}</a>'))
        if p.get("pmcid"):
            ids.append(("PubMed Central", f'<a href="https://pmc.ncbi.nlm.nih.gov/articles/{p["pmcid"]}/" rel="noopener">{p["pmcid"]}</a>'))
        if p.get("code"):
            ids.append(("Software", f'<a href="{p["code"]}" rel="noopener">{p["code_label"]}</a>'))
        ids += [("Published", p["date_h"]),
                ("Citations", f'{p["citations"]} &middot; Scholar, {M["asof"]}')]
        dl = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in ids)

        body = f'''{rail("publications.html","../")}
<main id="main"><div class="wrap art">
  {crumbs_html([("Home","index.html"),("Publications","publications.html"),(p["type"],None)],"../")}
  <div class="art__grid">
    <article>
      <div class="art__h">
        <p class="art__kicker">{"First-author" if p["role"]=="first" else "Co-authored"} {p["type"].lower()} &middot; {p["year"]}</p>
        <h1>{p["title"]}</h1>
        <p class="art__au">{authors_html(p)}</p>
        <p class="art__venue">{venue_html(p)}</p>
      </div>
      <div class="prose">
        <h2>In short</h2>
        <p>{p["plain"]}</p>
        <h2>Why it matters</h2>
        <ul>{why}</ul>
        <h2>Abstract</h2>
        <blockquote><p>{p["abstract"]}</p>
        <p class="data" style="font-size:var(--t-xs);color:var(--ink-3);margin-bottom:0">
        Published abstract, reproduced from the version of record.</p></blockquote>
        <h2>Keywords</h2>
        <ul class="tags">{kw}</ul>
        <h2>Cite this paper</h2>
        <div class="disclose__in" style="border:0;padding:0">
          <h4>APA</h4>
          <pre>{esc(apa(p))}</pre>
          <p style="margin:var(--s3) 0 var(--s5)"><button class="chip" type="button" data-copy="{esc(apa(p))}">{ico("copy")}Copy APA</button></p>
          <h4>BibTeX</h4>
          <pre>{esc(bibtex(p))}</pre>
          <p style="margin:var(--s3) 0 0"><button class="chip" type="button" data-copy="{esc(bibtex(p))}">{ico("copy")}Copy BibTeX</button></p>
        </div>
      </div>
      <p style="margin-top:var(--s8)"><a class="btn btn--solid" href="https://doi.org/{p["doi"]}" rel="noopener">{ico("ext")}Read the paper</a></p>
    </article>
    <aside class="aside">
      <div class="aside__box">
        <h2>Record</h2>
        <dl class="dl">{dl}</dl>
      </div>
      <div class="aside__box">
        <h2>More</h2>
        <dl class="dl">
          <dt>All publications</dt><dd><a href="../publications.html">Publication list</a></dd>
          <dt>Scholar profile</dt><dd><a href="{P["scholar"]}" rel="noopener">Google Scholar</a></dd>
          <dt>Research context</dt><dd><a href="../research.html">Research areas</a></dd>
        </dl>
      </div>
    </aside>
  </div>
</div></main>'''
        title = f'{p.get("short", p["title"])} | Eman Ahmed'
        write(path, head(title, desc, path, ld, extra=extra, up="../", og_type="article") + body + foot("../"))
        PAGES.append((path, TODAY, "0.8", "yearly"))

# --------------------------------------------------------------------------
# Research
# --------------------------------------------------------------------------
def build_research():
    desc = ("Polymer-stabilized enzymes in organic solvents, machine learning for biomaterial "
            "structure-function mapping, and automated photo-ATRP and SAXS at Rutgers.")
    faq = [
        ("What does Eman Ahmed research?",
         "Eman Ahmed researches high-throughput polymer chemistry and machine learning for biomaterials at "
         "Rutgers University. Her doctoral work develops automated, plate-based assays that identify random "
         "copolymers capable of keeping enzymes soluble and catalytically active in water-miscible organic "
         "solvents. She also works on automated photoinduced ATRP and on machine-learning-assisted analysis "
         "of small-angle X-ray scattering data."),
        ("Why does high-throughput experimentation matter for biomaterials?",
         "Biomaterial performance usually depends on several structural properties interacting at once, so "
         "varying one factor at a time samples the design space too sparsely to find good candidates. "
         "High-throughput experimentation runs many formulations in parallel under identical measurement "
         "conditions, and it retains failed conditions as data rather than discarding them, which produces "
         "the balanced datasets machine learning models need."),
        ("What is oxygen-tolerant ATRP and why does it enable automation?",
         "Atom transfer radical polymerization traditionally requires oxygen-free conditions, which means "
         "sealed, degassed glassware that cannot be parallelised. Oxygen-tolerant reversible-deactivation "
         "radical polymerization consumes oxygen within the reaction system itself, so the chemistry can "
         "proceed in open labware such as 96-well plates. That is what makes it accessible to liquid-handling "
         "robots and to high-throughput screening."),
        ("What is SAXS Assistant?",
         "SAXS Assistant is an open-source Python tool, co-authored by Eman Ahmed and published in Biophysical "
         "Journal, that automates small-angle X-ray scattering analysis. It extracts the Guinier radius of "
         "gyration, the pair distance distribution function, maximum particle dimension and Kratky features, "
         "uses a multilayer perceptron trained on 1,940 experimental SASBDB profiles to estimate maximum "
         "particle dimension, and flags low-confidence results instead of reporting them silently."),
        ("Who is Eman Ahmed's PhD advisor?",
         "Eman Ahmed is advised by Adam J. Gormley in the Department of Biomedical Engineering at Rutgers, "
         "The State University of New Jersey. The Gormley Lab works on polymer-based biomaterials, "
         "high-throughput polymer synthesis and screening, and machine learning for biomaterial design."),
    ]
    ld = [crumbs_node([("Home", ""), ("Research", "research.html")]),
          {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q,
                           "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
          {"@context": "https://schema.org", "@type": "WebPage", "url": f"{SITE}/research.html",
           "name": "Research | Eman Ahmed", "description": desc, "about": {"@id": PERSON_ID},
           "dateModified": TODAY, "mentions": [{"@type": "Thing", "name": k} for k in EXPERTISE]}]

    areas = "".join(area_block(a) for a in AREAS)
    meth = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in METHODS)
    faqh = "".join(f'''<div><dt>{q}</dt><dd><p>{a}</p></dd></div>''' for q, a in faq)
    past = f'''<div class="tl">
  <div class="tl__item"><p class="tl__when">2017&ndash;2018 &middot; Neimark Lab, Rutgers</p>
    <h3 class="tl__t">Tension-induced rupture of lipid membranes</h3>
    <p class="tl__where">Undergraduate research, Department of Chemical &amp; Biochemical Engineering</p>
    <ul><li>Coarse-grained computational study of how lipid bilayers fail under applied tension.</li>
    <li>Presented at the Gulf Coast Undergraduate Research Symposium, Rice University (2018).</li>
    <li>Honourable mention, Aresty Undergraduate Research Symposium, Rutgers (2018).</li></ul></div>
  <div class="tl__item"><p class="tl__when">2018 &middot; Gormley Lab, Rutgers</p>
    <h3 class="tl__t">Polymer characterisation</h3>
    <p class="tl__where">Undergraduate research, Department of Biomedical Engineering</p>
    <ul><li>Polymer vacuum filtration and solubility characterisation for polymer-based biomaterial systems.</li></ul></div>
</div>'''

    body = f'''{rail("research.html")}
<main id="main">
<div class="wrap art art--lead">
  {crumbs_html([("Home","index.html"),("Research",None)])}
  <div class="art__h">
    <h1>Making polymer discovery an empirical search rather than a guess</h1>
    <p class="hero__lede" style="margin-bottom:0">Biomaterial performance comes from several structural
    properties interacting at once, which makes it a poor fit for one-variable-at-a-time chemistry. My work
    runs the search in parallel instead &mdash; plate-based synthesis, consistent measurement, and models
    trained on everything that comes back.</p>
  </div>
</div>

<section class="sec sec--first sec--tight">
  <div class="wrap">
    <div class="areas">{areas}</div>
  </div>
</section>

<section class="sec sec--sunk">
  <div class="wrap">
    <div class="sec__head sec__head--split">
      <h2>Methods and instrumentation</h2>
      <p>What I actually use day to day, at the bench and in code.</p>
    </div>
    <dl class="facts">{meth}</dl>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec__head sec__head--split">
      <h2>Common questions</h2>
      <p>The questions I am asked most often about this work, answered directly.</p>
    </div>
    <dl class="facts">{faqh}</dl>
  </div>
</section>

<section class="sec sec--sunk">
  <div class="wrap">
    <div class="sec__head sec__head--split">
      <h2>Earlier work</h2>
      <p>Undergraduate research that led here.</p>
    </div>
    {past}
  </div>
</section>

<section class="sec">
  <div class="wrap"><div class="call">
    <h2>Related reading</h2>
    <p>The three research areas above map onto three published papers. Each has a full record with the
    published abstract, identifiers and citation formats.</p>
    <div class="call__acts">
      <a class="btn btn--solid" href="publications.html">{ico("doc")}Publications</a>
      <a class="btn btn--line" href="blog.html">Research notes</a>
    </div>
  </div></div>
</section>
</main>'''
    write("research.html", head("Research | Polymer Automation &amp; ML | Eman Ahmed",
                               desc, "research.html", ld) + body + foot())
    PAGES.append(("research.html", TODAY, "0.9", "monthly"))

# --------------------------------------------------------------------------
# Notes index (kept at blog.html to preserve the indexed URL) + note pages
# --------------------------------------------------------------------------
PROV = ("These notes are plain-language companions to peer-reviewed work. Every factual claim traces to "
        "the paper linked at the end of the note.")

def build_notes_index():
    desc = ("Notes on oxygen-tolerant ATRP and lab automation, machine-learning-assisted SAXS analysis, and "
            "why biomaterials datasets need the experiments that failed.")
    ld = [crumbs_node([("Home", ""), ("Notes", "blog.html")]),
          {"@context": "https://schema.org", "@type": "Blog", "@id": f"{SITE}/blog.html#blog",
           "url": f"{SITE}/blog.html", "name": "Research notes | Eman Ahmed",
           "description": desc, "author": {"@id": PERSON_ID}, "publisher": {"@id": PERSON_ID},
           "blogPost": [{"@type": "BlogPosting", "headline": n["title"],
                         "url": f"{SITE}/notes/{n['slug']}.html", "datePublished": n["date"],
                         "description": n["desc"], "author": {"@id": PERSON_ID}} for n in NOTES]}]
    items = "".join(f'''<article class="note">
  <p class="note__date"><time datetime="{n["date"]}">{n["date_h"]}</time><br>{n["reading"]} min read</p>
  <div>
    <h2 class="note__t"><a href="notes/{n["slug"]}.html">{n["title"]}</a></h2>
    <p class="note__d">{n["desc"]}</p>
    <ul class="tags">{"".join(f'<li><span class="tag">{t}</span></li>' for t in n["tags"])}</ul>
  </div>
</article>''' for n in NOTES)
    body = f'''{rail("blog.html")}
<main id="main"><div class="wrap art">
  {crumbs_html([("Home","index.html"),("Notes",None)])}
  <div class="art__h">
    <h1>Research notes</h1>
    <p class="hero__lede">Plain-language companions to the papers: what a method does, why it was built that
    way, and what it does not solve. Written for researchers outside the specific subfield.</p>
    <p class="data" style="font-size:var(--t-xs);color:var(--ink-3);margin-bottom:0">{PROV}</p>
  </div>
  <div class="notes">{items}</div>
</div></main>'''
    write("blog.html", head("Research Notes | Polymer Automation &amp; SAXS | Eman Ahmed",
                           desc, "blog.html", ld) + body + foot())
    PAGES.append(("blog.html", TODAY, "0.7", "monthly"))

def build_note_pages():
    by_slug = {p["slug"]: p for p in PUBLISHED}
    for n in NOTES:
        path = f"notes/{n['slug']}.html"
        src = by_slug[n["source"]]
        ld = [{"@context": "https://schema.org", "@type": "BlogPosting",
               "@id": f"{SITE}/{path}#post", "headline": n["title"], "name": n["title"],
               "url": f"{SITE}/{path}", "description": n["desc"],
               "datePublished": n["date"], "dateModified": n["date"],
               "author": {"@id": PERSON_ID}, "publisher": {"@id": PERSON_ID},
               "inLanguage": "en", "keywords": ", ".join(n["tags"]),
               "isPartOf": {"@id": f"{SITE}/blog.html#blog"},
               "image": f"{SITE}/images/og-image.png",
               "citation": {"@type": "ScholarlyArticle", "name": src["title"],
                            "sameAs": f"https://doi.org/{src['doi']}"},
               "mainEntityOfPage": {"@type": "WebPage", "@id": f"{SITE}/{path}"}},
              crumbs_node([("Home", ""), ("Notes", "blog.html"), (n["title"], path)])]
        tags = "".join(f'<li><span class="tag">{t}</span></li>' for t in n["tags"])
        body = f'''{rail("blog.html","../")}
<main id="main"><div class="wrap art">
  {crumbs_html([("Home","index.html"),("Notes","blog.html"),("Note",None)],"../")}
  <div class="art__grid">
    <article>
      <div class="art__h">
        <p class="art__kicker">Research note &middot; {n["reading"]} min read</p>
        <h1>{n["title"]}</h1>
        <p class="art__au">By <b>Eman Ahmed</b>, PhD candidate, {P["lab"]}, Rutgers University</p>
        <p class="art__venue"><time datetime="{n["date"]}">{n["date_h"]}</time></p>
      </div>
      <div class="prose">{n["body"]}
        <h2>Source</h2>
        <p>This note summarises <a href="../publications/{src["slug"]}.html">{src["title"]}</a>
        ({", ".join(a.split()[-1] for a in src["authors"][:3])} et al., <em>{src["journal"]}</em>,
        {src["year"]}; <a href="https://doi.org/{src["doi"]}" rel="noopener">doi:{src["doi"]}</a>).
        {PROV}</p>
        <ul class="tags">{tags}</ul>
      </div>
    </article>
    <aside class="aside">
      <div class="aside__box">
        <h2>Paper behind this note</h2>
        <dl class="dl">
          <dt>Title</dt><dd style="font-family:var(--sans);font-size:var(--t-sm)"><a href="../publications/{src["slug"]}.html">{src["title"]}</a></dd>
          <dt>Journal</dt><dd>{src["journal"]}, {src["year"]}</dd>
          <dt>DOI</dt><dd><a href="https://doi.org/{src["doi"]}" rel="noopener">{src["doi"]}</a></dd>
        </dl>
      </div>
      <div class="aside__box">
        <h2>More</h2>
        <dl class="dl">
          <dt>All notes</dt><dd><a href="../blog.html">Research notes</a></dd>
          <dt>Research</dt><dd><a href="../research.html">Research areas</a></dd>
          <dt>Contact</dt><dd><a href="../contact.html">Get in touch</a></dd>
        </dl>
      </div>
    </aside>
  </div>
</div></main>'''
        write(path, head(f'{n["title"]} | Eman Ahmed', n.get("meta") or n["desc"], path, ld, up="../", og_type="article") + body + foot("../"))
        PAGES.append((path, n["date"], "0.6", "yearly"))

# --------------------------------------------------------------------------
# CV
# --------------------------------------------------------------------------
def build_cv():
    desc = ("CV of Eman Ahmed, PhD candidate in biomedical engineering at Rutgers: education, Gormley Lab "
            "research, teaching, publications, awards and technical skills.")
    ld = [crumbs_node([("Home", ""), ("CV", "cv.html")]),
          {"@context": "https://schema.org", "@type": "WebPage", "url": f"{SITE}/cv.html",
           "name": "Curriculum Vitae | Eman Ahmed", "description": desc,
           "about": {"@id": PERSON_ID}, "dateModified": TODAY}]

    def tl(items):
        return '<div class="tl">' + "".join(
            f'''<div class="tl__item{" tl__item--on" if on else ""}">
  <p class="tl__when">{w}</p><h3 class="tl__t">{t}</h3><p class="tl__where">{p_}</p>
  <ul>{"".join(f"<li>{b}</li>" for b in bs)}</ul></div>''' for w, t, p_, bs, on in items) + "</div>"

    edu = tl([
        ("Sept 2022 &ndash; expected May 2026", "PhD, Biomedical Engineering",
         "Rutgers, The State University of New Jersey &middot; New Brunswick, NJ",
         ["Dissertation research: random copolymers for protein stabilization in water-miscible organic solvents.",
          f'Advisor: <a href="{P["advisor_url"]}" rel="noopener">{P["advisor"]}</a>, {P["lab"]}.',
          "Recipient of the Rutgers Biomedical and Health Sciences Fellowship."], True),
        ("Sept 2015 &ndash; May 2021", "BSc, Biomedical Engineering",
         "Rutgers, The State University of New Jersey &middot; New Brunswick, NJ",
         ["Graduated with highest honours; Dean's List every semester.",
          "Egypt Higher Education Initiative (HEI) Scholarship, 2015&ndash;2021.",
          "Honourable mention, Aresty Undergraduate Research Symposium, 2018."], False),
    ])
    res = tl([
        ("Sept 2023 &ndash; present", "Graduate researcher &middot; Random copolymers for protein stabilization",
         "Gormley Lab, Department of Biomedical Engineering, Rutgers University",
         ["Investigating polymer&ndash;enzyme hybrids in water-miscible organic solvents using high-throughput approaches.",
          "Developing automated, plate-based methodologies for evaluating protein solubility and retained activity.",
          "Presented findings at the Biomedical Engineering Society Annual Meeting, San Diego, October 2025."], True),
        ("Sept 2022 &ndash; Sept 2023", "Research fellow",
         "Department of Biomedical Engineering, Rutgers University",
         ["Rotated in the Gormley Lab, building skills in biomaterials formation and characterisation.",
          "Coursework in nanotechnology, biocontrol and medical implants.",
          "Assisted with grant writing and execution."], False),
        ("May 2018 &ndash; Sept 2018", "Undergraduate researcher",
         "Gormley Lab, Rutgers University",
         ["Polymer vacuum filtration and polymer solubility characterisation studies.",
          "Contributed to research on polymer-based biomaterial systems."], False),
        ("Sept 2017 &ndash; April 2018", "Undergraduate researcher",
         "Neimark Lab, Department of Chemical &amp; Biochemical Engineering, Rutgers University",
         ["Computational investigation of tension-induced rupture of lipid membranes.",
          "Presented at the Gulf Coast Undergraduate Research Symposium, Rice University, October 2018."], False),
    ])
    emp = tl([
        ("Sept 2024 &ndash; present", "Graduate assistant",
         "Department of Biomedical Engineering, Rutgers University",
         ["Supporting departmental operations and research initiatives.",
          "Assisting faculty with student mentorship; collaborating on grant projects."], True),
        ("Sept 2023 &ndash; June 2024", "Teaching assistant &middot; Introduction to Biomedical Engineering",
         "Rutgers School of Engineering",
         ["Led laboratory sessions and supported course instruction for undergraduates.",
          "Held weekly office hours; assessed assignments and gave written feedback."], False),
    ])
    pubs_li = "".join(f'<li><a href="publications/{p["slug"]}.html">{p["title"]}</a>. '
                      f'{", ".join(a.split()[-1]+" "+"".join(x[0] for x in a.split()[:-1]) for a in p["authors"])}. '
                      f'<em>{p["journal"]}</em> {p.get("volume","")}({p.get("issue","")}), {p.get("pages","")} ({p["year"]}). '
                      f'<a class="data" href="https://doi.org/{p["doi"]}" rel="noopener">doi:{p["doi"]}</a></li>'
                      for p in PUBLISHED)
    awards = [("Rutgers Biomedical and Health Sciences Fellowship", "2022&ndash;2023",
               "$33,999 stipend with full tuition remission."),
              ("Egypt Higher Education Initiative (HEI) Scholarship", "2015&ndash;2021",
               "Full undergraduate funding."),
              ("Honourable mention, Aresty Undergraduate Research Symposium", "2018",
               "For tension-induced rupture of lipid membranes."),
              ("Highest honours and Dean's List", "2015&ndash;2021",
               "Dean's List in every semester of the undergraduate degree.")]
    aw = "".join(f'<div><dt>{t}</dt><dd><p>{d}</p><p class="data" style="font-size:var(--t-xs);color:var(--ink-3);margin:0">{w}</p></dd></div>' for t, w, d in awards)
    meth = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in METHODS)
    serv = [("Biomedical Engineering Student Society", "2022 &ndash; present", "General body member."),
            ("Biomedical Engineering Society", "2018&ndash;2019", "Engineering Governing Council representative."),
            ("Research mentorship", "Ongoing", "Mentoring undergraduate researchers in the Gormley Lab in polymer synthesis, high-throughput screening and data analysis.")]
    sv = "".join(f'<div><dt>{t}</dt><dd><p>{d}</p><p class="data" style="font-size:var(--t-xs);color:var(--ink-3);margin:0">{w}</p></dd></div>' for t, w, d in serv)

    body = f'''{rail("cv.html")}
<main id="main">
<div class="wrap art art--lead">
  {crumbs_html([("Home","index.html"),("CV",None)])}
  <div class="art__h">
    {byline()}
    <h1>Curriculum vitae</h1>
    <p class="art__au">Eman Ahmed &middot; PhD candidate, Department of Biomedical Engineering,
    Rutgers, The State University of New Jersey</p>
    <p class="art__venue">{P["city"]}, {P["region"]}, USA &middot; <a href="mailto:{P["email"]}">{P["email"]}</a></p>
    <p style="margin:var(--s5) 0 0"><a class="btn btn--solid" href="assets/emancv.pdf" download>{ico("download")}Download PDF</a></p>
  </div>
</div>

<section class="sec sec--first sec--tight"><div class="wrap">
  <h2 style="font-size:var(--t-xl);margin-bottom:var(--s6)">Education</h2>{edu}
</div></section>

<section class="sec sec--sunk"><div class="wrap">
  <h2 style="font-size:var(--t-xl);margin-bottom:var(--s6)">Research experience</h2>{res}
</div></section>

<section class="sec"><div class="wrap">
  <h2 style="font-size:var(--t-xl);margin-bottom:var(--s6)">Teaching and employment</h2>{emp}
</div></section>

<section class="sec sec--sunk"><div class="wrap">
  <h2 style="font-size:var(--t-xl);margin-bottom:var(--s5)">Peer-reviewed publications</h2>
  <ol class="prose" style="max-width:none;color:var(--ink-2)">{pubs_li}</ol>
  <p style="margin-top:var(--s5)"><a class="btn btn--line" href="publications.html">Full publication records</a></p>
</div></section>

<section class="sec"><div class="wrap">
  <h2 style="font-size:var(--t-xl);margin-bottom:var(--s5)">Honours and awards</h2>
  <dl class="facts">{aw}</dl>
</div></section>

<section class="sec sec--sunk"><div class="wrap">
  <h2 style="font-size:var(--t-xl);margin-bottom:var(--s5)">Technical skills</h2>
  <dl class="facts">{meth}</dl>
</div></section>

<section class="sec"><div class="wrap">
  <h2 style="font-size:var(--t-xl);margin-bottom:var(--s5)">Service and mentorship</h2>
  <dl class="facts">{sv}</dl>
</div></section>
</main>'''
    write("cv.html", head("CV | Eman Ahmed, PhD Candidate, Rutgers BME",
                         desc, "cv.html", ld) + body + foot())
    PAGES.append(("cv.html", TODAY, "0.8", "monthly"))

# --------------------------------------------------------------------------
# Teaching
# --------------------------------------------------------------------------
def build_teaching():
    desc = ("Teaching assistant for Introduction to Biomedical Engineering at Rutgers, graduate assistant, "
            "and undergraduate research mentor in the Gormley Lab.")
    ld = [crumbs_node([("Home", ""), ("Teaching", "teaching.html")]),
          {"@context": "https://schema.org", "@type": "WebPage", "url": f"{SITE}/teaching.html",
           "name": "Teaching | Eman Ahmed", "description": desc,
           "about": {"@id": PERSON_ID}, "dateModified": TODAY}]
    body = f'''{rail("teaching.html")}
<main id="main">
<div class="wrap art art--lead">
  {crumbs_html([("Home","index.html"),("Teaching",None)])}
  <div class="art__h">
    <h1>Teaching and mentorship</h1>
    <p class="hero__lede" style="margin-bottom:0">Most of what I teach is procedural: how to run an assay so
    the numbers mean something, how to tell a real signal from a pipetting error, and how to write down what
    you did so someone else can repeat it.</p>
  </div>
</div>

<section class="sec sec--first sec--tight"><div class="wrap">
  <div class="sec__head sec__head--split">
    <h2>How I teach</h2>
    <p>Three things I try to get across, in laboratories and in one-to-one mentorship.</p>
  </div>
  <dl class="facts">
    <div><dt>A result you cannot reproduce is not a result</dt>
      <dd><p>Working in high-throughput research makes this unavoidable: with ninety-six wells running at once,
      sloppy technique does not produce one bad number, it produces a bad dataset. I teach protocol discipline
      first, because everything downstream depends on it.</p></dd></div>
    <div><dt>Negative results are data</dt>
      <dd><p>Students arrive expecting experiments to work and treat failures as wasted time. In screening
      work the conditions that fail define the boundary of the useful region, and they are worth recording with
      the same care as the ones that succeed.</p></dd></div>
    <div><dt>Start from the measurement</dt>
      <dd><p>Before running anything, I ask what number will come out and what it would mean if it came out
      differently. It is a faster route to understanding an assay than working forward from the protocol.</p></dd></div>
  </dl>
</div></section>

<section class="sec sec--sunk"><div class="wrap">
  <h2 style="font-size:var(--t-xl);margin-bottom:var(--s6)">Positions</h2>
  <div class="tl">
    <div class="tl__item tl__item--on">
      <p class="tl__when">Sept 2024 &ndash; present</p>
      <h3 class="tl__t">Graduate assistant</h3>
      <p class="tl__where">Department of Biomedical Engineering, Rutgers University</p>
      <ul><li>Supporting departmental operations and research initiatives.</li>
      <li>Assisting faculty with student mentorship.</li>
      <li>Collaborating on grant projects.</li></ul>
    </div>
    <div class="tl__item">
      <p class="tl__when">Sept 2023 &ndash; June 2024</p>
      <h3 class="tl__t">Teaching assistant &middot; Introduction to Biomedical Engineering</h3>
      <p class="tl__where">Rutgers School of Engineering &middot; undergraduate course</p>
      <ul><li>Led laboratory sessions and supported course instruction.</li>
      <li>Weekly office hours for students working through foundational material.</li>
      <li>Assessed assignments and provided written feedback.</li>
      <li>Course topics: biomechanics, biomaterials, medical devices, tissue engineering, biomedical imaging, bioethics.</li></ul>
    </div>
    <div class="tl__item">
      <p class="tl__when">Ongoing</p>
      <h3 class="tl__t">Undergraduate research mentorship</h3>
      <p class="tl__where">Gormley Lab, Rutgers University</p>
      <ul><li>Mentoring undergraduate researchers in polymer synthesis technique.</li>
      <li>Training on high-throughput screening workflows and liquid handling.</li>
      <li>Supervising data analysis for biomaterials experiments.</li></ul>
    </div>
  </div>
</div></section>

<section class="sec"><div class="wrap"><div class="call">
  <h2>Prospective students</h2>
  <p>If you are a Rutgers undergraduate interested in polymer chemistry, laboratory automation or applying
  machine learning to experimental data, get in touch &mdash; and say what you have already tried, not just
  what you are interested in.</p>
  <div class="call__acts"><a class="btn btn--solid" href="contact.html">{ico("mail")}Email me</a></div>
</div></div></section>
</main>'''
    write("teaching.html", head("Teaching &amp; Mentorship | Eman Ahmed, Rutgers BME",
                               desc, "teaching.html", ld) + body + foot())
    PAGES.append(("teaching.html", TODAY, "0.6", "yearly"))

# --------------------------------------------------------------------------
# Lab & collaborators (kept at collaborators.html -- the URL is indexed)
# --------------------------------------------------------------------------
def build_lab():
    desc = ("Eman Ahmed's group and co-authors: the Gormley Lab at Rutgers Biomedical Engineering, the "
            "Neimark Lab, and beamline collaborators at NSLS-II, Brookhaven.")
    ld = [crumbs_node([("Home", ""), ("Lab", "collaborators.html")]),
          {"@context": "https://schema.org", "@type": "WebPage", "url": f"{SITE}/collaborators.html",
           "name": "Lab and collaborators | Eman Ahmed", "description": desc,
           "about": {"@id": PERSON_ID}, "dateModified": TODAY}]
    coauthors = {}
    for p in PUBLISHED:
        for a in p["authors"]:
            if a == P["name"]: continue
            coauthors.setdefault(a, []).append(p)
    rows = "".join(
        f'''<div><dt>{a}</dt><dd><p>Co-author on {len(ps)} paper{"s" if len(ps)>1 else ""}: '''
        + ", ".join(f'<a href="publications/{x["slug"]}.html">{x["journal"]}</a>' for x in ps)
        + ".</p></dd></div>"
        for a, ps in sorted(coauthors.items(), key=lambda kv: (-len(kv[1]), kv[0])))

    body = f'''{rail("collaborators.html")}
<main id="main">
<div class="wrap art art--lead">
  {crumbs_html([("Home","index.html"),("Lab",None)])}
  <div class="art__h">
    <h1>Lab and collaborators</h1>
    <p class="hero__lede" style="margin-bottom:0">This work is done in the Gormley Lab at Rutgers, with
    synchrotron measurements collected at Brookhaven National Laboratory and analysis built on tools the
    wider SAXS community maintains.</p>
  </div>
</div>

<section class="sec sec--first sec--tight"><div class="wrap">
  <h2 style="font-size:var(--t-xl);margin-bottom:var(--s5)">Current group</h2>
  <dl class="facts">
    <div><dt>Gormley Lab</dt><dd>
      <p>Principal investigator <a href="{P["advisor_url"]}" rel="noopener">{P["advisor"]}</a>, Associate
      Professor, {P["dept"]}, Rutgers University. The lab works on polymer-based biomaterials, high-throughput
      polymer synthesis and screening, polymer&ndash;protein conjugates, enzyme stabilization with synthetic
      polymers, and machine learning for biomaterial design.</p>
      <p style="margin-bottom:0"><a href="{P["lab_url"]}" rel="noopener">gormleylab.com</a> &middot;
      <a href="{P["dept_url"]}" rel="noopener">Rutgers BME</a></p></dd></div>
    <div><dt>Rutgers Biomedical and Health Sciences</dt><dd>
      <p style="margin-bottom:0">RBHS Fellowship recipient, 2022&ndash;2023, supporting the first year of
      doctoral research.</p></dd></div>
    <div><dt>NSLS-II, Brookhaven National Laboratory</dt><dd>
      <p style="margin-bottom:0">Synchrotron small-angle X-ray scattering measurements underpinning the
      <a href="publications/saxs-assistant-automated-saxs-analysis.html">SAXS Assistant</a> work, co-authored
      with beamline scientist James Byrnes.</p></dd></div>
  </dl>
</div></section>

<section class="sec sec--sunk"><div class="wrap">
  <div class="sec__head sec__head--split">
    <h2>Co-authors</h2>
    <p>Everyone I have published with, and where.</p>
  </div>
  <dl class="facts">{rows}</dl>
</div></section>

<section class="sec"><div class="wrap">
  <h2 style="font-size:var(--t-xl);margin-bottom:var(--s5)">Earlier affiliation</h2>
  <dl class="facts">
    <div><dt>Neimark Lab</dt><dd>
      <p>Alexander Neimark, Distinguished Professor, Department of Chemical &amp; Biochemical Engineering,
      Rutgers University. As an undergraduate I worked here on the computational study of tension-induced
      rupture in lipid membranes, presented at Rice University and awarded an honourable mention at the
      Aresty Symposium.</p></dd></div>
  </dl>
</div></section>

<section class="sec sec--sunk"><div class="wrap"><div class="call">
  <h2>Open to collaboration</h2>
  <p>Particularly interested in talking to groups working on high-throughput polymer synthesis, enzyme
  stabilization, SAXS at scale, or machine learning applied to experimental materials data.</p>
  <div class="call__acts"><a class="btn btn--solid" href="contact.html">{ico("mail")}Get in touch</a></div>
</div></div></section>
</main>'''
    write("collaborators.html", head("Lab &amp; Collaborators | Gormley Lab, Rutgers | Eman Ahmed",
                                     desc, "collaborators.html", ld) + body + foot())
    PAGES.append(("collaborators.html", TODAY, "0.5", "yearly"))

# --------------------------------------------------------------------------
# Contact
# --------------------------------------------------------------------------
def build_contact():
    desc = ("Contact Eman Ahmed, PhD candidate at Rutgers (Gormley Lab), about collaboration in "
            "high-throughput polymer chemistry, SAXS analysis or ML for biomaterials.")
    ld = [crumbs_node([("Home", ""), ("Contact", "contact.html")]),
          {"@context": "https://schema.org", "@type": "ContactPage", "url": f"{SITE}/contact.html",
           "name": "Contact | Eman Ahmed", "description": desc,
           "about": {"@id": PERSON_ID}, "dateModified": TODAY}]
    links = [("mail", "Email", P["email"], f"mailto:{P['email']}"),
             ("cap", "Google Scholar", "Publications and citations", P["scholar"]),
             ("in", "LinkedIn", "Professional profile", P["linkedin"]),
             ("code", "Gormley Lab", "gormleylab.com", P["lab_url"]),
             ("doc", "Curriculum vitae", "PDF download", "assets/emancv.pdf")]
    ll = "".join(f'''<li><a href="{u}"{' rel="noopener"' if u.startswith("http") else ""}>
      {ico(i)}<span class="links__k">{k}</span><span class="links__v">{v}</span></a></li>''' for i, k, v, u in links)
    subj = [("Research collaboration", "Collaboration%20enquiry"),
            ("A question about a paper or method", "Question%20about%20a%20paper"),
            ("Speaking or seminar invitation", "Speaking%20invitation"),
            ("Undergraduate research in the Gormley Lab", "Undergraduate%20research%20enquiry")]
    sl = "".join(f'<li><a href="mailto:{P["email"]}?subject={q}">{ico("mail")}'
                 f'<span class="links__k">{t}</span></a></li>' for t, q in subj)

    body = f'''{rail("contact.html")}
<main id="main">
<div class="wrap art">
  {crumbs_html([("Home","index.html"),("Contact",None)])}
  <div class="art__grid">
    <div>
      <div class="art__h">
        <h1>Get in touch</h1>
        <p class="hero__lede" style="margin-bottom:0">Email is the reliable route. I read everything and
        normally reply within a few working days &mdash; if a message needs data or a figure I do not have to
        hand, it may take longer.</p>
      </div>
      <h2 style="font-size:var(--t-lg);margin-bottom:var(--s4)">Start an email</h2>
      <p style="color:var(--ink-2)">These open a draft with the subject filled in.</p>
      <ul class="links">{sl}</ul>

      <h2 style="font-size:var(--t-lg);margin:var(--s8) 0 var(--s4)">What helps</h2>
      <ul class="prose" style="color:var(--ink-2)">
        <li>If you are asking about a method, say which paper and which step &mdash; it saves a round trip.</li>
        <li>If you are proposing a collaboration, a sentence on what you would want from this side is more
        useful than a general introduction.</li>
        <li>If you are a student looking for research experience, tell me what you have already tried.</li>
      </ul>
    </div>
    <aside class="aside">
      {byline()}
      <div class="aside__box">
        <h2>Where to find me</h2>
        <dl class="dl">
          <dt>Email</dt><dd><a href="mailto:{P["email"]}">{P["email"]}</a></dd>
          <dt>Department</dt><dd style="font-family:var(--sans);font-size:var(--t-sm)">{P["dept"]}<br>Rutgers, The State University of New Jersey<br>{P["city"]}, {P["region"]}, USA</dd>
          <dt>Lab</dt><dd><a href="{P["lab_url"]}" rel="noopener">Gormley Lab</a></dd>
          <dt>Scholar</dt><dd><a href="{P["scholar"]}" rel="noopener">Google Scholar</a></dd>
          <dt>LinkedIn</dt><dd><a href="{P["linkedin"]}" rel="noopener">eman-ahmed</a></dd>
        </dl>
      </div>
    </aside>
  </div>
</div>

<section class="sec"><div class="wrap">
  <h2 style="font-size:var(--t-xl);margin-bottom:var(--s5)">Elsewhere</h2>
  <ul class="links">{ll}</ul>
</div></section>
</main>'''
    write("contact.html", head("Contact | Eman Ahmed, Rutgers Biomedical Engineering",
                               desc, "contact.html", ld) + body + foot())
    PAGES.append(("contact.html", TODAY, "0.7", "yearly"))

# --------------------------------------------------------------------------
# 404
# --------------------------------------------------------------------------
def build_404():
    ld = [{"@context": "https://schema.org", "@type": "WebPage", "name": "Page not found"}]
    body = f'''{rail("")}
<main id="main"><div class="wrap art">
  <div class="art__h">
    <p class="art__kicker">404</p>
    <h1>That page isn't here</h1>
    <p class="hero__lede">The link may be out of date. Everything on the site is reachable from these:</p>
  </div>
  <ul class="links">
    <li><a href="/index.html">{ico("pin")}<span class="links__k">Home</span></a></li>
    <li><a href="/research.html">{ico("model")}<span class="links__k">Research</span></a></li>
    <li><a href="/publications.html">{ico("doc")}<span class="links__k">Publications</span></a></li>
    <li><a href="/blog.html">{ico("code")}<span class="links__k">Research notes</span></a></li>
    <li><a href="/cv.html">{ico("cap")}<span class="links__k">CV</span></a></li>
    <li><a href="/contact.html">{ico("mail")}<span class="links__k">Contact</span></a></li>
  </ul>
</div></main>'''
    h = head("Page not found | Eman Ahmed", "This page does not exist on emanahmed.org.", "404.html", ld)
    h = h.replace("</head>", '<meta name="robots" content="noindex">\n</head>')
    write("404.html", h + body + foot())

# --------------------------------------------------------------------------
# robots.txt + sitemap.xml
# --------------------------------------------------------------------------
def build_robots():
    write("robots.txt", f"""# emanahmed.org -- academic research site, open to crawling.

User-agent: *
Allow: /
Disallow: /_src/

# Assistants and answer engines are welcome to read and cite this site.
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: CCBot
Allow: /

Sitemap: {SITE}/sitemap.xml
""")

def build_sitemap():
    seen, urls = set(), []
    for loc, mod, pri, freq in PAGES:
        if loc in seen: continue
        seen.add(loc)
        urls.append(f"""  <url>
    <loc>{SITE}/{loc}</loc>
    <lastmod>{mod}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{pri}</priority>
  </url>""")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "\n".join(urls) + "\n</urlset>\n")

# --------------------------------------------------------------------------
def main():
    build_home(); build_research(); build_publications(); build_pub_pages()
    build_notes_index(); build_note_pages(); build_cv(); build_teaching()
    build_lab(); build_contact(); build_404()
    build_robots(); build_sitemap()
    print(f"built {len(PAGES)} indexable pages + 404, robots.txt, sitemap.xml")
    for loc, *_ in PAGES: print("  /" + loc)

if __name__ == "__main__":
    main()
