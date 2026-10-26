# **Classification without human checking: what I am learning**

25 October 2026\. Working notes. Earlier pieces: [Document classification: a short introduction](https://docs.google.com/document/d/1vRxDLM1KMRF5rUioUJEHoAgkwX1ad_fwSKfOy9vFr2s/edit) and [Automatic Document Sorting Without Human Review](https://docs.google.com/document/d/1s0EyWWu1uj-GxLMvdLDvcTI2m_rhIM9FnChefNQonTs/edit).

## **The business problem**

An organisation pays people to look at documents: to sort incoming pages into the right folder, to read a contract for the clauses that matter, to check a form. The only way a classifier reduces that cost is if some of its answers are used without a person checking them. An answer a person has to check anyway saves nothing; the person still reads the document.

So the question is not "how accurate is the classifier?" It is: "How many answers can we use without checking before the error rate passes human levels?" A careful person gets 2% to 5% of answers wrong. We call the share of unchecked answers **coverage**, and we measure coverage at that fixed error ceiling.

The classifier scores every answer. Using a separate calibration set, we pick a score cut-off that keeps the error rate on answers above it under our limit. We then apply that cut-off to the test documents in a single pass. Every result in these notes reports coverage at a 5% or 2% error limit, measured this way.

## **What the first application taught: sorting pages into types**

The first application ([layout-classify](https://www.google.com/search?q=https://github.com/peterwilliams97/layout-classify)) labelled the first page of a PDF with one of 11 document types, or "none". In practice: a document arrives by scanner or email, the classifier names its type, and if the score clears the cut-off, the system files it automatically.

> * A decision model given one sentence per type and no labelled pages filed 74.5% of test pages at 5% error and 61% at 2%. The most possible was 75%, because a quarter of the test pages fit no type.  
> * The best classifier trained on 411 labelled pages filed 50% at 5% and 33% at 2%.  
> * Accuracy and coverage pick different winners. Models that were 97% to 98% accurate filed little or nothing, because their wrong answers scored as high as their right ones.  
> * Pages that fit no type cost twice: they cannot be filed, and keeping them out raises the cut-off for everything else. Letting the classifier say "none" recovered coverage.  
> * The calibration set has to be a few hundred pages. On 141 pages the cut-off swung with the draw; on 549 it settled.

The lesson I took from it: when the document types are familiar and fixed, a language model already recognises them. One sentence per type is enough to define them, and a model with zero labelled pages beat a classifier trained on 411\.

## **Second application: contract review**

A lawyer reviewing a commercial contract asks the same questions of each one: is there a non-compete, a cap on liability, a change-of-control clause, an auto-renewal? Those questions already exist as a dataset, CUAD (Contract Understanding Atticus Dataset): 510 contracts from SEC filings, labelled by law students trained by attorneys for 41 clause categories. The business version: a classifier answers each question for each contract; above the cut-off the answer is used and nobody reads the contract for that question; below it a person does.

CUAD stands in for the list an in-house team keeps for its own contracts; the method is the same.

The shape is different from page sorting:

> * One yes/no classifier per question, 39 of them (two questions are positive in every contract and are left out), instead of one choice among 11 types.  
> * The unit is the whole contract, often 40 pages, and the clause that answers a question is a paragraph or two of it.  
> * Most questions are rare: for 23 of the 39, fewer than a third of contracts have the clause. Answering "no" to everything is 80% to 98% accurate on those.

>   
That last point changes the measurement. A constant "no" passes a 10% error limit on seven questions without reading anything. So coverage is reported **above the constant-answer floor**: the coverage a classifier gets beyond what answering the train majority gets at the same error rate. The repo is [contract-check](https://github.com/peterwilliams97/contract-check); the split is 153 train, 153 validation, 204 test contracts.

### **First results**

Mean over 39 questions of test coverage above the [constant-answer floor,](#bookmark=id.frtkfywx2sqd) cut-offs fitted on validation.

| Model | Trained on | Above constant, 2% error | Above constant, 5% error |
| :---- | :---- | :---- | :---- |
| constant | train majority answer per question; no text | 0.00 | 0.00 |
| TF-IDF \+ LR, whole contract | 153 contracts | 0.02 | 0.30 |
| TF-IDF \+ LR, paragraphs | 153 contracts, paragraph positive where it overlaps a labelled span | 0.05 | 0.35 |
| gemma3:4b via Ollama, 5 retrieved paragraphs per question | nothing | 0.00 | 0.03 |

### **What it has taught so far**

> * **The zero-label result did not transfer.** The local model with no labels was 58% accurate on questions where "no" everywhere gets about 80%, and covered a tenth of what the trained paragraph model covered. Shown five paragraphs that look relevant to a question, a 4B model says the clause is there. Whether the fault is the retrieval (the right paragraph is not among the five) or the model (it is, and the model still says yes) is the next measurement.  
> * **Rare positives make "no" cheap.** Without the [constant-answer floor,](#bookmark=id.frtkfywx2sqd) the whole-contract TF-IDF model showed 30% coverage at 5% error, and most of it was confident "no" answers on questions where the model had never once said "yes". The floor has to be part of the measurement, not a footnote.  
> * **Paragraph-level training helps a little, and its scores are worse.** Taking the maximum over 70 paragraph probabilities pushes "yes" scores up and "no" scores down, so five questions breached the 5% limit on test. The gain over whole-contract TF-IDF is within calibration noise.  
> * **At 2% error nothing works yet.** Every model is near zero. For page sorting, the zero-label model reached 61% at 2%.  
> * **Few test positives, coarse answers.** Five questions have ten or fewer positive test contracts; their coverage numbers cannot tell a classifier from a constant answer.  
> * **A second dataset shows the same pattern.** ContractNLI tests 607 NDAs against 17 standard statements, each marked as true, false, or not mentioned. Whole-contract TF-IDF, trained on 484 contracts, covers 20% above the [constant-answer floor](#bookmark=id.frtkfywx2sqd) at 5% error and 2% at 2%. The dataset's 61-contract validation split is too small to set a reliable cut-off, confirming the [calibration lesson](https://www.google.com/search?q=%3Ftab%3Dt.0%23bookmark%3Did.roe3waawyrfh) from page sorting.

## **What is the same across both**

> * The measure is coverage at a bounded error rate, set on calibration data and read once on test. Accuracy is not the measure.  
> * What decides coverage is whether wrong answers score lower than right ones, not how many answers are right.  
> * Something has to stand in for "the easy answer": "none" for page sorting, the [constant-answer floor](#bookmark=id.frtkfywx2sqd) for yes/no questions. Without it the headline number is inflated.  
> * Calibration needs hundreds of examples per decision. Contract-check has 153 validation contracts per question, which is at the low end.

## **Next**

> * Measure whether the five retrieved paragraphs contain the labelled clause (recall at 5), and the local model's accuracy when they do.  
> * Depending on that, fix retrieval or try a larger local model on validation only.  
> * Decide which of the 41 questions matter for the contract type a reader would actually check (sale and supply agreements), with a lawyer, and report those first.  
> * The business version of this is review against a contract playbook: an in-house legal team’s list of clauses, the positions it accepts, and the fallbacks. CUAD’s 41 questions are a public stand-in for such a playbook. The next dataset should be a real playbook and the contracts it is applied to, where the positive rate per question is high enough that the constant floor is not most of the answer. 