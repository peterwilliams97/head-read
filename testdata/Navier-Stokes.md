# **Navier–Stokes: from the equations to the September 2026 blow-up claim**

*Bracketed references like \[Note A\] point to the Notes section at the end. Sections 1–7, 10 and the Notes are stable, textbook material. Sections 8, 9 and 11 describe events of 8–9 September 2026 and carry a status note.*  
 

## **1\. What the equations say**

Take a fluid filling three-dimensional space. Describe it by a velocity field u(x, t), a vector at each point x and time t, and a pressure field p(x, t). We assume the fluid is **incompressible** (constant density, which we set to 1\) and **viscous** (it has internal friction, measured by a constant ν \> 0). A body force f(x, t) may act on it, gravity for example, or something we choose.  
   
The [Navier–Stokes equations](https://en.wikipedia.org/wiki/Navier%E2%80%93Stokes_equations) are:  
   
**∂u/∂t \+ (u·∇)u \= −∇p \+ ν∆u \+ f**  
**∇·u \= 0**

   
The first line is Newton's second law applied to a small parcel of fluid. Read the terms left to right:

> * **∂u/∂t \+ (u·∇)u** is the acceleration of the parcel. The parcel is moving with velocity u, so the rate of change it experiences is not just ∂u/∂t at a fixed point but also the change it sees by being carried to a new location. That second piece, (u·∇)u, is the *advective* or *convective* term. Write it out in components: (u·∇)u \= u₁ ∂u/∂x₁ \+ u₂ ∂u/∂x₂ \+ u₃ ∂u/∂x₃. It is quadratic in u. This single term is responsible for essentially every difficulty in the subject.  
> * **−∇p** is the force from pressure differences. Fluid is pushed from high pressure toward low.  
> * **ν∆u** is viscous diffusion. The Laplacian smooths the velocity field the same way it smooths temperature in the heat equation. Viscosity turns kinetic energy into heat and erases fine detail.  
> * **f** is whatever external force we impose.

   
The second line, ∇·u \= 0, says the flow neither creates nor destroys volume. It is a constraint, not an evolution equation. Pressure is the Lagrange multiplier that enforces it: take the divergence of the first equation, use ∇·u \= 0, and you get a Poisson equation −∆p \= ∇·((u·∇)u) − ∇·f. So p is not an independent unknown. It is determined instantaneously by u, everywhere at once. That non-locality is the first hint that the equations are unusual.  
 

## **2\. Where they come from and where they are used**

The equations were written down by Claude-Louis Navier in 1822 and put on a firm basis by George Stokes in 1845\. They are derived from conservation of mass and momentum for a continuum, plus the assumption that viscous stress is proportional to the rate of strain. Nothing exotic goes in.  
   
They describe almost every fluid you meet: air flowing over a wing, water in a pipe, blood in an artery, weather systems, ocean currents, the coolant in a reactor, the plasma in a star if you add electromagnetism. Engineering runs on numerical approximations to these equations. Every aircraft, every car, every turbine is designed with computational fluid dynamics, which is Navier–Stokes discretised on a grid.  
   
That is the paradox to hold onto. We compute with these equations every day with great success, and yet we do not know whether their solutions always make sense. The open question is not about whether the equations describe fluids. It is about what the equations themselves guarantee. Trefethen puts the engineer's view plainly: well-posedness is normally a housekeeping matter, and the engineers have never been troubled by it.  
 

## **3\. Special cases that are understood**

Before the hard case, it helps to see what is easy.  
   
[**Stokes flow**](https://en.wikipedia.org/wiki/Stokes_flow) **(drop the nonlinear term).** For very slow, very viscous flow, (u·∇)u is negligible and you get ∂u/∂t \= −∇p \+ ν∆u \+ f. This is linear. It is a heat equation with a constraint, and it is completely understood: solutions exist for all time, are unique, and are as smooth as the data. Everything hard is in the term we dropped.  
   
[**Euler equations**](https://en.wikipedia.org/wiki/Euler_equations_\(fluid_dynamics\)) **(drop viscosity).** Set ν \= 0 and you get the inviscid Euler equations of 1757\. These are older and in some ways harder, because there is no smoothing at all. Euler and Navier–Stokes are worked on in parallel, and progress on Euler has repeatedly pointed the way. But the two are not interchangeable: adding even an infinitesimal viscosity changes the character of the equations, since the ν∆u term is the only one that acts more strongly at smaller scales, which is exactly where a singularity would form.  
   
**Compressible inviscid flow (a neighbour that does break).** Drop viscosity and allow density to vary, and smooth solutions really do develop singularities: shock waves. This became urgent with jet aircraft and nuclear explosions after 1945, and the theory of shocks, with its entropy conditions for picking out the physical solution, is a mature field with uniqueness questions still open. It is the nearest example of a fluid model that breaks, and the reason singularity formation in Navier–Stokes is a natural worry rather than a contrived one.  
   
**Two dimensions.** If the flow is confined to a plane, the Navier–Stokes problem is solved: smooth initial data produce a unique smooth solution for all time. The reason is worth understanding, because it shows exactly what goes wrong in three dimensions. Define the vorticity ω \= ∇×u, the local rate of rotation. Taking the curl of the Navier–Stokes equations gives the [vorticity equation](https://en.wikipedia.org/wiki/Vorticity_equation)  
   
**∂ω/∂t \+ (u·∇)ω \= (ω·∇)u \+ ν∆ω**  
   
(taking f \= 0 for the moment). In two dimensions ω is perpendicular to the plane of motion, so (ω·∇)u vanishes identically. Vorticity is simply carried along by the flow and diffused by viscosity. Its maximum can never grow. That single fact controls everything and gives global smoothness.

   
In three dimensions (ω·∇)u does not vanish. This term is called **vortex stretching**. When a vortex tube is aligned with a direction in which the flow is being stretched, the tube gets thinner and, by conservation of angular momentum, spins faster. Stronger vorticity produces stronger straining, which stretches the tube harder. This positive feedback is the physical candidate for singularity formation, and it has no analogue in two dimensions. \[Note A works through the 2D/3D difference in detail.\]  
 

## **4\. What "solved" would mean: existence and smoothness**

Start with smooth initial velocity u₀(x) at time zero, with ∇·u₀ \= 0, decaying fast at infinity so the fluid has finite energy. Does the equation produce a smooth velocity field u(x, t) for all future time? Or can the solution break down, with velocity or its derivatives becoming infinite at some finite time T?  
   
A breakdown of that kind is called a **singularity** or **finite-time blow-up**. It would mean that the equations, applied to perfectly reasonable smooth data, stop making sense as a description after time T. Physically it would mean the continuum model fails on its own terms; some other physics would have to take over at small scales.  
   
What is actually known:

> * **Short-time existence.** From smooth data a unique smooth solution exists for at least a short time. This is standard.  
> * **Leray's weak solutions (1934).** Jean Leray showed that solutions exist for all time if you weaken the notion of solution: they satisfy the equation in an averaged sense and have finite energy, but might not be unique and might not be smooth. Whether Leray's solutions are actually smooth is precisely the open question.  
> * **Energy inequality.** Dot the equation with u and integrate over space. The nonlinear term and the pressure term drop out (this uses ∇·u \= 0). You get d/dt (½∫\|u\|²) \= −ν∫\|∇u\|² \+ ∫f·u. With no forcing, kinetic energy is non-increasing. So energy is under control forever. This is the only globally-in-time estimate anyone has.  
> * **Continuation criteria.** [Beale, Kato and Majda (1984)](https://en.wikipedia.org/wiki/Beale%E2%80%93Kato%E2%80%93Majda_criterion) showed that a smooth solution can be continued past time T provided ∫₀ᵀ ‖ω(·,t)‖∞ dt is finite. In words: blow-up can happen only if the maximum vorticity becomes non-integrable in time. This tells you where to look for a singularity but not whether one exists.

 

## **5\. Why energy is not enough: the scaling argument**

This is the heart of why the problem is hard, and it can be stated in a paragraph.  
   
The Navier–Stokes equations (with f \= 0\) have a scaling symmetry. If u(x, t) is a solution, so is  
   
**uλ(x, t) \= λ u(λx, λ²t)**  
   
for any λ \> 0, with pλ(x, t) \= λ² p(λx, λ²t). Check it: each term in the equation picks up the same factor λ³. Taking λ large zooms in on small scales and short times.  
   
Now ask what the scaling does to the energy. Compute ∫\|uλ\|² dx \= λ² ∫\|u(λx)\|² dx \= λ−1 ∫\|u\|² dy. Energy goes *down* by a factor λ as you zoom in. This means a solution can concentrate a fixed amount of activity into a smaller and smaller region, and the energy bound will not notice; in fact the energy at small scales tends to zero. The quantity we control is **supercritical** with respect to the scaling. It provides no obstruction to a singularity.  
   
The quantities that *would* stop a singularity (critical or subcritical norms, for instance the L³ norm of u, or the L∞ norm of ω integrated in time) are ones we cannot bound globally. The gap between what we can control (energy) and what we would need to control (a scale-invariant quantity) is the whole problem. It is the same structural gap that makes the Yang–Mills mass gap and several other problems hard. \[Note A, part 3, shows the same scaling in 2D, where the exponent is zero and energy is critical.\]  
 

## **6\. The Clay Millennium formulation**

In 2000 the [Clay Mathematics Institute](https://www.claymath.org/millennium/navier-stokes-equation/) listed seven problems with a million-dollar prize each. Navier–Stokes is one. The [offitcial statement](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf) was written by Charles Fefferman and is careful about what counts. There are four ways to win.  
   
The setting is either all of R³ with initial data that decay rapidly at infinity, or a periodic box (the three-torus). Then:  
 

> * **(A)** Prove that for every smooth, divergence-free, rapidly decaying u₀ on R³, with no external force, there is a smooth solution for all time with bounded energy.  
> * **(B)** The same on the periodic box.  
> * **(C)** Disprove (A): exhibit smooth initial data u₀ on R³ and a smooth external force f(x, t), both decaying appropriately, for which no smooth solution with bounded energy exists for all time. That is, exhibit a finite-time blow-up.  
> * **(D)** Disprove (B) on the periodic box, with a smooth periodic force.

 

Three things to notice. First, the "prove" options (A, B) are stated with *no* force, while the "disprove" options (C, D) are allowed a force. Fefferman included the force in C and D to make a counterexample more accessible; the point of a counterexample is to show the equations can break, and a smooth driving force is a legitimate input. Second, the force must be genuinely smooth and satisfy the decay or periodicity conditions. Mathematicians have sometimes used awkward, non-smooth forces to make fluids misbehave; if that were allowed you would just be injecting the singularity by hand, which answers nothing. Third, there is no wall. Fefferman's reason: in a model with a boundary, a singularity may be the fluid interacting with the wall; without one, in his words, it is the fluid doing the crazy stuff.  
   
There is an asymmetry in the meaning of the two outcomes. A proof of A or B says: fluids governed by these equations never break down on their own. A counterexample under C or D says: the equations can be driven to breakdown by a smooth input. The second is a real theorem about the equations, and it rules out any general regularity result that ignores forcing. But it leaves open whether unforced flow, turbulence developing from smooth initial data with f \= 0, ever generates a singularity by itself. Most physicists mean the unforced question when they ask "is Navier–Stokes solved".  
   
**What a blow-up would mean for real fluids.** Not much, and this is agreed on all sides. Real fluids are made of molecules; the continuum assumption that you can zoom in forever fails long before a mathematical singularity would form. A blow-up result therefore has no immediate practical consequence. Its interest is that it is surprising the idealised equations permit it at all: Newton's second law applied to a continuum turns out to have consequences nobody would guess.  
   
Two weeks before the events of Section 8, Lloyd Trefethen posted an [essay](https://arxiv.org/abs/2608.24965) making the same point in a longer frame. The Navier–Stokes problem, like the Riemann Hypothesis and P vs NP, has drifted from a practical challenge to a theoretical one. Twenty-five years of intense work on singularities has made the candidate scenarios look ever more special and ever further from "wet" fluid mechanics; the singularity-forming configurations, if they exist, are probably unstable, so that small perturbations shut them off. He predicts that if blow-up is proved, the next scientific question will not be how to modify the equations but why the singularities have so little consequence. A forced blow-up under option C or D is the most theoretical form this outcome could take. Trefethen described the shape of the result before it was announced.  
 

## **7\. How blow-up proofs are built**

To understand what was reported, you need one more idea: how anyone constructs a singularity for a nonlinear PDE. There are two templates in play, and the September 2026 results come from the second.

   
**Template 1: self-similar blow-up.** Guess that near the singular time T the solution looks like a fixed profile that shrinks and intensifies:  
   
**u(x, t) ≈ (T − t)−α U( x / (T − t)β )**  
   
Substituting this ansatz turns the time-dependent PDE into a stationary problem for the profile U. Then the proof has two parts: (i) find a profile U, and (ii) show that the true solution starting from suitable data stays close to the self-similar solution all the way up to time T, which requires a stability analysis of the linearised operator around U. Part (ii) is usually the hard part. \[Note B walks through the steps and why the naive version fails for Navier–Stokes.\] This is the dominant approach, and since 2013 it has usually been computer-assisted: simulate a candidate scenario, then prove it rigorously by accounting for every numerical error.  
   
**Template 2: the infinite cascade.** Build an infinite sequence of smooth, non-singular solutions, "layers", each driven by a smooth force, at successively smaller scales, and add them up. The sum is a solution whose velocity is unbounded at a finite time. This is analytic, with no computer assistance, and it was developed by Córdoba and Martínez-Zoroa. The catch that stopped it short of the Clay criteria: each layer's force is smooth, but the sum of the forces need not be. \[Note C explains the idea and the catch.\]  
   
The milestones, as the people involved tell it:

> * **Hou and Luo (2013).** Numerical evidence, later made rigorous, that the Euler equations blow up inside a cylinder whose top and bottom halves spin in opposite directions. Córdoba calls this the first serious claim of a singularity. Before it, in his account, nobody believed Navier–Stokes had one.  
> * [Elgindi (2019)](https://arxiv.org/abs/1904.04795) proved finite-time blow-up for 3D Euler with C1,α data (once differentiable, not smooth) and no boundary. Together with Hou–Luo it shifted opinion toward singularities being real, for Euler first and possibly Navier–Stokes.  
> * [Chen and Hou (2022)](https://arxiv.org/abs/2210.07191) gave a computer-assisted proof of the 2013 scenario with smooth data and a boundary.  
> * **Martínez-Zoroa's 2021 thesis and Córdoba–Martínez-Zoroa (2023).** The analytic cascade method, and Euler blow-up with a rough force. An oddball approach in a computer-assisted field.  
> * [Wang et al. (2025)](https://arxiv.org/abs/2509.14185), a Google DeepMind collaboration with Gómez-Serrano, Buckmaster and others, used machine learning to find *unstable* self-similar singularities in fluid models: profiles that exist but that generic data will not follow.

   
The physical picture in all of these is vortex stretching pushed to its limit: a vortex structure that contracts and spins up without bound.  
 

## **8\. The forced route and the Buckmaster–Alpöge ladder**

*Status note for Sections 8, 9 and 11: written on 9 September 2026 from announcements, press coverage and Buckmaster's public statement, all less than two days old. Names, dates and claims here are the participants' own statements, not verified facts, and will change.*  
   
The remaining hurdle in the Córdoba–Martínez-Zoroa program was to make the cascade converge with the total force still smooth. That is the step both AI-assisted teams claim. Charles Fefferman, who wrote the Clay problem, says the heroes of the story are Córdoba and Martínez-Zoroa; Buckmaster's statement says the basic ideas are theirs, that the program was not proposed by a language model, and that in his view Martínez-Zoroa deserves a Fields Medal. Martínez-Zoroa's own reaction: it would have been nice to do it themselves, but he is happy for Buckmaster.  
   
What Tristan Buckmaster (NYU) and Levent Alpöge (a mathematician employed by Anthropic; the collaboration was personal, with no institutional involvement on either side) did was take the program and push it to smooth forcing, up a ladder of increasingly hard models: the incompressible porous media equation, then on 15 August 2026 the Boussinesq equations and the 3D Euler equations, without boundary. The Euler proof was verified in Lean on 22 August. All three results were made public on 8 September, and OpenAI concedes priority on 3D Euler to them.  
   
They also believe they have blow-up for hypo-dissipative Navier–Stokes, a version with weakened viscosity that sits between Euler and the full equations. That paper is unreleased pending Lean verification. Buckmaster says it is suggestive of a path to *unforced* Euler, the harder target.  
   
The work took about a year, most of it slow, with the decisive results arriving in the last month. They used Claude, OpenAI's Codex (with GPT-5.6 Sol) and, for write-ups and auditing, Astra. Buckmaster describes the first LLM-generated Euler proof as the worst he has ever read, and the released Euler write-up as "AI slop" that they had intended to spend weeks cleaning up before the events of Section 11 forced their hand. All of their drafts, for the whole project, were kept in Codex sessions. That detail matters for Section 11\.  
 

## **9\. What OpenAI reported on 8 September 2026**

OpenAI posted a PDF it describes as a 165-page proof, together with a Lean formalisation, on its own website, about twelve hours after Buckmaster's statement. (Buckmaster was told "about 100 pages" on 6 September and has not seen it.) As of 9 September nothing has appeared on arXiv or in a refereed venue, and no outside mathematician has reported completing a review. The theorem, in the form relevant to Clay:  
   
**Theorem 1.1.** For every viscosity ν \> 0, there exists a smooth external force f, compactly supported in space and time, such that the solution starting from rest (u₀ \= 0\) has velocity that becomes unbounded at some finite time T, while the kinetic energy remains bounded for all t \< T.  
**Corollary 10.6.** The periodic version, with periodic force and periodic pressure.  
   
If the argument is correct, this addresses options C and D. It says nothing about A and B; the paper does not claim unforced blow-up. The mechanism is a vortex, set up by a smooth force, that spirals inward and spins up without bound while its energy stays finite; OpenAI's own visualisation shows the rotation speed concentrating at the core. The compactly supported force is what would make it a valid Clay counterexample rather than a trick; whether it meets Fefferman's conditions exactly is the question Section 10 says reviewers must settle. Some experts quoted in coverage regard the forcing option as a loophole in how the problem is usually understood. That is a comment on the problem statement, not on the proof, and it is the point Trefethen made in general terms two weeks earlier (Section 6).  
   
Everything below is OpenAI's own account and has not been independently confirmed. OpenAI states that the effort began on 1 September, prompted by rumours that Buckmaster and Alpöge had solved a Millennium problem; that groups of agents of various sizes, on a new internal model, attacked variants of Euler and Navier–Stokes; that nearly 100 agents working for about 50 hours produced a disproof of Euler regularity (that is, unforced Euler blow-up with smooth data); that roughly 10,000 agents then ran for about 88 hours on Navier–Stokes and produced the proof, with a further 17 hours for another model to formalise it in Lean; that the agents exchanged almost five million messages; and that the total was about 300 billion output tokens. Bubeck's estimate of the cost is several million dollars.  
 

## **10\. What the Lean formalisation does and does not establish**

[Lean](https://en.wikipedia.org/wiki/Lean_\(proof_assistant\)) is a proof assistant. A Lean formalisation means every step of the argument has been checked by machine against the axioms of mathematics, so there are no gaps or errors in the logical chain from the stated hypotheses to the stated conclusion. This is a strong guarantee about internal validity, and it is why the press coverage, Quanta included, is treating the result as essentially established.  
   
It does not verify that the statement proved is the statement Clay asked for. The reviewer's job now is to read the formal theorem and confirm that its hypotheses on the force (smoothness, decay or periodicity, support) and on the solution (bounded energy, smoothness up to time T, genuine unboundedness of velocity) match Fefferman's conditions exactly. This is where any weakness would show, and it is a job for human mathematicians. As of writing, no one outside OpenAI has completed that review, which is why this document says "claimed" where the coverage says "solved". Clay's rules require publication in a refereed venue and a two-year waiting period before a prize is considered.  
   
Buckmaster's statement makes a related point about presentation. He and Alpöge had chosen not to release a Lean certificate alongside an unpolished preprint, on the principle that the first thing anyone reads should be a mathematical argument in the normal form, not a formal certificate. A Lean file is proof that a theorem is true; it is not an explanation of why, and the explanation is what lets other mathematicians build on it. The Clay summary of the problem makes the same point from the other side: why ask for a proof? Because a proof gives not only certitude but understanding.  
 

## **11\. The dispute**

The mathematics above is independent of the following. Buckmaster's account is in his [public statement](https://cims.nyu.edu/~tristanb/statement.pdf); he says explicitly that he is not accusing anyone of anything, only stating what he was told, when, and what was proposed to him. Different parties are giving different versions, and Quanta describes the details as murky.  
   
His account: on 3 September, with a rumour circulating that a major problem had been solved and with Alpöge tipped that information about their work had reached OpenAI, he emailed a mathematician at OpenAI to explain the situation privately. On 6 September, in two calls with that mathematician and Sébastien Bubeck, he was told an internal OpenAI model had proved forced Navier–Stokes blow-up. The initial description was that the model had been given only the problem statement with very little human input; over the course of the call it emerged that a team had been working on it, that the model had first been set on easier problems including Euler, and that large compute had been used. He says it was eventually agreed that OpenAI's first prompt was sent after information about their work had reached OpenAI. He asked whether the model had been trained on their Codex sessions, which held all their drafts, and says he did not get an answer to the training question. He says Bubeck proposed that he publish the Navier–Stokes result as sole author, crediting an OpenAI model, with Alpöge removed from authorship, and that when he said he would go public, Bubeck replied "Why would you ruin your career?" and later "If you don't want me to be nice, then I don't have to be nice."  
   
Bubeck has called the allegations circulating online false and inflammatory. OpenAI states that neither its researchers nor its agents saw the Buckmaster–Alpöge work before it was public, that no specific user data was accessed, that it cannot rule out that de-identified usage data improved its models, and that the proofs differ significantly. It concedes priority on 3D Euler and claims it for Navier–Stokes. None of this bears on whether Theorem 1.1 is correct. It bears on credit and provenance, and it will look different once the proof is reviewed and the records are examined. The one credit question already settled by everyone involved is the debt to Córdoba and Martínez-Zoroa.  
 

## **12\. Two readings of the same event**

Buckmaster had planned to say, on announcing the work, that the results are not the important thing. The important thing is that a mathematician and a language model did in a month what would previously have been a career's work, and produced proofs that the human collaborator initially could not read. He calls it a Deep Blue–Kasparov moment for mathematics, with consequences for how students are trained, how credit is assigned, how refereeing works, and what is worth one human life's attention. He argues the community needs an unhurried discussion about this, and that the dispute has displaced it. Whether or not the OpenAI proof survives review, the Euler and Boussinesq results are already Lean-verified, and that argument stands on them alone. Córdoba's joke, "I don't use AI: I have Luis", and Martínez-Zoroa's "I'll have to adapt, clearly", are the same moment seen from the people whose ideas were pushed to completion by someone else's machine.  
   
Trefethen's essay, written before any of this, offers the complementary reading. His claim is that the problem itself had become more theoretical than when it was posed: a resolution would be historic for the surrounding theory but would not touch the fluid mechanics engineers use. Put the two together and the September 2026 announcements change who does mathematics far more than they change what we know about fluids. The forced blow-up, if it holds, is a striking theorem about the Navier–Stokes equations and a non-event for the Navier–Stokes fluid. Trefethen's closing speculation is worth keeping in view: problems that resist solution for a century may do so precisely because they lack measurable consequences to grab hold of, and glide through both theory and practice like neutrinos. The unforced problem, options A and B, is still such a problem.  
 

## **13\. Summary**

> * Navier–Stokes is Newton's law for a viscous incompressible fluid. Its only hard term is the quadratic advection (u·∇)u, which in 3D produces vortex stretching.  
> * Two-dimensional flow is understood; three-dimensional flow is not, because the one global estimate available (energy) is supercritical and cannot see small scales.  
> * The Clay problem offers four routes: prove global smoothness without forcing (A, B) or exhibit blow-up, optionally with a smooth force (C, D), in either case with no wall.  
> * Two proof templates: self-similar profile plus stability (Hou–Luo, Elgindi, Chen–Hou, usually computer-assisted) and the analytic infinite cascade (Córdoba–Martínez-Zoroa). Known candidate singularities are contrived and probably unstable, which is why they are not expected in real flows.  
> * The cascade method produced forced blow-up with a rough total force; the missing step was keeping the total force smooth. Buckmaster and Alpöge did that for Euler, Lean-verified on 22 August 2026, with hypo-dissipative Navier–Stokes pending; OpenAI concedes them Euler priority.  
> * OpenAI posted, on its own site, a machine-checked proof of forced Navier–Stokes blow-up with compactly supported smooth force for every viscosity: an answer to C and D if it survives review, which has not started.  
> * The unforced question, A and B, is untouched. The physically deepest version of the problem remains open, and in Trefethen's argument it is also the version with the least practical consequence.  
> * Everyone involved, including Fefferman, credits the underlying ideas to Córdoba and Martínez-Zoroa. Verification by outside mathematicians and by Clay is pending; a dispute over provenance is unresolved. Sections 8, 9 and 11 are dated 9 September 2026 and will need revising.

 

# **Notes**

## **Note A. Why three dimensions is so much harder than two**

The whole difference is one term in the vorticity equation of Section 3\.  
   
**1\. The 2D collapse.** In 2D, u \= (u₁, u₂, 0\) depends only on (x, y), so ω \= (0, 0, ω₃). Then (ω·∇)u \= ω₃ ∂u/∂z \= 0, because nothing depends on z. The vorticity equation collapses to  
   
**Dω/Dt \= ν∆ω**  
   
where D/Dt \= ∂/∂t \+ u·∇ is the derivative following a fluid parcel. That is a scalar advection–diffusion equation. Its solutions obey a maximum principle: each parcel's vorticity can only be smoothed toward its neighbours, never amplified. So ‖ω(t)‖∞ ≤ ‖ω₀‖∞ for all time, for free. Beale–Kato–Majda then says the solution stays smooth forever. Even Euler (ν \= 0\) is fine in 2D: vorticity is exactly conserved along particle paths, so every Lp norm of ω is conserved. There are infinitely many conserved quantities, which is why 2D turbulence behaves so differently from 3D (energy cascades to *large* scales rather than small).  
   
**2\. The 3D feedback loop.** In 3D, (ω·∇)u is generically nonzero. Decompose the velocity gradient ∇u into its symmetric part S (the strain-rate tensor) and its antisymmetric part, which is just ω in disguise. The antisymmetric part contributes nothing to (ω·∇)u, so  
   
**Dω/Dt \= Sω \+ ν∆ω**  
 

Vorticity is a vector being multiplied by the strain matrix. If ω is aligned with an eigenvector of S with positive eigenvalue λ, then \|ω\| grows like eλt along the parcel. Physically: a vortex tube in a stretching flow gets thinner and, by angular momentum conservation, spins faster. There is no maximum principle for a vector equation with a source term like this.  
   
Now the feedback. S is not independent of ω. Since ∇·u \= 0, u is recovered from ω by the [Biot–Savart law](https://en.wikipedia.org/wiki/Biot%E2%80%93Savart_law) (identical in form to magnetostatics): u \= ∇×ψ where ∆ψ \= −ω. So S is a singular integral of ω, roughly the same size as ω. That gives, heuristically,  
   
**d\|ω\|/dt \~ \|ω\|²**  
   
which blows up in finite time: \|ω\| \~ 1/(T − t). Whether the real dynamics achieve this, or whether geometry (misalignment between ω and the stretching direction) and viscosity always defeat it, is the open question. A result of Constantin and Fefferman says blow-up requires the *direction* of ω to vary wildly near the singularity, which is a hint about what the geometry must look like, but not a proof either way.  
   
**3\. Two more ways of seeing the same thing.**  
   
*Dimension counting.* Vorticity is a 2-form; in n dimensions it has n(n−1)/2 components. In 2D that is one scalar, conserved along flow lines. In 3D it is three components, transformed by the Jacobian of the flow map, and Jacobians of volume-preserving maps can have arbitrarily large eigenvalues.  
   
*Scaling.* Under u → λu(λx, λ²t), the energy ∫\|u\|² scales like λ2−n. In 2D that exponent is 0: energy is scale-invariant (critical) and controls all scales. In 3D it is −1: supercritical, controlling nothing small. The quantity you would like to control in 3D is enstrophy ∫\|ω\|², which is conserved in 2D but can be pumped in 3D by the vortex-stretching term ∫ω·Sω.  
   
So: 2D has no stretching, a maximum principle, and a critical energy. 3D has all three failures at once, and they are the same failure seen three ways.  
 

## **Note B. Self-similar blow-up, step by step**

This is Template 1 of Section 7\. The idea in one line: guess that near the singularity the solution is a fixed shape that shrinks and intensifies, find the shape, then prove the real solution sticks to it.  
   
**Step 1\. The ansatz.** Suppose blow-up happens at time T at the origin, and write τ \= T − t. Guess  
   
**u(x, t) \= τ−α U(x / τβ)**  
   
As τ → 0 the profile U is evaluated on an ever smaller ball (scale τβ) with ever larger amplitude (τ−α). Substitute into the equation and demand that the τ-dependence cancel. For Euler, ∂ₜu \~ τ−α−1 and (u·∇)u \~ τ−2α−β, so you need α \+ 1 \= 2α \+ β, i.e. α \+ β \= 1\. One free parameter remains; that is typical and important below. For Navier–Stokes the viscous term ν∆u \~ τ−α−2β additionally forces α \= β, hence α \= β \= ½: the same exponents as the scaling symmetry of Section 5\.  
   
**Step 2\. The profile equation.** With the τ-dependence cancelled you get a stationary PDE for U in the similarity variable y \= x / τβ. For Navier–Stokes (ν \= 1 after rescaling):  
   
**αU \+ β(y·∇)U \+ (U·∇)U \= −∇P \+ ∆U**  
   
The terms αU \+ β(y·∇)U are new. They come from the chain rule: as τ shrinks, a point at fixed x moves outward in y-coordinates, so in the profile frame there is an outward drift and a damping. Solving this for a nontrivial, decaying, divergence-free U is the first half of a blow-up proof.  
   
For Navier–Stokes this exact form is dead: Nečas, Růžička and Šverák (1996) proved that any such U with finite energy is zero. Exactly self-similar blow-up of the Leray type cannot happen. That is why the successful constructions are not exactly self-similar but *approximately* so, or use exponents that only Euler allows, or abandon the template altogether (Note C).  
   
**Step 3\. Why Euler is easier here.** With α \+ β \= 1 free, Euler admits a whole family of scalings, and the profile equation is first-order in U (no Laplacian). Elgindi's 2019 proof worked in axisymmetric flow without swirl, where vorticity reduces to a scalar and the profile equation reduces to something you can attack with explicit functions. The catch: the profile he found has only C1,α regularity at the axis, not smoothness. Smooth data is exactly what the Clay problem demands, and it is harder because smooth flows must satisfy extra Taylor-expansion constraints at the singular point.  
   
**Step 4\. Stability, which is where the pages go.** Finding U proves nothing on its own. You need: if the actual initial data is close to the profile (in similarity variables), the solution stays close to the profile up to time T. Write u \= τ−α(U \+ ε)(y, s), where s \= −log τ is the natural time in the shrinking frame (s → ∞ as t → T). The error satisfies  
   
**∂sε \= Lε \+ N(ε)**  
   
with L the linearisation of the profile equation around U and N quadratic. The dynamics in s run forever, so you need L to be dissipative: spectrum in the left half-plane, up to a finite number of unstable directions. A nonlinear stability argument, essentially a fixed-point theorem in a weighted space, then shows ε stays small for all s, so the solution really does blow up like the profile.  
   
Handling the unstable directions of L is the technical core. Each corresponds to a way the solution could slide off the self-similar path, for instance a shift in the blow-up time or point. You kill them by adjusting finitely many parameters in the initial data (a "modulation" or shooting argument). The Chen–Hou proof is computer-assisted because the spectral gap of L is verified numerically with rigorous interval-arithmetic bounds rather than by hand. An *unstable* singularity, in the sense of Wang et al. (Section 7), is one where L has many unstable directions: the profile is a genuine solution, but only data tuned to lie on a thin manifold will follow it, and generic perturbations escape. This is the technical content of Trefethen's remark that singularity-forming configurations are probably unstable and therefore of little consequence for real flows.  
   
**Step 5\. What the final theorem says.** Data u₀ \= U(x), and a solution with ‖u(t)‖∞ \~ (T − t)−α → ∞ while ∫\|u\|² stays bounded. Unbounded velocity with finite energy is what makes it a genuine singularity rather than energy escaping to infinity.  
   
That is the template: pick exponents, find a profile, linearise, prove a spectral gap, close the nonlinear estimate. The differences between papers are in which symmetry reduction makes the profile findable and how the unstable modes are handled.  
 

## **Note C. The infinite cascade and the smooth-force hurdle**

This is Template 2 of Section 7, the Córdoba–Martínez-Zoroa construction that the September 2026 results complete. The description here is at the level of the public accounts; the papers themselves are the source for anything more precise.  
   
**The idea.** Instead of one profile that shrinks, build a sequence of solutions u₁, u₂, u₃, … at successively smaller spatial scales and shorter time scales. Each un is smooth and non-singular on its own, and each is driven by its own smooth force fn. Arrange the scales so that the sequence is summable in the energy norm but the n-th layer contributes a velocity of order 1 (or growing) at the n-th scale. The sum u \= Σ un then has bounded energy but unbounded velocity as the layers pile up at a point in space-time. Martínez-Zoroa calls this an infinite cascade; the picture is the same energy cascade to small scales that Section 5 said the energy bound cannot see, but constructed by hand, layer by layer, rather than left to the nonlinearity.  
   
**Why a force is natural here.** The layers interact through the nonlinear term (u·∇)u: the cross terms um·∇un are not zero. Rather than fight them, the method absorbs them into the forces: choose fn so that each layer, in the presence of the others, still solves the equation. This is why the construction works with a force and has no unforced version yet. Note also that the argument is entirely analytic. Each layer is explicit enough to estimate by hand, so there is no computer-assisted spectral bound as in Note B, Step 4\.

   
**The catch.** Each fn is smooth, but the total force F \= Σ fn is a sum over infinitely many scales, and the derivatives of fn grow with n. F can be bounded and still fail to be smooth, in the way that Σ 2−n sin(4nx) is bounded and continuous but nowhere differentiable. Córdoba–Martínez-Zoroa's 2023 Euler result has exactly this character: forced blow-up with a force that is "messy", in Quanta's word, and so falls short of Fefferman's option C, which demands a smooth F.  
   
**The hurdle both AI teams claim to have cleared.** Redesign the cascade so that F is smooth: make the layer forces decay fast enough in every derivative, while the layer velocities still pile up to a singularity. The difficulty is that these two demands pull against each other, since the forces are what hold the layers together against the cross terms, and a weak force means weak control. According to the public accounts, this is the step Buckmaster and Alpöge achieved for IPM, Boussinesq and Euler with LLM assistance, and the step OpenAI's agents achieved for full Navier–Stokes. In Navier–Stokes the viscous term is an extra headwind: it damps the small layers, which is why the viscous case sits above Euler on the ladder and why the intermediate hypo-dissipative case (weaker viscosity) came first for Buckmaster and Alpöge.  
   
**Why it says little about unforced flow.** The forces do the structural work of the construction. Remove them and the layers no longer solve the equation; the cascade has to be generated by the nonlinearity itself, which is the original problem. So the forced result should be read as: the equations admit a smooth-forced cascade to a singularity. Whether they generate such a cascade unaided is options A and B, untouched.  
 

## **Timeline (from Buckmaster's statement, OpenAI's post, Quanta and arXiv)**

> * 2013: Hou–Luo, numerical Euler blow-up in a counter-rotating cylinder.  
> * 2019: Elgindi, Euler blow-up with C1,α data, no boundary.  
> * 2021: Martínez-Zoroa's thesis, analytic cascade methods.  
> * 2022: Chen–Hou, computer-assisted proof of the 2013 scenario.  
> * 2023: Córdoba–Martínez-Zoroa, Euler blow-up with a rough force.  
> * \~Sept 2025 – Aug 2026: Buckmaster–Alpöge work, mostly slow; IPM result first.  
> * 15 Aug 2026: Boussinesq and Euler blow-up with smooth forcing obtained.  
> * 22 Aug 2026: Euler proof verified in Lean.  
> * 25 Aug 2026: Trefethen's "Reflections on the Millennium Problems" posted to arXiv.  
> * 1 Sept 2026: OpenAI's stated start date for its effort.  
> * 2–3 Sept 2026: rumour reaches Buckmaster; he emails OpenAI privately.  
> * 6 Sept 2026: two calls with OpenAI (Bubeck present); proposals made and declined.  
> * 7 Sept 2026, just before midnight: Buckmaster–Alpöge papers and Buckmaster's statement released.  
> * 8 Sept 2026, morning: OpenAI posts its Navier–Stokes claim, about twelve hours later.

 

## **Links**

> * Buckmaster's statement (primary source for Sections 8, 11, 12): [cims.nyu.edu/\~tristanb/statement.pdf](https://cims.nyu.edu/~tristanb/statement.pdf)  
> * Quanta, with Fefferman, Córdoba and Martínez-Zoroa quotes (Sections 7, 8, Note C): [quantamagazine.org/ai-has-solved-one-of-maths-1-million-millennium-prize-problems-20260908](https://www.quantamagazine.org/ai-has-solved-one-of-maths-1-million-millennium-prize-problems-20260908/)  
> * Trefethen, Reflections on the Millennium Problems (Sections 2, 6, 12): [arxiv.org/abs/2608.24965](https://arxiv.org/abs/2608.24965)  
> * Clay problem page: [claymath.org/millennium/navier-stokes-equation](https://www.claymath.org/millennium/navier-stokes-equation/)  
> * Fefferman's official statement (PDF): [claymath.org/wp-content/uploads/2022/06/navierstokes.pdf](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf)  
> * OpenAI announcement: [openai.com/index/navier-stokes-solution](https://openai.com/index/navier-stokes-solution/)  
> * TechCrunch on the dispute: [techcrunch.com/2026/09/08/…](https://techcrunch.com/2026/09/08/openai-fought-dirty-on-career-making-math-problem-says-nyu-mathematician/)  
> * Scientific American on the announcement and dispute: [scientificamerican.com/article/ai-may-have-just-solved…](https://www.scientificamerican.com/article/ai-may-have-just-solved-a-million-dollar-math-problem-the-field-will-never-be-the-same/)  
> * Elgindi, Euler blow-up with C1,α data: [arxiv.org/abs/1904.04795](https://arxiv.org/abs/1904.04795)  
> * Chen & Hou, computer-assisted Euler blow-up with boundary: [arxiv.org/abs/2210.07191](https://arxiv.org/abs/2210.07191)  
> * Wang et al., Discovery of unstable singularities: [arxiv.org/abs/2509.14185](https://arxiv.org/abs/2509.14185)  
> * Background: [Navier–Stokes existence and smoothness](https://en.wikipedia.org/wiki/Navier%E2%80%93Stokes_existence_and_smoothness), [vorticity equation](https://en.wikipedia.org/wiki/Vorticity_equation), [Beale–Kato–Majda criterion](https://en.wikipedia.org/wiki/Beale%E2%80%93Kato%E2%80%93Majda_criterion)

>   
>   
>   
>   
> 