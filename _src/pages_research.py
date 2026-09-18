# -*- coding: utf-8 -*-
"""Deep research pages. Each figure's numbers trace to the cited paper."""
import viz
from viz import figure, table, legend_items, dotplot_log, barh, dotmatrix, linechart

# =========================================================================
# 1. Machine learning for biomaterials  (Tissue Engineering Part A, 2024)
# =========================================================================

DATASETS = [
    ("Scaffold study", 182, "13 polymers, 182 scaffolds tested"),
    ("Titanium nanotube analysis", 272, "272 labelled samples, 30 publications"),
    ("Kohn polyacrylate library", 112, "112 distinct degradable polymers"),
    ("Lipid nanoparticle screen", 1080, "1,080-LNP formulation library"),
    ("Poly(β-amino ester) library", 2500, "~2,500 degradable PAEs for gene delivery"),
    ("Drug–excipient space", 2_100_000, "2.1 million possible pairings"),
]

ALGOS = ["Random forest", "Support vector machine", "Neural network",
         "Gradient boosting", "Gaussian regression", "Hidden Markov model", "Active learning"]
DOMAINS = ["Tissue engineering", "Gene delivery", "Drug delivery",
           "Protein stabilization", "Antifouling materials", "Data mining"]
USE = {
    (0, 0): 1, (0, 5): 1, (0, 4): 1,
    (1, 0): 1, (1, 4): 1,
    (2, 2): 1, (2, 1): 1,
    (3, 1): 1,
    (4, 0): 1, (4, 2): 1,
    (5, 3): 1,
    (6, 3): 1, (6, 2): 1,
}

DESCRIPTORS = [
    ("Structural", "Fibre diameter, pore diameter, porosity, pore size"),
    ("Mechanical", "Young's modulus, compressive strength"),
    ("Thermal", "Glass transition temperature (Tₘ)"),
    ("Surface", "Contact angle, roughness, hydrophobicity, wettability"),
    ("Compositional", "Monomer ratios, pendant groups, backbone modifications"),
    ("Molecular", "Cheminformatic descriptors (e.g. PaDEL) for lipids and small molecules"),
]


def ml_figures():
    rows = sorted(DATASETS, key=lambda r: r[1])
    f1 = figure(
        "fig-datasets",
        "How big is a high-throughput biomaterials dataset?",
        "Study sizes cited in the review, on a logarithmic axis. Four orders of magnitude "
        "separate a careful polymer library from the combinatorial space it samples.",
        dotplot_log([(r[0], r[1], r[2]) for r in rows],
                    xlabel="Number of distinct formulations or samples (log scale)",
                    title="Dataset sizes in high-throughput biomaterials studies",
                    desc="Dot plot on a log axis. Scaffold study 182, titanium nanotube analysis 272, "
                         "Kohn polyacrylate library 112, lipid nanoparticle screen 1080, "
                         "poly(beta-amino ester) library 2500, drug-excipient space 2.1 million.",
                    highlight=len(rows) - 1),
        table(["Study", "Size", "Description"],
              [(r[0], viz.fmt(r[1]), r[2]) for r in rows]),
        "reported",
        "Study sizes as cited in Ahmed <em>et al.</em>, <em>Tissue Engineering Part A</em> 30(19–20), "
        "662–680 (2024). A dot plot is used rather than bars because a bar length on a log axis "
        "misrepresents ratio.",
        note="The gap is the argument. Experimental libraries reach a few thousand members; the spaces "
             "they are drawn from run to millions. Nothing exhaustive is possible here, so the question "
             "becomes which few thousand to make, which is a modelling problem, not a pipetting one.")

    f2 = figure(
        "fig-algorithms",
        "Which methods are being used where",
        "The pairings of algorithm and application area discussed in the review.",
        dotmatrix(DOMAINS, ALGOS, USE,
                  title="Machine learning methods by biomaterials application area",
                  desc="Dot matrix pairing seven algorithms with six application areas."),
        table(["Method", "Application areas discussed"],
              [(a, ", ".join(DOMAINS[j] for j in range(len(DOMAINS)) if USE.get((i, j))) or "None")
               for i, a in enumerate(ALGOS)]),
        "reported",
        "Pairings as discussed in the review. A filled dot means the review covers that method in that "
        "area; an empty position is not a claim that the combination is unused.")

    f3 = figure(
        "fig-descriptors",
        "What a polymer looks like to a model",
        "A model cannot read a structure. It reads whatever numbers you chose to describe it, and "
        "that choice bounds what the model can possibly learn.",
        "", table(["Descriptor family", "Examples"], DESCRIPTORS), "reported",
        "Descriptor families as surveyed in the review.")
    return f1, f2, f3


