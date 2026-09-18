# -*- coding: utf-8 -*-
"""
Single source of truth for emanahmed.org.

Every bibliographic field here was taken from the publisher of record
(ACS, Liebert, Cell Press) or PubMed Central. Do not edit generated HTML —
edit this file and re-run `python3 _src/build.py`.
"""

SITE = "https://emanahmed.org"

PROFILE = {
    "name": "Eman Ahmed",
    "given": "Eman",
    "family": "Ahmed",
    "role": "PhD Candidate in Biomedical Engineering",
    "lab": "Gormley Lab",
    "lab_url": "https://www.gormleylab.com/",
    "dept": "Department of Biomedical Engineering",
    "dept_url": "https://bme.rutgers.edu/",
    "org": "Rutgers, The State University of New Jersey",
    "org_url": "https://www.rutgers.edu",
    "city": "Piscataway",
    "region": "NJ",
    "country": "US",
    "email": "eman.ahmed@rutgers.edu",
    "scholar": "https://scholar.google.com/citations?user=2X7j71EAAAAJ&hl=en",
    "linkedin": "https://www.linkedin.com/in/eman-ahmed-14724613b/",
    # Scholar metrics — update when you refresh them, and move the date with them.
    "metrics": {"papers": "3", "citations": "43", "hindex": "3", "asof": "September 2026"},
    "photo": "images/eman-us.jpeg",
    "advisor": "Adam J. Gormley",
    "advisor_url": "https://bme.rutgers.edu/adam-j-gormley",
}

# Terms a researcher in this field would actually type. Used for knowsAbout
# and to keep page copy honest about what the site is about.
EXPERTISE = [
    "High-throughput experimentation",
    "Machine learning for biomaterials",
    "Atom transfer radical polymerization (ATRP)",
    "Photoinduced ATRP",
    "Reversible-deactivation radical polymerization",
    "Random copolymers",
    "Protein stabilization",
    "Polymer-enzyme hybrids",
    "Biocatalysis in organic solvents",
    "Small-angle X-ray scattering (SAXS)",
    "Laboratory automation",
    "Liquid handling robotics",
    "Structure-property relationships",
    "Polymer chemistry",
    "Biomaterials discovery",
]

# --- Publications ----------------------------------------------------------
# role: "first" | "co"  — status: "published" | "inprep"

