# -*- coding: utf-8 -*-
"""
Research notes: plain-language companions to peer-reviewed work.

Every factual claim in these notes traces to one of the papers in data.py.
Each note carries a visible provenance line linking the paper it summarises.
"""

NOTES = [
    {
        "slug": "why-a-well-plate-changed-polymer-chemistry",
        "meta": "Oxygen-tolerant chemistry moved controlled radical polymerisation out of sealed glassware and into open well plates, which is what makes it robot-ready.",
        "title": "What oxygen tolerance buys you in polymer chemistry",
        "date": "2026-03-04",
        "date_h": "4 March 2026",
        "desc": ("Controlled radical polymerisation used to require sealed, degassed glassware. Oxygen-tolerant "
                 "chemistry moved it into open well plates, and that one change is what puts polymer synthesis "
                 "within reach of a liquid-handling robot."),
        "tags": ["ATRP", "Automation", "High-throughput"],
        "source": "automation-assisted-photo-atrp",
        "reading": "6",
        "body": """
<p>If you have only ever seen controlled radical polymerisation described in a textbook, the constraint that shapes
everything in practice is easy to miss: oxygen kills it. Propagating radicals react with molecular oxygen far faster
than they react with monomer, so a conventional atom transfer radical polymerisation needs sealed glassware and a
freeze-pump-thaw cycle or a nitrogen sparge before anything useful happens.</p>

<p>That requirement quietly sets the ceiling on how many experiments you can run. Degassing is manual, it is slow, and
it does not parallelise. A skilled person might set up a dozen carefully controlled reactions in a day. Twelve points is
not enough to map a reaction space with four or five interacting variables.</p>

<h2>Open labware is the whole point</h2>

<p>Oxygen-tolerant reversible-deactivation radical polymerisation changes the arithmetic. By building oxygen consumption
into the system itself, photocatalytically, enzymatically, or through the reducing environment of the
photo-ATRP mechanism, the reaction becomes something you can run in an uncapped well on an open bench.</p>

<p>Once that is true, a 96-well plate stops being a container and becomes an experimental design. Each well is an
independent condition. A liquid handler can lay down ninety-six different ligand, initiator, monomer and catalyst
combinations in the time it would take to degas one flask, and every one of them is measured the same way, which
matters more than it sounds like it should. Consistency in how data is collected is what makes it usable for modelling
later.</p>

<h2>Where it gets interesting: the slow monomers</h2>

<p>Acrylates propagate quickly and are relatively forgiving. Methacrylates are not. Methyl methacrylate has a
substantially smaller propagation rate constant, which means the balance between activation and deactivation that ATRP
depends on has to be tuned more carefully, and the right ligand and initiator pairing is not something you can
reliably reason your way to from first principles.</p>

<p>This is precisely the situation where throughput earns its keep. Rather than arguing about which ligand should work,
you screen the ligands. In our <a href="../publications/automation-assisted-photo-atrp.html">ACS Polymers Au
paper</a> we used an automated photo-ATRP platform to do exactly that, extending a workflow the lab had previously
built for PET-RAFT and enzyme-assisted RAFT to a third major polymerisation chemistry.</p>

<h2>The unglamorous part that makes it reproducible</h2>

<p>A high-throughput platform that only works in the lab that built it is a demo, not a method. The practical obstacle
is rarely the robot. It is translating an intended experimental design into the deck layout, volumes and transfer
sequence the instrument needs, without arithmetic errors propagating silently across ninety-six wells.</p>

<p>We released a Python package to handle that planning step. It is not the scientifically exciting part of the work,
and it is probably the part that determines whether anyone else can run it.</p>

<h2>What this unlocks</h2>

<p>The reason to care about throughput here is not throughput. It is that data-driven optimisation of polymerisation
conditions needs datasets that are large, consistent and include the conditions that did not work. Hand-run chemistry
produces small datasets biased towards conditions the chemist already expected to succeed. Plate-based chemistry
produces the other kind.</p>
"""
    },
    {
        "slug": "trusting-a-saxs-analysis-you-did-not-do-by-hand",
        "meta": "SAXS analysis is full of judgement calls that vary between analysts. Automating it means making them explicit, and flagging profiles you should not trust.",
        "title": "Trusting a SAXS analysis you didn't do by hand",
        "date": "2026-01-22",
        "date_h": "22 January 2026",
        "desc": ("Small-angle X-ray scattering analysis is full of judgement calls that vary between analysts. "
                 "Automating it is less about speed than about making those calls explicit, and about flagging "
                 "the profiles where the answer should not be trusted."),
        "tags": ["SAXS", "Machine learning", "Reproducibility"],
        "source": "saxs-assistant-automated-saxs-analysis",
        "reading": "7",
        "body": """
<p>Small-angle X-ray scattering gives you the size and shape of something in solution without crystallising it, which is
why it is so useful for proteins, polymer nanoparticles and anything else that will not sit still. What it does not give
you is an unambiguous answer. Between the raw scattering curve and a reported radius of gyration sit a series of
decisions, and different analysts make them differently.</p>

<h2>The judgement calls</h2>

<p>Where do you set the Guinier region? Too narrow and the fit is noisy; too wide and you violate the approximation the
fit depends on. How do you choose the maximum particle dimension, <code>Dmax</code>, when computing the pair distance
distribution function? Pick it too small and you truncate real structure, too large and you invent oscillation that is
not there. Is the sample aggregating? Is there interparticle interference at low <em>q</em>?</p>

<p>An experienced person handles all of this more or less automatically, and does it well. The problem is that they
handle it at a rate of a few profiles an hour, and two experienced people will not produce identical numbers. Once you
are generating hundreds of profiles from a high-throughput synthesis campaign, both of those facts become blocking.</p>

<h2>Cross-validation instead of assertion</h2>

<p>The design decision I think matters most in <a href="../publications/saxs-assistant-automated-saxs-analysis.html">SAXS
Assistant</a> is that it does not simply report a number. There are two independent routes to a radius of gyration: the
Guinier approximation at low <em>q</em>, and integration of the pair distance distribution function. On a well-measured
dataset those two should agree. When they diverge, something is wrong: with the measurement, the buffer
subtraction, or the assumption of monodispersity.</p>

<p>Using that agreement as a built-in quality gate means the tool has a basis for declining to answer, which is the
property you actually want from automation. A pipeline that confidently returns a plausible-looking number for a bad
profile is worse than no pipeline.</p>

<h2>Training on what people actually did</h2>

<p>For <code>Dmax</code> estimation we trained a multilayer perceptron regressor on 1,940 experimental data files from
the Small Angle Scattering Biological Data Bank. The choice of training data is deliberate: these are real profiles with
<code>Dmax</code> values chosen by researchers, many of them specialists. The model is therefore learning how the field
makes this judgement, not how an idealised simulation behaves.</p>

<p>On a held-out test set it reached R&sup2; = 0.90 with a mean absolute error of 11.7&nbsp;&Aring;. That is not a
replacement for expert review on a structure you intend to publish. It is entirely adequate for triaging several hundred
profiles down to the handful that deserve it.</p>

<h2>Shape, without pretending to a structure</h2>

<p>The other piece is classification. We fitted a Gaussian mixture model over SASBDB entries to group scattering profiles
into structural classes, so a user can ask how closely an experimental sample resembles known biomolecular shapes. The
Kratky plot has always carried this information (folded, unfolded, multidomain), but reading it has been
qualitative. Clustering makes it a probability rather than an impression, without overclaiming that you have solved a
structure.</p>

<h2>The general point</h2>

<p>Automating an analysis forces you to write down the decisions that were previously made implicitly. That is
uncomfortable, because some of them turn out not to have a principled basis. It is also the only way to make the
analysis reproducible, and the flags for low-confidence results are, in the end, more valuable than the speed.</p>
"""
    },
    {
        "slug": "biomaterials-discovery-needs-the-failures",
        "meta": "The biomaterials literature records what worked, so models trained on it never see the boundary of the useful region. High-throughput screening fixes that.",
        "title": "Biomaterials discovery needs the experiments that failed",
        "date": "2025-11-12",
        "date_h": "12 November 2025",
        "desc": ("Machine learning on biomaterials data keeps running into the same problem: the published record is "
                 "a survivorship-biased sample of what worked. High-throughput experimentation is one of the few ways "
                 "to fix that at the source."),
        "tags": ["Machine learning", "Biomaterials", "Research practice"],
        "source": "mapping-biomaterial-complexity-machine-learning",
        "reading": "6",
        "body": """
<p>Biomaterials are hard to design because their performance usually comes from several subtle properties interacting at
once. Surface chemistry, molecular weight distribution, charge density, hydrophobic balance and architecture all
contribute, and rarely independently. The structure&ndash;function relationship is real, but it is not something you can
usually write down.</p>

<p>The traditional response is to hold everything constant and vary one thing. It is rigorous, and in a space with this
much interaction between variables it is close to hopeless. You sample a line through a space that has structure
in every direction.</p>

<h2>The obvious fix has a less obvious problem</h2>

<p>Machine learning is the natural tool for a high-dimensional structure&ndash;function map, and the barrier to using it
has dropped sharply: an experimentalist can now train a competent model without a background in statistics. That is a
genuine shift, and it is the shift our <a href="../publications/mapping-biomaterial-complexity-machine-learning.html">review
in Tissue Engineering Part A</a> was written around.</p>

<p>But models are only as good as what they learn from, and the biomaterials literature is a filtered sample. Papers
report the formulations that worked. The ones that aggregated, or failed to release, or provoked an immune response, are
mostly absent, not through dishonesty, but because a null result is hard to publish and the material was
abandoned.</p>

<p>A model trained on that record learns which successful materials resemble other successful materials. It has very
little to say about where the boundary of the useful region lies, because it has never been shown the other side of it.</p>

<h2>Why high-throughput data is different in kind</h2>

<p>This is the part I think is underappreciated. When you run a 96-well plate, you keep every well. The formulations that
precipitated are recorded with the same rigour as the ones that performed, because they were measured by the same
instrument in the same run. You are not making a publication decision about each data point.</p>

<p>The resulting dataset is balanced in a way that a literature-derived one structurally cannot be. That is a large part
of why high-throughput experimentation and machine learning belong together, not because the throughput is
impressive, but because of what it does to the shape of the data.</p>

<h2>Where data mining still helps</h2>

<p>None of which means the published record is useless. Text and data mining across existing literature can map regions
of a design space cheaply enough to tell you where not to spend benchtime, and for well-studied material classes the
aggregate signal is strong. Our review covers these approaches alongside direct experimentation, across tissue
engineering, gene delivery, drug delivery, protein stabilization and antifouling materials.</p>

<p>The practical position is that mined data is good for narrowing and high-throughput data is good for deciding. Used
the other way round, you get a model that is confident about a region nobody has actually measured.</p>

<h2>What follows for how we run experiments</h2>

<p>If you accept that the failures carry information, some things follow. Record them with the same metadata as the
successes. Do not discard a plate because most of it did not work. Report the full screened range, not the subset that
supports the conclusion. And design assays so that failure produces a number rather than an absence: a solubility
of zero is data; a well you stopped measuring is not.</p>
"""
    },
]