# =========================================================================
# 2. Automated photo-ATRP  (ACS Polymers Au, 2026)
# =========================================================================

MONOMERS = [
    ("2-Hydroxyethyl acrylate", "HEA", "acrylate"),
    ("Methyl acrylate", "MA", "acrylate"),
    ("2-Hydroxypropyl acrylate", "HPA", "acrylate"),
    ("Methyl methacrylate", "MMA", "methacrylate"),
]

DISPERSITY = [
    ("Acrylates, optimised", 1.15, "--v1", "best reported condition"),
    ("Acrylates, well-controlled", 1.30, "--v1", "reported upper bound, Đ < 1.3"),
    ("MMA with PMDETA + BPN", 1.26, "--v2", "at target specifications"),
]

CONDITIONS = [
    ("Plate format", "96-well polypropylene"),
    ("Reaction volume", "200 µL"),
    ("Oxygen headspace", "100 µL"),
    ("Solvent", "DMSO"),
    ("Metal catalyst", "CuBr₂"),
    ("Photocatalysts", "ZnTPP, Eosin Y"),
    ("Primary light source", "560 nm red LED, 5 mW cm⁻²"),
    ("Validation light source", "515 nm green LED, 2.61 mW cm⁻²"),
    ("Ligands screened", "Me₆TREN, PMDETA"),
    ("Initiators screened", "MBiB, BPN"),
]

REAGENT_COLS = ["Me₆TREN + MBiB", "PMDETA + BPN"]
REAGENT_ROWS = [m[1] for m in MONOMERS]
REAGENT_USE = {(0, 0): 1, (1, 0): 1, (2, 0): 1, (3, 1): 1}