PUBLICATIONS = [
    {
        "slug": "mapping-biomaterial-complexity-machine-learning",
        "short": "Mapping Biomaterial Complexity by ML",
        "meta": "First-author review in Tissue Engineering Part A: using high-throughput experimentation and machine learning to map biomaterial structure-function behaviour.",
        "title": "Mapping Biomaterial Complexity by Machine Learning",
        "authors": ["Eman Ahmed", "Prajakatta Mulay", "Cesar Ramirez",
                    "Gabriela Tirado-Mansilla", "Eugene Cheong", "Adam J. Gormley"],
        "role": "first",
        "status": "published",
        "type": "Review",
        "journal": "Tissue Engineering Part A",
        "volume": "30",
        "issue": "19-20",
        "pages": "662-680",
        "firstpage": "662",
        "lastpage": "680",
        "year": "2024",
        "date": "2024-10-11",
        "date_h": "11 October 2024",
        "doi": "10.1089/ten.tea.2024.0067",
        "pmid": "39135398",
        "pmcid": "PMC12394815",
        "citations": "25",
        "keywords": ["biomaterials", "high-throughput experimentation", "machine learning",
                     "structure-property relationships", "tissue engineering", "data mining"],
        "abstract": (
            "Biomaterials often have subtle properties that ultimately drive their bespoke performance. "
            "Given this nuanced structure–function behavior, the standard scientific approach of one "
            "experiment at a time or design of experiment methods is largely inefficient for the discovery "
            "of complex biomaterials. More recently, high-throughput experimentation coupled with machine "
            "learning methods has matured beyond expert users allowing scientists and engineers from diverse "
            "backgrounds to access these powerful data science tools. As a result, we now have the opportunity "
            "to strategically utilize all available data from high-throughput experiments to train efficacious "
            "models and map the structure-function behavior of biomaterials for their discovery. Herein, we "
            "discuss this necessary shift to data-driven determination of structure–function properties of "
            "biomaterials as we highlight how machine learning is leveraged in identifying physicochemical cues "
            "for biomaterials in tissue engineering, gene delivery, drug delivery, protein stabilization, and "
            "antifouling materials. We also discuss data-mining approaches that are coupled with machine learning "
            "to map biomaterial functions that reduce the load on experimental approaches for faster biomaterial "
            "discovery. Ultimately, harnessing the prowess of machine learning will lead to accelerated discovery "
            "and development of optimal biomaterial designs."
        ),
        "plain": (
            "Biomaterials rarely fail or succeed for one obvious reason — performance usually comes from a "
            "combination of small structural details interacting at once. Testing those combinations one experiment "
            "at a time does not scale. This review sets out how high-throughput experimentation paired with machine "
            "learning changes the search: run many conditions in parallel, keep every data point including the "
            "failures, and train models that map structure to function across the whole space rather than at a few "
            "sampled points."
        ),
        "why": [
            "Covers five application areas in one place — tissue engineering, gene delivery, drug delivery, protein stabilization and antifouling materials — rather than a single material class.",
            "Treats data mining as a first-class method alongside experiment, showing where published data can substitute for benchwork.",
            "Written for experimentalists adopting ML, not for ML specialists: the framing is which model to reach for and what data it needs.",
        ],
        "tags": ["Machine learning", "High-throughput", "Biomaterials", "Review"],
    },
    {
        "slug": "automation-assisted-photo-atrp",
        "short": "Automation-Assisted Photoinduced ATRP",
        "meta": "How oxygen-tolerant chemistry puts ATRP on a liquid-handling robot: high-throughput screening of ligands and initiators, published in ACS Polymers Au.",
        "title": "Automation-Assisted Photoinduced Atom Transfer Radical Polymerization",
        "authors": ["Cesar Ramirez", "Eman Ahmed", "Elena Di Mare", "Maria Pineiro-Goncalves",
                    "Apostolos Maroulis", "Prajakatta Mulay", "D. Christopher Radford", "Adam J. Gormley"],
        "role": "co",
        "status": "published",
        "type": "Research article",
        "journal": "ACS Polymers Au",
        "volume": "6",
        "issue": "1",
        "pages": "181-193",
        "firstpage": "181",
        "lastpage": "193",
        "year": "2026",
        "date": "2026-02-11",
        "date_h": "Published online 28 August 2025; issue 11 February 2026",
        "doi": "10.1021/acspolymersau.5c00067",
        "pmid": "41693847",
        "pmcid": "PMC12903423",
        "citations": "10",
        "keywords": ["ATRP", "photo-ATRP", "laboratory automation", "high-throughput polymer synthesis",
                     "oxygen tolerance", "reversible-deactivation radical polymerization"],
        "abstract": (
            "Oxygen-tolerant reversible-deactivation radical polymerizations (RDRP) now allow many of these "
            "reactions to proceed in open labware, such as well plates. This enables the high-throughput synthesis "
            "of tailored polymers and lowers the knowledge barrier required to obtain these materials. Building on "
            "our previous work automating photoinduced electron/energy transfer reversible addition–fragmentation "
            "chain transfer (PET–RAFT) and enzyme-assisted RAFT (Enz-RAFT) polymerization, we now introduce "
            "automated atom transfer radical polymerization (ATRP). Here, we demonstrate the potential of this "
            "platform for the high-throughput optimization of ATRP chemistry. Furthermore, we demonstrate that this "
            "workflow can help provide insights into the selection of reaction components, such as ligands and "
            "initiators, for the polymerization of kinetically difficult monomers such as methyl methacrylate with "
            "smaller rates of propagation than acrylates. This coupling paves the way for data-driven optimization "
            "of ATRP reactions, accelerated by the generation of high-throughput data sets. To facilitate the "
            "integration of robotics for high-throughput applications in polymer synthesis and optimization of "
            "photo-ATRP, we have made a Python package available to assist with experimental planning."
        ),
        "plain": (
            "ATRP is one of the workhorse reactions for making polymers with controlled length and composition, but "
            "it has historically needed inert, oxygen-free conditions — which rules out running it in an open well "
            "plate on a robot. Oxygen-tolerant chemistry removes that constraint. This paper puts photo-ATRP onto an "
            "automated liquid-handling platform and uses it to screen reaction components at a scale that is "
            "impractical by hand, including for methyl methacrylate, a monomer that propagates slowly enough to be "
            "genuinely awkward to optimise."
        ),
        "why": [
            "Extends the group's automated platform from PET-RAFT and Enz-RAFT to ATRP, so a third major RDRP chemistry becomes accessible to high-throughput screening.",
            "Produces practical guidance on ligand and initiator selection for kinetically difficult monomers such as methyl methacrylate.",
            "Ships a Python package for experimental planning, so the workflow is reproducible outside the originating lab.",
        ],
        "tags": ["ATRP", "Automation", "Polymer synthesis", "Robotics"],
    },
    {
        "slug": "saxs-assistant-automated-saxs-analysis",
        "short": "SAXS Assistant: Automated SAXS Analysis",
        "meta": "Open-source Python tool that automates SAXS analysis, estimates maximum particle dimension with machine learning, and flags low-confidence results.",
        "title": "SAXS Assistant: Automated SAXS analysis for structural discovery in biologics and polymeric nanoparticles",
        "authors": ["Cesar Ramirez", "Elena Di Mare", "James Byrnes", "Eman Ahmed",
                    "Maria Pineiro-Goncalves", "Cristian Lopez", "N. Sanjeeva Murthy", "Adam J. Gormley"],
        "role": "co",
        "status": "published",
        "type": "Research article",
        "journal": "Biophysical Journal",
        "volume": "124",
        "issue": "21",
        "pages": "3772-3786",
        "firstpage": "3772",
        "lastpage": "3786",
        "year": "2025",
        "date": "2025-09-23",
        "date_h": "23 September 2025",
        "doi": "10.1016/j.bpj.2025.09.034",
        "pmid": "40999685",
        "citations": "8",
        "code": "https://pypi.org/project/SAXS-Assistant/",
        "code_label": "pip install SAXS-Assistant",
        "keywords": ["small-angle X-ray scattering", "SAXS", "machine learning", "radius of gyration",
                     "pair distance distribution function", "polymeric nanoparticles", "BioXTAS RAW"],
        "abstract": (
            "Small-angle x-ray scattering (SAXS) is a powerful technique for assessing macromolecular structure. "
            "High-throughput SAXS is limited by the time-consuming and, at times, subjective nature of SAXS data "
            "interpretation. Here, we present SAXS Assistant, a Python-based script that streamlines SAXS data "
            "analysis to extract features for machine learning (ML) and key structural parameters, including the "
            "Guinier radius of gyration (Rg), pair distance distribution function (PDDF)-derived Rg, maximum particle "
            "dimension (Dmax), and Kratky plots. The script builds upon BioXTAS RAW and validates reliability via "
            "Guinier/PDDF Rg agreement, an important indicator of well-measured data sets. For assistance in Dmax "
            "estimation, a multilayer perceptron regressor was trained with 1940 data files from the Small Angle "
            "Scattering Biological Data Bank. The model achieved a test set performance R2 = 0.90 and mean absolute "
            "error = 11.7 Å. Training exclusively with experimental data translates analyses from researchers, "
            "including experts in the field, to the ML model, which helps assess Dmax estimations from PDDF. Gaussian "
            "mixture model clustering was implemented to classify profiles into structural classes based on entries in "
            "the Small Angle Scattering Biological Data Bank. Users may therefore assess the similarity between "
            "experimental samples and known biomolecular shapes within the mapped repository entries. This "
            "probabilistic clustering aids in quantifying information from Kratky and generating shape-descriptive "
            "features. SAXS Assistant accelerates SAXS data analysis through enforced quality control, ML-ready "
            "outputs, and flags for low-confidence results. In addition to providing the ability to analyze large data "
            "sets at high throughput, this tool is versatile and may serve researchers in both biological and synthetic "
            "polymer research fields."
        ),
        "plain": (
            "SAXS tells you the size and shape of something in solution, but getting there involves judgement calls — "
            "where to set the Guinier range, whether a P(r) fit is trustworthy, what maximum dimension to believe. Those "
            "calls are slow and they vary between analysts, which is a problem once you are producing hundreds of "
            "profiles. SAXS Assistant automates the pipeline, trains a model on 1,940 experimental profiles from the "
            "SASBDB to estimate Dmax, clusters profiles against known biomolecular shapes, and flags results it is not "
            "confident about instead of quietly returning them."
        ),
        "why": [
            "Trained only on experimental SASBDB data, so the model reproduces how practitioners actually analyse profiles rather than idealised simulations.",
            "Reports test-set R² = 0.90 and mean absolute error of 11.7 Å for maximum particle dimension.",
            "Flags low-confidence results rather than returning them silently — the quality control is part of the tool, not a separate manual step.",
            "Released open source on PyPI and built on BioXTAS RAW, so it slots into existing SAXS workflows.",
        ],
        "tags": ["SAXS", "Machine learning", "Open source", "Nanoparticles"],
    },
    {
        "slug": None,
        "title": "High-Throughput Approach for Evaluating the Solubility of Polymer-Stabilized Proteins in Organic Solvent",
        "authors": ["Eman Ahmed", "Adam J. Gormley"],
        "role": "first",
        "status": "inprep",
        "type": "Manuscript in preparation",
        "journal": None,
        "year": None,
        "citations": None,
        "plain": (
            "The doctoral project: a plate-based, automated assay for asking which random copolymers keep an enzyme "
            "soluble and active once it is moved into a water-miscible organic solvent."
        ),
        "tags": ["Protein stabilization", "High-throughput", "Biocatalysis"],
    },
]

