# -*- coding: utf-8 -*-
"""Deep research pages.

Only values stated in the published papers appear here. Nothing on these pages
is simulated, illustrative or reconstructed: if a number is shown, it was
printed in the paper it is attributed to. Tables, not charts -- a plot of three
cherry-picked values, or of quantities that are not comparable, says less than
the numbers themselves.
"""
from viz import figure, table

# =========================================================================
# 1. Machine learning for biomaterials  (Tissue Engineering Part A, 2024)
# =========================================================================

DATASETS = [
    ("Scaffold study", "182 scaffolds", "13 polymers, 182 scaffolds tested"),
    ("Titanium nanotube analysis", "272 samples", "272 labelled samples drawn from 30 publications"),
    ("Kohn polyacrylate library", "112 polymers", "112 distinct degradable polymers"),
    ("Lipid nanoparticle screen", "1,080 formulations", "1,080-LNP formulation library"),
    ("Poly(β-amino ester) library", "~2,500 polymers", "degradable PAEs for gene delivery"),
]

DESCRIPTORS = [
    ("Structural", "Fibre diameter, pore diameter, porosity, pore size"),
    ("Mechanical", "Young's modulus, compressive strength"),
    ("Thermal", "Glass transition temperature"),
    ("Surface", "Contact angle, roughness, hydrophobicity, wettability"),
    ("Compositional", "Monomer ratios, pendant groups, backbone modifications"),
    ("Molecular", "Cheminformatic descriptors (e.g. PaDEL) for lipids and small molecules"),
]


def ml_figures():
    f1 = figure(
        "fig-datasets",
        "How big is a high-throughput biomaterials dataset?",
        "Study sizes cited in the review. A carefully built experimental library runs to hundreds or "
        "a few thousand members, which is what the modelling has to work with.",
        "", table(["Study", "Size", "Description"], DATASETS), "reported",
        "Study sizes as cited in Ahmed <em>et al.</em>, <em>Tissue Engineering Part A</em> 30(19–20), "
        "662–680 (2024).")

    f3 = figure(
        "fig-descriptors",
        "What a polymer looks like to a model",
        "A model cannot read a structure. It reads whatever numbers you chose to describe it, and "
        "that choice bounds what the model can possibly learn.",
        "", table(["Descriptor family", "Examples"], DESCRIPTORS), "reported",
        "Descriptor families as surveyed in the review.")
    return f1, f3


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
    ("Acrylates, optimised", "1.15", "best reported condition"),
    ("Acrylates, well-controlled", "< 1.30", "reported upper bound across the acrylate screen"),
    ("MMA with PMDETA + BPN", "1.26", "at target specifications"),
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

PAIRING = {"acrylate": "Me₆TREN + MBiB", "methacrylate": "PMDETA + BPN"}


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
        "", table(["Monomer", "Class", "Reported best pairing"],
                  [(f"{n} ({a})", c, PAIRING[c]) for n, a, c in MONOMERS]), "reported",
        "As reported in the paper: Me₆TREN consistently produced high dispersity with MMA, while "
        "PMDETA and BPN emerged as the most suitable reagents for high-throughput MMA synthesis.",
        note="Methyl methacrylate propagates more slowly than the acrylates, so the activation–"
             "deactivation balance that ATRP depends on has to be retuned. There is no reliable way to "
             "reason to the answer from first principles, which is exactly why screening it is worth the "
             "instrument time.")

    f3 = figure(
        "fig-dispersity",
        "Dispersity, reported",
        "Đ = M𝓌/Mₙ. A perfectly uniform chain population would be 1.00; below about 1.3 is "
        "normally taken as well-controlled.",
        "", table(["Condition", "Đ", "Note"], DISPERSITY), "reported",
        "Only values stated in the paper are listed. This is not the full screen. For the complete "
        "dataset see the publication.")
    return f1, f2, f3


# =========================================================================
# 3. SAXS + machine learning  (Biophysical Journal, 2025)
# =========================================================================

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

OUTPUTS = [
    ("Guinier Rg", "Radius of gyration from the low-q straight-line fit"),
    ("PDDF Rg", "Radius of gyration from the pair distance distribution"),
    ("Dmax", "Maximum particle dimension, from the PDDF and from the trained model"),
    ("Kratky features", "Shape-descriptive features used by the clustering step"),
    ("Confidence flag", "Whether the two Rg routes agree well enough to report the result"),
]


def saxs_figures():
    f_out = figure(
        "fig-outputs",
        "What the pipeline returns for each profile",
        "The tool extracts the same set of parameters for every dataset, which is what makes a "
        "batch of profiles comparable rather than a set of individual judgement calls.",
        "", table(["Output", "What it is"], OUTPUTS), "reported",
        "Outputs as described in Ramirez, Di Mare, Byrnes, Ahmed <em>et al.</em>, "
        "<em>Biophysical Journal</em> 124(21), 3772–3786 (2025).")

    f_tol = figure(
        "fig-tolerance",
        "The rule that lets the pipeline decline to answer",
        "The model's predicted Dmax is compared against the value from the BIFT fit. Agree "
        "within 20% and it is reported in green; disagree by more and it is shown in red rather than "
        "quietly returned.",
        "", table(["Deviation from BIFT Dmax", "Outcome"],
                  [("Within ±20%", "Accepted, shown green"),
                   ("More than ±20%", "Flagged as low confidence, shown red")]), "reported",
        "The ±20% threshold and the red/green reporting are as described in the paper.",
        note="This is the part worth copying. An automated analysis that always returns a "
             "plausible-looking number is worse than none; the useful property is knowing when to stop.")

    f_mlp = figure(
        "fig-mlp",
        "The regressor",
        "A small, deliberately unglamorous network: four hidden layers of 32 units, trained only on "
        "experimental profiles so that it learns how practitioners actually make this call.",
        "", table(["Hyperparameter", "Value"], HYPER), "reported",
        "Architecture and hyperparameters as published.")

    return f_out, f_tol, f_mlp, MODEL


# =========================================================================
# 4. Polymer-stabilized enzymes  (doctoral work, in preparation)
# =========================================================================

WORKFLOW = [
    ("Synthesise copolymer library", "photo-ATRP, one plate"),
    ("Add enzyme", "form polymer–enzyme hybrid"),
    ("Transfer to organic solvent", "water-miscible"),
    ("Read solubility", "plate reader"),
    ("Read retained activity", "enzyme assay"),
    ("Model structure–function", "on every well, including failures"),
]


def enzyme_figures():
    return (figure(
        "fig-workflow",
        "The assay, end to end",
        "Each step has to survive being done ninety-six times in parallel without the numbers drifting.",
        "", table(["Step", "Stage", "Detail"],
                  [(str(i + 1), s, sub) for i, (s, sub) in enumerate(WORKFLOW)]), "schematic",
        "A description of the approach. This work is in preparation; no results are shown."),)