def atrp_figures():
    f1 = figure(
        "fig-conditions",
        "The reaction, as it actually runs",
        "Published conditions for the automated photo-ATRP platform.",
        "", table(["Parameter", "Value"], CONDITIONS), "reported",
        "Conditions as published in Ramirez, Ahmed <em>et al.</em>, <em>ACS Polymers Au</em> 6(1), "
        "181–193 (2026).",
        note="Two of these numbers carry the whole idea. A 200 µL reaction sitting under 100 µL of "
             "air is a reaction that has given up on being oxygen-free. The catalytic system scavenges "
             "the oxygen instead. That is what lets the plate stay in open labware and be handled by a robot.")

    f2 = figure(
        "fig-reagents",
        "Different monomers want different reagents",
        "The reagent pairing that gave good control, by monomer class. The same combination does not "
        "work across the board, which is the finding.",
        dotmatrix(REAGENT_COLS, REAGENT_ROWS, REAGENT_USE,
                  title="Best-performing ligand and initiator pairing by monomer",
                  desc="Acrylates HEA, MA and HPA pair with Me6TREN and MBiB; "
                       "methyl methacrylate pairs with PMDETA and BPN."),
        table(["Monomer", "Class", "Reported best pairing"],
              [(f"{n} ({a})", c,
                REAGENT_COLS[0] if c == "acrylate" else REAGENT_COLS[1])
               for n, a, c in MONOMERS]),
        "reported",
        "As reported in the paper: Me₆TREN consistently produced high dispersity with MMA, while "
        "PMDETA and BPN emerged as the most suitable reagents for high-throughput MMA synthesis.",
        note="Methyl methacrylate propagates more slowly than the acrylates, so the activation–"
             "deactivation balance that ATRP depends on has to be retuned. There is no reliable way to "
             "reason to the answer from first principles, which is exactly why screening it is worth the "
             "instrument time.")

    f3 = figure(
        "fig-dispersity",
        "Dispersity, reported",
        "Đ = Mᵥ/Mₙ. A perfectly uniform chain population would be 1.00; below about 1.3 is "
        "normally taken as well-controlled.",
        barh(DISPERSITY, xlabel="Dispersity (Đ)", xdom=(1.0, 1.4),
             ref={"x": 1.0, "label": "Đ = 1.00, perfectly uniform"},
             xfmt=lambda v: f"{v:.2f}",
             title="Reported dispersity values",
             desc="Acrylates optimised 1.15, acrylates well-controlled upper bound 1.30, "
                  "MMA with PMDETA and BPN 1.26."),
        table(["Condition", "Đ", "Note"], [(r[0], f"{r[1]:.2f}", r[3]) for r in DISPERSITY]),
        "reported",
        "Only values stated in the paper are plotted. This is not the full screen. For the complete "
        "dataset see the publication.",
        legend=legend_items([("--v1", "Acrylates"), ("--v2", "Methacrylate (MMA)")]))
    return f1, f2, f3


# =========================================================================
# 3. SAXS + machine learning  (Biophysical Journal, 2025)
# =========================================================================

import math, sas
from viz import tolerance_strip, mlp_diagram, detector

SHAPES = [("globular", "--v1"), ("elongated", "--v2"), ("two-domain", "--v3")]

MODEL = [
    ("Training profiles", "1,940", "experimental files from the SASBDB"),
    ("Architecture", "4 × 32", "hidden layers × units, ReLU"),
    ("Test R²", "0.90", "on held-out data"),
    ("Mean absolute error", "11.7 Å", "on maximum particle dimension"),
]

HYPER = [
    ("Model", "Multilayer perceptron regressor"),
    ("Hidden layers", "4, each of 32 units"),
    ("Activation", "ReLU"),
    ("Solver", "Adam"),
    ("Alpha (L2 penalty)", "1 × 10⁻³"),
    ("Maximum iterations", "1,000"),
    ("Random state", "42"),
    ("Training set", "1,940 SASBDB profiles"),
    ("Analysis q-range", "0.005–0.25 Å⁻¹"),
    ("Collection q-range", "0.005–3.13 Å⁻¹"),
    ("Detectors", "Pilatus 1M (SAXS), Pilatus 900K (WAXS)"),
]


