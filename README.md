# emanahmed.org

Research site for Eman Ahmed, PhD candidate in biomedical engineering at Rutgers
University (Gormley Lab). Static HTML, no build dependencies beyond Python 3.

## Editing

**Do not edit the generated `.html` files** — they are overwritten on every build.
Edit the source and rebuild:

| What you want to change | File |
|---|---|
| Name, affiliation, email, links, Scholar metrics | `_src/data.py` → `PROFILE` |
| ORCID, GitHub, ResearchGate and other profiles | `_src/data.py` → `PROFILE` (empty = not rendered) |
| Publications (abstracts, DOIs, citation counts) | `_src/data.py` → `PUBLICATIONS` |
| Research areas, methods list | `_src/data.py` → `AREAS`, `METHODS` |
| Research notes (articles) | `_src/notes.py` |
| Deep research pages and their figures | `_src/pages_research.py` |
| Figure and table shell | `_src/viz.py` |
| Page structure, SEO tags, structured data | `_src/build.py` |
| Visual design | `css/styles.css` (handwritten, not generated) |
| Behaviour (theme, menu, copy buttons) | `js/main.js` (handwritten) |

Then:

```sh
python3 _src/build.py
```

Check that no page scrolls sideways (needs Chrome installed):

```sh
node _src/overflow-test.mjs 320      # every page must fit a 320px viewport
```

Preview locally:

```sh
python3 -m http.server 8777    # then open http://localhost:8777
```

## Keeping it accurate

- **Citation metrics** live in `PROFILE["metrics"]`. When you update `citations`,
  `hindex` or `papers`, move `asof` to the same date — it is displayed next to the
  numbers and in the footer.
- **Per-paper citation counts** live on each entry in `PUBLICATIONS`.
- When a paper moves from `"status": "inprep"` to published, fill in `journal`,
  `volume`, `issue`, `pages`, `date`, `doi`, `abstract`, `slug`, `short` and `meta`.
  A `slug` is what gives it a dedicated page at `/publications/<slug>.html`.
- Every bibliographic field should come from the publisher of record or PubMed
  Central, not from memory. The Google Scholar–readable `citation_*` meta tags on
  each publication page are generated from these fields.

## Figures

Every figure on the site is a **table of values published in one of the three
papers**, rendered into the HTML at build time. Two rules:

1. **Nothing is simulated, illustrative or reconstructed.** If a number appears,
   it was printed in the paper it is attributed to. The site used to draw
   scattering curves computed from a made-up sphere, a log dot plot mixing
   library sizes with hypothetical combinatorial spaces, and an animated
   "pipeline" hero. None of that was data, and all of it is gone.
2. **A provenance badge.** `Reported` (published value) or `Schematic` (a
   description of a method, used only for the in-preparation doctoral
   workflow). Never publish a figure without one.

There are deliberately no chart renderers in `_src/viz.py`. If a future figure
genuinely needs a plot, it needs real measured data behind it first.

## SEO / discovery notes

- `robots.txt` allows all major search crawlers and explicitly allows assistant
  crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended and others).
- `sitemap.xml` is regenerated on every build; `lastmod` uses the build date.
- Each publication page carries Highwire Press `citation_*` meta tags, which is
  what Google Scholar indexes, plus `ScholarlyArticle` JSON-LD.
- `research.html` carries `FAQPage` structured data.
- Page URLs deliberately keep their `.html` extensions so that already-indexed
  URLs keep working. Do not rename them without setting up redirects.
- `.nojekyll` is present so GitHub Pages serves the files exactly as generated.
- No page may scroll horizontally at 320px — `node _src/overflow-test.mjs` measures
  this in a real browser. Two things break it in practice: a `<pre>` or long token
  that cannot wrap, and a grid item keeping its default `min-width: auto`, which
  lets one unbreakable child (a DOI is ~290px) size the whole column. DOIs and
  other copyable values carry `class="data"`, which allows them to break. Wide
  tables scroll inside `.fig__tablewrap`.
- Known, unfixed: below ~300px the header rail needs 297px for the wordmark, the
  "Rutgers BME" sub-label and the two buttons, so it overflows on a 280px screen
  (Galaxy Fold cover display). Hiding the sub-label under 320px would fix it.
- Profile identifiers in `PROFILE` (`orcid`, `github`, `researchgate`, `openalex`,
  `bluesky`) drive `sameAs`, the `Person` `identifier`, the footer, the contact
  page and the `rel="me"` links from one list. Leave one empty and it renders
  nowhere — never put a placeholder or a guessed ID in there.
- Off-site authority — getting the Gormley Lab and Rutgers BME pages to link
  here — is the remaining lever, and it is not a markup problem. The plan, with
  draft emails and a profile checklist, is in `_src/authority-kit.md`.

## Still to do

- Register an ORCID iD and put the bare ID in `PROFILE["orcid"]`. Nothing else is
  needed — the schema, footer and contact page pick it up on the next build.
  See `_src/authority-kit.md` for why this one is worth doing first.
- Replace `images/eman-us.jpeg` with a professional headshot when one exists.
- `images/og-image.jpg` is generated from `images/og-image.svg` (JPEG, not PNG — the
  scattering gradients quadruple in size as PNG). Regenerate it if the tagline changes.
