# -*- coding: utf-8 -*-
"""
Figure primitives -> inline HTML.

Every figure on the site is a table of values published in one of the papers,
rendered at build time so it is readable by crawlers and answer engines,
visible with JS disabled, and free of layout shift.

There are deliberately no chart renderers here. The site previously drew plots
from simulated scattering and from illustrative arithmetic, which looked like
evidence without being any. If a figure is worth showing, its numbers came out
of a paper; if the numbers came out of a paper, a table shows them without
implying a measurement that was never made.

Every figure carries a provenance badge saying where its numbers came from.
"""
import html

PROV = {
    "measured":  ("Measured", "Values measured in the published work."),
    "reported":  ("Reported", "Values exactly as published; see the source note."),
    "schematic": ("Schematic", "A description of the method, not reported data."),
}


def esc(s):
    return html.escape(str(s), quote=True)


def figure(fid, title, sub, svg, table, prov, source=None, legend=None, note=None):
    """A titled block of published values.

    `svg` is retained for call compatibility and is rendered above the table
    when a caller passes one; every current figure passes "".
    """
    kind, default = PROV[prov]
    plot_html = f'<div class="fig__plot">{svg}</div>' if svg else ""
    legend_html = f'<div class="fig__legend">{legend}</div>' if legend else ""
    note_html = f'<p class="fig__note">{note}</p>' if note else ""
    # With no plot there is nothing for the table to be the fallback *for*, so
    # it is shown open rather than hidden behind a disclosure.
    data_html = (f'<details class="fig__data" open><summary>The numbers</summary>{table}</details>'
                 if not svg else
                 f'<details class="fig__data"><summary>Show the numbers</summary>{table}</details>')
    return f'''<figure class="fig" id="{fid}">
  <figcaption class="fig__head">
    <h3 class="fig__title">{title}</h3>
    <p class="fig__sub">{sub}</p>
  </figcaption>
  {plot_html}
  {legend_html}
  {note_html}
  {data_html}
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