def saxs_figures():
    D = sas.compute_all()
    g = D["globular"]

    # -- Guinier ----------------------------------------------------------
    q2lim = 0.016

    def near(pts, xt):
        """index of the point closest to a target x -- log-spaced q makes index
        fractions meaningless for label placement."""
        return min(range(len(pts)), key=lambda k: abs(pts[k][0] - xt))

    gp, ga = [], []
    for q, i in zip(g["q"], g["i"]):
        if q * q > q2lim: break
        gp.append((q * q, math.log(i)))
        ga.append((q * q, -q * q * g["rg"] ** 2 / 3))
    gi_lbl, ga_lbl = near(gp, 0.0132), near(ga, 0.0112)
    f_guinier = figure(
        "fig-guinier",
        "Guinier: where the straight line stops being straight",
        "Plot ln I(q) against q² and the low-q data falls on a line whose slope is −Rg²/3. "
        "The approximation only holds while q·Rg stays small, and choosing where to cut it is one of "
        "the judgement calls the pipeline has to make explicit.",
        linechart(
            [{"name": "Computed I(q)", "pts": gp, "var": "--v1",
              "label_at": gi_lbl, "anchor": "end", "label_dy": 24},
             {"name": "Guinier approximation", "pts": ga, "var": "--v2", "dash": True,
              "label_at": ga_lbl, "anchor": "end", "label_dy": -17}],
            xlabel="q² (Å⁻²)", ylabel="ln I(q) / I(0)",
            xdom=(0, q2lim),
            xfmt=lambda v: f"{v:.3f}",
            yfmt=lambda v: f"{v:.1f}",
            marks=[{"type": "vline", "x": g["q2max"],
                    "label": f"q²max = 1.5/Rg² = {g['q2max']:.4f}"}],
            title="Guinier plot for a computed globular scatterer",
            desc="Log intensity against q squared. The computed curve and the Guinier straight-line "
                 "approximation agree below the marked limit and diverge above it."),
        table(["Quantity", "Value"],
              [("Model body", "Sphere, R = 30 Å"),
               ("Rg from p(r)", f"{g['rg']:.2f} Å"),
               ("Exact Rg = R√(3/5)", f"{30*math.sqrt(0.6):.2f} Å"),
               ("Guinier limit q²max = 1.5/Rg²", f"{g['q2max']:.5f} Å⁻²"),
               ("Equivalent q·Rg", f"{math.sqrt(1.5):.2f}")]),
        "computed",
        "Computed for this page from the Debye relation, not measured. The q²max = 1.5/Rg² limit "
        "is the criterion used in the paper. The recovered Rg matches the exact value for a sphere "
        f"({g['rg']:.2f} Å against {30*math.sqrt(0.6):.2f} Å), which is the check that the "
        "calculation is right.",
        legend=legend_items([("--v1", "Computed I(q)"), ("--v2", "Guinier approximation")]))

    # -- Kratky -----------------------------------------------------------
    ks = []
    for name, var in SHAPES:
        d = D[name]
        pts = [(q, 1000 * q * q * i) for q, i in zip(d["q"], d["i"]) if q >= 0.01]
        ks.append({"name": name.replace("-", "‑"), "pts": pts, "var": var,
                   "label_at": max(range(len(pts)), key=lambda k: pts[k][1])})
    f_kratky = figure(
        "fig-kratky",
        "Kratky: shape, read off the curve",
        "q²I(q) against q. A compact body gives a clear peak that falls away; as a particle becomes "
        "elongated or splits into domains the curve broadens and the decay softens. This is the plot the "
        "clustering step turns from an impression into a probability.",
        linechart(ks, xlabel="q (Å⁻¹)", ylabel="q² I(q) / I(0),  × 10⁻³",
                  xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.3f}",
                  title="Kratky plots for three computed bodies",
                  desc="Kratky plots for a globular sphere, an elongated prolate ellipsoid and a "
                       "two-domain dumbbell, all computed from geometry."),
        table(["Body", "Rg (Å)", "Dmax (Å)", "Dmax / Rg"],
              [(sas.BODIES[n][2], f"{D[n]['rg']:.1f}", f"{D[n]['dmax']:.0f}",
                f"{D[n]['dmax']/D[n]['rg']:.2f}") for n, _ in SHAPES]),
        "computed",
        "All three curves come from one calculation per body: Monte-Carlo p(r), then I(q) by the Debye "
        "relation. Because Rg and Dmax are derived from the same p(r), the three figures on "
        "this page are mutually consistent the way a real measurement would be.",
        legend=legend_items([(v, sas.BODIES[n][2]) for n, v in SHAPES]),
        note=f"Note the ratio Dmax/Rg in the table: {D['globular']['dmax']/D['globular']['rg']:.2f} for the "
             f"sphere, against the exact value of {math.sqrt(5/3)*2:.2f} for a solid sphere. Elongation "
             f"pushes it to {D['elongated']['dmax']/D['elongated']['rg']:.2f}. That single ratio carries "
             "much of what the shape classification is picking up on.")

    # -- P(r) -------------------------------------------------------------
    ps = []
    # Every curve peaks near 1.0, so labelling each at its own maximum stacks all
    # three labels on top of one another. Separate them along r instead.
    label_r = {"globular": 20.0, "elongated": 88.0, "two-domain": 64.0}
    for name, var in SHAPES:
        d = D[name]
        pts = list(zip(d["r"], d["p"]))
        li = min(range(len(pts)), key=lambda k: abs(pts[k][0] - label_r[name]))
        ps.append({"name": name.replace("-", "‑"), "pts": pts, "var": var,
                   "label_at": li, "anchor": "middle", "label_dy": -13})
    f_pr = figure(
        "fig-pr",
        "P(r): the histogram of distances inside the particle",
        "Every pair of points in the body contributes one distance. The longest of them is "
        "Dmax, and estimating it reliably from noisy data is the step the model was trained to "
        "assist with.",
        linechart(ps, xlabel="r (Å)", ylabel="p(r), normalised",
                  xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.1f}",
                  marks=[{"type": "vline", "x": D[n]["dmax"],
                          "label": f"Dmax {D[n]['dmax']:.0f} Å"} for n, _ in SHAPES],
                  title="Pair distance distributions for three computed bodies",
                  desc="Pair distance distribution functions. The sphere is symmetric; the elongated "
                       "body has a long tail; the two-domain body is bimodal."),
        table(["Body", "Shape of p(r)", "Dmax (Å)"],
              [(sas.BODIES["globular"][2], "Single symmetric peak", f"{D['globular']['dmax']:.0f}"),
               (sas.BODIES["elongated"][2], "Skewed, long tail to high r", f"{D['elongated']['dmax']:.0f}"),
               (sas.BODIES["two-domain"][2], "Bimodal: within-domain then between-domain",
                f"{D['two-domain']['dmax']:.0f}")]),
        "computed",
        f"Monte-Carlo sampled from the geometry of each body, {sas.N_PAIRS:,} point pairs per body, "
        "fixed seed, smoothed with three passes of a 3-point kernel.",
        legend=legend_items([(v, sas.BODIES[n][2]) for n, v in SHAPES]))

    # -- decision rule ----------------------------------------------------
    f_tol = figure(
        "fig-tolerance",
        "The rule that lets the pipeline decline to answer",
        "The model's predicted Dmax is compared against the value from the BIFT fit. Agree "
        "within 20% and it is reported in green; disagree by more and it is shown in red rather than "
        "quietly returned.",
        tolerance_strip(title="Dmax agreement tolerance",
                        desc="A deviation axis from minus 45 to plus 45 percent. The central plus or "
                             "minus 20 percent band is accepted; outside it, predictions are flagged."),
        table(["Deviation from BIFT Dmax", "Outcome"],
              [("Within ±20%", "Accepted, shown green"),
               ("More than ±20%", "Flagged as low confidence, shown red")]),
        "reported",
        "The ±20% threshold and the red/green reporting are as described in the paper.",
        note="This is the part worth copying. An automated analysis that always returns a "
             "plausible-looking number is worse than none; the useful property is knowing when to stop.")

    # -- MLP --------------------------------------------------------------
    f_mlp = figure(
        "fig-mlp",
        "The regressor",
        "A small, deliberately unglamorous network: four hidden layers of 32 units, trained only on "
        "experimental profiles so that it learns how practitioners actually make this call.",
        mlp_diagram(title="Multilayer perceptron architecture",
                    desc="Input features feed four hidden layers of 32 units each, ending in a single "
                         "output predicting maximum particle dimension."),
        table(["Hyperparameter", "Value"], HYPER),
        "reported",
        "Architecture and hyperparameters as published.")

    # -- detector ---------------------------------------------------------
    pr = sas.pair_distribution("globular")
    q, i = sas.profile(pr, qmin=0.01, qmax=0.62, n=260)
    f_det = figure(
        "fig-detector",
        "What the detector actually sees",
        "Particles tumbling freely in solution scatter isotropically, so the two-dimensional pattern is a "
        "set of concentric rings. The dark bands are not noise. They are the minima of the particle's "
        "form factor, and their spacing is what encodes its size.",
        f'<div class="det">{detector(q, i, title="Simulated solution-scattering detector image", desc="Concentric rings of varying intensity around a central beamstop, computed from the scattering profile of a 30 angstrom sphere.")}</div>',
        table(["Feature", "Meaning"],
              [("Central disc", "Beamstop: the direct beam is blocked"),
               ("Radius", "Increasing q, so decreasing length scale"),
               ("Bright rings", "Maxima of the form factor"),
               ("Dark rings", "Minima: their positions fix the particle radius"),
               ("First minimum", "q ≈ 4.493 / R for a sphere")]),
        "computed",
        "Rendered from the same computed I(q) as the curves above, for a 30 Å sphere. The ring "
        "positions are the real form-factor minima, not decoration.")

    return f_guinier, f_kratky, f_pr, f_det, f_tol, f_mlp, MODEL


