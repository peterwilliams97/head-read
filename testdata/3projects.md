# **Local document AI: three projects**

Oct 22, 2026 · @Peter Williams

Three projects that take the method in [Automatic Document Sorting Without Human Review](https://docs.google.com/document/d/1s0EyWWu1uj-GxLMvdLDvcTI2m_rhIM9FnChefNQonTs/edit) to the three insurance document jobs: claims intake, submissions, certificates. Each runs on a local GPU with no cloud service and reports one number: the share of work done with no human check at a fixed error bound.

# **Common ground**

Every project uses the same measurement rule as the sorting write-up, so results are comparable and nobody argues about what "works" means.

* **One output, one score.** The model gives an answer (a type, a page boundary, a field value) and a probability in \[0, 1\].  
* **One rule for accepting it.** Rank calibration pages by score; the cut-off is the lowest score whose one-sided 90% Clopper-Pearson upper bound on error is at or below 2% (5% also reported). That needs 114 consecutive correct answers at the top of the ranking for 2%, 45 for 5%.  
* **One number reported.** Coverage: the share of answers above the cut-off. Error on those answers is checked on a held-out test set and must stay under the bound.  
* **Three splits.** Train / validation / test, disjoint by source document. Cut-offs are set on train \+ validation, never on test.  
* **Out-of-scope input is in the test set.** About a tenth of pages fit no target type. Accepting one is an error.  
* **Hardware stated.** Model, quantisation, GPU, median seconds per page, OCR time separate.

Starting tooling is the [layout-classify](https://github.com/peterwilliams97/layout-classify) repo (Python, MIT): rendering at 200 dpi, Tesseract OCR cache, the calibration code, and the d3-flash prompt with one definition per type. d3-flash (Decision 3.0, 8B) is the model to start with because its scores were calibrated in the sorting experiment; any local model that returns a probability can be swapped in. Models that return no probability (gemma4 via Ollama) cannot be used for automatic acceptance and are run only as an accuracy comparison.

# **Project 1: split a claims packet and label each document**

**Aim.** A claim arrives as one PDF holding several documents: a loss notice, photos, a repair estimate, a police report, medical bills. Output the page ranges of each document and a type for each, with no human check on the ones that clear the cut-off.

**Input.** A multi-page PDF, born-digital or scanned at 150 dpi or higher.

**Output.** A list of (first page, last page, type, score). Types to start with: loss notice, photo, estimate, police report, medical bill, correspondence, none.

**Method.** Two decisions per page, each with its own score and cut-off:

1. **Boundary.** Is this page the first page of a new document? Input is the OCR text of this page and the previous page (first 150 words of each). This is a yes/no decision model call.  
2. **Type.** Which type is the document that starts here? Same call shape as the sorting write-up: one-sentence definition per type, first 150 words of the document.

A packet is accepted whole only if every boundary and type decision in it clears its cut-off; otherwise the whole packet goes to a person, since a wrong split corrupts every label after it.

**What is measured.**

* Coverage of packets accepted whole at 2% and 5% error, where an error is any wrong boundary or wrong type in an accepted packet.  
* Per-page boundary coverage and type coverage separately, so it is clear which decision limits the packet number.  
* Seconds per page.

**Questions the result answers.**

1. What share of packets need no human check?  
2. Is the boundary decision or the type decision the limit?  
3. Does giving the model both pages' text beat giving it only the current page?

**Done when.** A results table with one row per model variant and the columns above, on a test set of at least 100 packets, with the test set never used to set cut-offs or write definitions.

# **Project 2: sort submission attachments and read application fields**

**Aim.** A broker's email carries an application form (ACORD 125 or 140), a statement of values, supplementals and loss runs from several carriers. Label each attachment by type, then read the named fields off the application form, with no human check on labels and fields that clear the cut-off.

This is the front half of the submissions job. The back half — merging several carriers' loss runs into one claims history and checking them against the application — is left out until the front half has a number.

**Input.** The attachments of one email: PDFs, sometimes spreadsheets.

**Output.**

1. Per attachment: (type, score). Types: application, statement of values, supplemental, loss run, correspondence, none.  
2. Per application form: a fixed list of fields, each (value, score). Start with ten: applicant name, mailing address, policy effective date, policy expiration date, business description, annual revenue, number of employees, prior carrier, prior premium, requested limits.

**Method.**

* Attachment type: the sorting write-up's method unchanged, with new definitions.  
* Field reading: one decision-model call per field, given the OCR text of the form with word positions and the question "what is the value of \<field\>?" The model returns the value and a probability that it is correct. Fixed-layout forms make this easier than free text: the field label is always present and in the same place.

**What is measured.**

* Attachment-type coverage at 2% and 5%.  
* Per-field coverage at 2% and 5%, where an error is a value that does not match the hand-checked value after normalising whitespace, case and date format.  
* Form coverage: share of forms where all ten fields clear the cut-off.  
* Seconds per form.

**Questions the result answers.**

1. What share of forms need no human check on any field?  
2. Which fields limit that share (dates and money amounts are the usual suspects)?  
3. Does OCR text with positions beat plain OCR text for field reading?

**Done when.** Two results tables: attachment types, and fields (one row per field), on at least 100 forms. A form-level number is not reported unless the per-field numbers are.

## **Project 3: read a certificate of insurance and check it against requirements**

**Aim.** A vendor sends a certificate of insurance (ACORD 25). Read its coverage lines and compare each with the requirement the contract states, with no human check on comparisons that clear the cut-off.

This is the front half of the certificates job. Emailing the vendor about gaps and tracking renewals is left out.

**Input.** One certificate PDF, and a requirements list as data: for each coverage type (general liability, auto, umbrella, workers' compensation), the minimum limit, and whether the certificate holder must be named as additional insured.

**Output.** Per coverage line on the certificate: (coverage type, carrier, policy number, effective date, expiration date, each limit, score). Per requirement: pass / fail / not found, with a score.

**Method.**

* Field reading as in Project 2\. The ACORD 25 is one fixed layout with a known table of coverage rows, so the field list is fixed.  
* Comparison is code, not a model: limit on certificate ≥ required limit; expiration date after today; additional-insured box ticked where required. The comparison's score is the lowest score among the fields it used.

**What is measured.**

* Per-field coverage at 2% and 5%, as in Project 2\.  
* Requirement-check coverage: share of (certificate, requirement) pairs whose pass/fail is accepted without review, with error measured against hand-checked pass/fail.  
* Certificate coverage: share of certificates where every requirement check is accepted.

**Questions the result answers.**

1. What share of certificates can be checked with no human looking at them?  
2. Which field limits that share? Limits are money amounts in a dense table; expect them to.  
3. How much does a wrong field matter when the comparison has a wide margin (a \$5M limit against a \$1M requirement passes even if the model misreads one digit)?

**Done when.** Field table and requirement-check table on at least 100 certificates, each against a requirements list of four coverages.

## **Corpus**

There is no public corpus of filled insurance documents, and ACORD licenses its forms, so the test documents have to be made or found.

* **Project 1 (claims packets):** assemble packets from public documents of the right types. Estimates, police reports and medical bills exist on DocumentCloud and in RVL-CDIP-N's source PDFs; photos are any image page. A packet is a random sequence of 3–8 documents with known boundaries, so ground truth is free. Add a tenth of packets containing an out-of-scope document.  
* **Projects 2 and 3 (ACORD forms):** fill forms synthetically. The field values are generated, so ground truth is exact. Vary the filling: typed into the PDF form fields, printed and scanned at 150–300 dpi, and a share with fields left blank or overflowing. Whether blank ACORD forms can be used this way depends on ACORD's licence; check before building. If not, build a form with the same fields and layout under a different name — the method does not depend on the ACORD name.  
* **Real documents:** anything from a real workplace stays on that workplace's machine. The repos hold code and synthetic data only.

Minimum sizes: 100 test documents per project, with 114 consecutive correct answers needed in the calibration ranking to clear 2%, so a calibration pool of at least 300\.