PUBLISHED = [p for p in PUBLICATIONS if p["status"] == "published"]

# --- Research areas --------------------------------------------------------

AREAS = [
    {
        "id": "protein-stabilization",
        "icon": "flask",
        "title": "Polymer-stabilized enzymes in organic solvents",
        "lede": "Doctoral project, Gormley Lab, 2022-2026",
        "body": [
            "Enzymes are extraordinary catalysts in water and frequently useless outside it. Move one into a "
            "water-miscible organic solvent — which is often where the interesting synthetic chemistry happens — "
            "and it tends to unfold, aggregate and drop out of solution.",
            "Random copolymers can act as synthetic chaperones, wrapping a protein in a shell whose chemistry can be "
            "tuned monomer by monomer. The difficulty is that the design space is enormous and the structure-function "
            "relationship is not obvious from first principles. My work builds plate-based, automated assays that "
            "measure solubility and retained activity across large copolymer libraries, so the search can be run "
            "empirically at scale rather than one rational design at a time.",
        ],
        "tags": ["Random copolymers", "Polymer-enzyme hybrids", "Biocatalysis", "Solubility assays", "Automation"],
    },
    {
        "id": "machine-learning",
        "icon": "model",
        "title": "Machine learning for biomaterial structure-function mapping",
        "lede": "First-author review, Tissue Engineering Part A, 2024",
        "body": [
            "High-throughput experiments produce the kind of data that models need: many conditions, consistent "
            "measurement, and — importantly — retained failures. The question is what to do with it.",
            "My review in Tissue Engineering Part A surveys how machine learning is being used to identify the "
            "physicochemical cues that govern biomaterial performance, across tissue engineering, gene delivery, drug "
            "delivery, protein stabilization and antifouling surfaces, along with the data-mining approaches that let "
            "published results stand in for experiments that have not been run yet.",
        ],
        "tags": ["Structure-property relationships", "Data mining", "Model selection", "Biomaterials discovery"],
    },
    {
        "id": "automation",
        "icon": "robot",
        "title": "Automated polymer synthesis and analysis",
        "lede": "photo-ATRP platform and SAXS Assistant",
        "body": [
            "Oxygen-tolerant reversible-deactivation radical polymerization made it possible to run controlled polymer "
            "chemistry in open labware. That is what puts it within reach of a liquid handler, and it is the premise "
            "behind our automated photo-ATRP platform, which screens ligands and initiators for monomers — methyl "
            "methacrylate among them — that are slow enough to be painful to optimise by hand.",
            "Synthesis throughput is only useful if characterisation keeps up. SAXS Assistant addresses the other end "
            "of the pipeline: it automates small-angle X-ray scattering analysis, estimates maximum particle dimension "
            "with a model trained on 1,940 experimental profiles, and refuses to report results it cannot stand behind.",
        ],
        "tags": ["photo-ATRP", "Liquid handling robotics", "SAXS", "Open-source tooling", "Reproducibility"],
    },
]

METHODS = [
    ("Polymer chemistry", "Photoinduced ATRP, PET-RAFT, random copolymer synthesis, vacuum filtration, solubility characterisation"),
    ("High-throughput experimentation", "Liquid handling robotics, 96-well plate assay design, automated enzyme activity and solubility screening"),
    ("Structural characterisation", "Small-angle X-ray scattering, Guinier and P(r) analysis, Kratky interpretation, synchrotron data workflows"),
    ("Computation", "Python, scikit-learn, multilayer perceptron and Gaussian mixture models, data visualisation, experimental design automation"),
    ("Biophysics", "Protein stabilization, biocatalysis in water-miscible organic solvents, coarse-grained modelling of lipid membranes"),
]