# =========================================================================
# 4. Polymer-stabilized enzymes  (doctoral work, in preparation)
# =========================================================================

from viz import flow
from math import comb

WORKFLOW = [
    ("Synthesise copolymer library", "photo-ATRP, one plate"),
    ("Add enzyme", "form polymer–enzyme hybrid"),
    ("Transfer to organic solvent", "water-miscible"),
    ("Read solubility", "plate reader"),
    ("Read retained activity", "enzyme assay"),
    ("Model structure–function", "on every well, including failures"),
]


def enzyme_figures():
    # Combinatorics of a modest copolymer design space -- plain arithmetic.
    n_mon, pick, steps, lengths = 6, 3, 10, 4
    blends = comb(n_mon, pick)                 # which monomers
    comps = comb(steps - 1, pick - 1)          # compositions in 10% increments
    space = blends * comps * lengths
    rows = [
        ("Monomers available", f"{n_mon}", "an illustrative palette"),
        ("Monomers per copolymer", f"{pick}", "terpolymers"),
        ("Distinct monomer sets", f"{blends}", f"C({n_mon},{pick})"),
        ("Compositions per set", f"{comps}", "10% increments summing to 100%"),
        ("Chain-length targets", f"{lengths}", "degree of polymerisation"),
        ("Total distinct polymers", f"{space:,}", f"{blends} × {comps} × {lengths}"),
        ("Plates required", f"{space / 96:.0f}", "at 96 formulations per plate"),
    ]
    f1 = figure(
        "fig-space",
        "Why this has to be run in parallel",
        "A deliberately conservative design space: six monomers, three per polymer, composition in "
        "10% steps, four chain lengths, and it is already past what anyone screens by hand.",
        "", table(["Quantity", "Value", "How"], rows), "computed",
        "Plain combinatorial arithmetic for an illustrative palette, not a description of a specific "
        "screen. The point is the order of magnitude.",
        note=f"{space:,} polymers is about {space/96:.0f} plates. At one hand-run reaction per hour it is "
             "years of benchwork; on an automated platform it is a manageable campaign. And the real space "
             "is larger, because composition does not come in tidy 10% steps.")

    f2 = figure(
        "fig-workflow",
        "The assay, end to end",
        "Each step has to survive being done ninety-six times in parallel without the numbers drifting.",
        flow(WORKFLOW, title="Polymer-stabilized enzyme screening workflow",
             desc="Six steps: synthesise copolymer library, add enzyme, transfer to organic solvent, "
                  "read solubility, read retained activity, model structure-function."),
        table(["Step", "Stage", "Detail"],
              [(str(i + 1), s, sub) for i, (s, sub) in enumerate(WORKFLOW)]),
        "schematic",
        "A diagram of the approach. Results from this work are in preparation and are not shown here.")
    return f1, f2
