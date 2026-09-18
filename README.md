# emanahmed.org

Research site for Eman Ahmed, PhD candidate in biomedical engineering at Rutgers
University (Gormley Lab). Static HTML, no build dependencies beyond Python 3.

## Editing

**Do not edit the generated `.html` files** — they are overwritten on every build.
Edit the source and rebuild:

| What you want to change | File |
|---|---|
| Name, affiliation, email, links, Scholar metrics | `_src/data.py` → `PROFILE` |
| Publications (abstracts, DOIs, citation counts) | `_src/data.py` → `PUBLICATIONS` |
| Research areas, methods list | `_src/data.py` → `AREAS`, `METHODS` |
| Research notes (articles) | `_src/notes.py` |
| Page structure, SEO tags, structured data | `_src/build.py` |
| Visual design | `css/styles.css` (handwritten, not generated) |
| Behaviour (theme, menu, copy buttons) | `js/main.js` (handwritten) |

Then:

```sh
python3 _src/build.py
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

## Still to do

- Register an ORCID iD and add it to `PROFILE`; it should then be added to the
  `sameAs` list in `person_node()` in `_src/build.py`.
- Replace `images/eman-us.jpeg` with a professional headshot when one exists.
- Re-generate `images/og-image.png` from `images/og-image.svg` if the tagline changes.
