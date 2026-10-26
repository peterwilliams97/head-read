# **Capability Is Not Value**

Evaluating an AI tool before measuring how well it works

*New technologies can do to normally careful programmers what a hot tip does to a retail investor: we can forget our normal caution and think only about the upside. AI is the current hot new technology, and developers have turned out to be as susceptible as anyone: adopting a tool on the strength of a demo, a benchmark, or a vendor's figure. The correction for this is prosaic: the plainest rule in investing, that Warren Buffett repeats ad nauseam. You come out ahead only on the net, after the alternative you'd have used anyway, after the hours spent checking the tool's work, after every cost the demo left out. Which is precisely why it was skipped in the excitement. This article is about how to curb your enthusiasm about AI and use as you would any other tool.*

`Adam Smith watched the most productive workshop of his age and did not mistake its motion for its worth. The discipline here is his: admire the machine, then ask what it nets.`

Most evaluation of an AI tool measures how well it performs the task — accuracy, completion rate, win-rate against a benchmark. That measurement is useful, but it answers the second question while skipping the first. It assumes the tool is worth using and asks only how good it is. The prior question is whether the tool adds anything net: whether, once you account for what you would otherwise do and what the tool costs in practice, you are better off with it than without it.

The distinction matters because a model's raw capability and its net contribution to a system are different quantities, and the distance between them is where engineering time and budgets quietly disappear. A tool can be impressive in isolation and worth nothing in place.

## The perception gap

This can't be settled by how the tool feels to use. In a 2025 randomised controlled trial, METR had experienced developers complete real tasks on codebases they knew well, with and without AI assistance. The developers estimated the AI had made them about 20 percent faster. Measured against their own unaided runs, they were about 19 percent slower. The people doing the work were wrong about the sign of the effect, not merely its size.

The conclusion is not that the tools are useless; the study's authors are careful to say otherwise. It is narrower and more durable: the sense that a tool is powerful is not evidence that it adds value. Enthusiasm — from a developer, a manager, or a vendor — marks a place to begin measuring. It is never itself a measurement. The questions that follow are built to take external evidence as their input rather than that feeling.

`Two figures stand at the start of this. The first is Smith in his workshop, refusing to be dazzled by the cleverest machine of his century until he had asked what it actually produced. The second is a farmer's son on a rise above his valley, looking not at one future but at all of them at once — the farm behind him, the workshop in the town, the chimneys beyond it, the college on the far hill — and choosing among them on their merits, each measured against the others rather than against nothing. Adopt both postures and the rest follows. Do not value a tool by how powerful it feels; value it the way the son values a life, against the concrete alternative you would otherwise have chosen. The four questions below are only that comparison, made explicit.`

## Four questions that separate the two

Four checks tend to separate tools that net positive from tools that merely perform well. They predate machine learning — they come from decision analysis, causal inference, evidence-based medicine, and operations research — and each catches a different way that capability fails to convert into value. A tool that cannot answer all four usually is not worth integrating.

**The baseline.** The most common error in evaluating an AI tool is comparing it against doing nothing. Net value is defined relative to the best alternative actually available, which is rarely zero and often unglamorous: a regular expression, a database query, a template, an hour of someone's afternoon. A tool that reaches 95 percent accuracy adds nothing if the boring alternative reaches 95 percent for less. The real question is not whether it works but whether it beats the specific thing you would otherwise use, named and costed. If the comparison is against nothing, there is no measurement.

`A farmer's son weighing the lives open to him — the farm, the trade, the factory town, the college on the hill. He is not asking whether any one of them is good. He is asking which is best for him, net of the rest. That is the whole of evaluation`.

**The bottleneck.** Improving a step helps the whole only if that step was the constraint. This is Amdahl's law restated as advice: if a stage accounts for five percent of the time or cost, automating it perfectly caps the gain at five percent, and integration usually consumes most of that. Tools optimise non-constraints by default, because the steps easiest to automate are often not the ones that were slow. Strength applied off the critical path produces a convincing demo and no movement in the outcome anyone is paid for.

**The decision.** Information has value only when it changes what happens next. Before building or buying, it is worth naming the decision the output would alter:  the branch the system takes, the action a person performs differently. If the same next step follows whether the output is good or bad, the output is inert, and the tool producing it usually is too. This is the check that makes "don't bother" a rigorous answer rather than a lazy one.

**The full cost.** Vendor benchmarks report success with the failures removed. Real cost includes the failures: the runs abandoned and redone by hand, the drift, and above all the time spent verifying output. Much of the slowdown in the METR trial came from exactly this — developers checking work the AI had produced. A deterministic process that needs no review is frequently cheaper in total than a cleverer one whose output a human must audit one time in five. The honest figure is the whole distribution, not the part that went well, and in practice it tends to run several times the sticker price once verification, monitoring, and correction are included.

## When the request arrives pre-sold

Much of the difficulty in practice is that the person asking for the tool has already been sold on it, often by marketing they have not checked. That is not a problem to argue away; it is a condition to plan around, and the same four questions work as a filter on incoming requests as well as on one's own ideas.

A request with no decision behind it — where the person cannot say what they would do differently once the tool works — becomes a moving target that never resolves, and it is cheaper to surface that at the start than after months of work. A request whose honest baseline is the existing spreadsheet or team is worth naming as zero-yield before any code is written, even at the cost of the engagement. Requests tend to point at the visible, high-status use case, while the returns in the published data sit in the unglamorous work nearer the actual cost centre. And because real costs run well above the estimate, work is safer structured so that failure appears in weeks rather than after a year of demos that looked like progress.

## What the evidence currently says

The figures below are useful less as an argument against AI than as a correction to the assumption that adoption alone produces returns.

MIT NANDA's [*State of AI in Business 2025*](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) found that roughly 95 percent of enterprise generative-AI pilots produced no measurable effect on profit and loss, with the strongest returns in back-office automation and externally built tools succeeding about twice as often as internal ones. [BCG's 2026 executive survey](https://www.bcg.com/publications/2026/as-ai-investments-surge-ceos-take-the-lead) found about 26 percent of companies reporting meaningful financial value from AI. Gartner has projected that around 30 percent of generative-AI projects begun in 2024 will be abandoned by the end of 2026\. IBM's CEO study found roughly one initiative in four meeting its expected return. Running through these is a recurring operational point: results can resemble success for as long as eighteen months before the absence of value becomes visible, and total cost commonly runs two to four times the headline once verification and governance are counted.

The counterweight belongs here too. The same surveys record large and growing spend and a real minority of projects that succeed. The purpose of the four questions is not to conclude that AI does not work. It is that the gap between what a tool can do and what it adds is wide, predictable, and the place where evaluation actually happens.  
