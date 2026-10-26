# **Automatic Document Sorting Without Human Review**

---

## **Aim**

Sort incoming PDFs into document types automatically, with no human check, while keeping the error on accepted pages under a fixed bound. The target documents are born-digital PDFs and clean scans (150 dpi or higher).

Our goal is to reduce human labour by minimizing the amount of human checking.[^1]  

[layout-classify](https://github.com/peterwilliams97/layout-classify) (Python, MIT, commit [3e0e8b6](https://github.com/peterwilliams97/layout-classify/tree/3e0e8b6b5fb85ea4e7063cf7a5871ac812bda6c0)) labels the first page of a PDF with one of 11 document types and a probability score in \[0, 1\]. Above a score cut-off the label is accepted with no human check; below it the page goes to a person. A page that fits none of the 11 types is labelled none by some classifiers and always goes to a person.

The 11 types: budget, email, form, invoice, letter, memo, news\_article, questionnaire, resume, scientific\_publication, specification.

We measure the fraction of pages that pass the cut-off (coverage) and the fraction of accepted pages that are misclassified (error), at 5% and 2% error bounds. The 2% bound is there because 5% error is probably worse than a careful human operator achieves; human error rates are examined in the synth-classify article.

 We built several classifiers that run on a  laptop and asked four questions about each one:

> 1. **How much work can it do without a person checking?** *Coverage* is the share of test pages above the cut-off. *Error* is the share of those whose type is wrong. We report coverage at 5% and at 2% error, with 0 hand-labelled pages, 10 per type, and every training page.  
> 2. **Does the page image beat the OCR text?**  
> 3. **What do pages that fit no type cost?** Production must send these to a person.  
> 4. **How many seconds per page?**

## **Answer**

1. **With no labelled pages, d3-flash given one sentence per type and a "none" option files 74.5% of test pages at under 5% error and 61% at under 2%.** The most any classifier can file is 75%, because a quarter of the test pages fit no type. The best trained model, TF-IDF \+ logistic regression on 411 labelled pages, files 50% and 33%.  
2. **The page image alone files nothing.** Image plus OCR words (LayoutLMv3, fine-tuned on 411 pages) files 37% at 5%, less than text alone. The vision LLM gemma4:e4b reading the image is 97.8% accurate but gives no score, so nothing it labels can skip a person.  
3. **Pages that fit no type cost coverage twice.** They can only go to a person, and keeping them out pushes the cut-off up for everything else: UltraBERT \+ LR's coverage of in-class pages fell from 83% to 62% when the reject share of the calibration set rose from 10% to 25%. Allowed to answer "none", d3-flash labelled 73 of 91 reject pages "none"; 8 slipped through at 5%, 1 at 2%.  
4. **Seconds per page:** Tesseract OCR 0.67; then TF-IDF \+ LR 0.0004, UltraBERT \+ LR 0.04, d3-flash 1.9. gemma4:e4b 2.65 with no OCR.

## **Method**

### **The pages**

The source PDFs behind [RVL-CDIP-N](https://proceedings.neurips.cc/paper_files/paper/2022/hash/4c0986bd04d747745beba3752bdf4d9d-Abstract-Datasets_and_Benchmarks.html) (Larson et al., NeurIPS 2022): modern documents, mostly from [DocumentCloud](https://www.documentcloud.org/home/), labelled with 12 types. Each PDF's first page is rendered at 200 dpi. A quality gate keeps native-digital pages and scans of at least 150 dpi; 184 of 1,229 fail. Handwritten is dropped (a medium, not a type), leaving 11 types: budget, email, form, invoice, letter, memo, news article, questionnaire, resume, scientific publication, specification. Reject pages come from RVL-CDIP-O, the same authors' set of documents of none of the types: 229 pages, labelled none.

| Split | In-class pages | Reject pages | Use |
| :---- | :---- | :---- | :---- |
| train | 204 | 69 | Build classifiers (reject pages never trained on) |
| validation | 207 | 69 | With train, set the cut-off |
| test | 274 | 91 | Read once, after every decision |

### **The classifiers**

| Reads | Classifier | Hand labels |
| :---- | :---- | :---- |
| OCR text | TF-IDF \+ logistic regression | 411, or 10 per type |
| OCR text | UltraBERT-Embed-150M (frozen) \+ logistic regression | 411, or 10 per type |
| OCR text | d3-flash (vllm-sr/d3-flash), a decision model asked a multiple-choice question with the type definitions; variants with 3 example pages per type, and with "none" as an option | 0 (33 for the examples) |
| Page image | DiT-base (frozen) \+ logistic regression | 411, or 10 per type |
| Image \+ OCR words and boxes | LayoutLMv3-base, all weights fine-tuned | 411, or 10 per type |
| Page image | gemma4:e4b via Ollama, given type names and definitions, reply restricted to a name; variant with "none" | 0 |

### **The cut-off**

One rule for every row. The cut-off is the lowest score at which the one-sided 90% Clopper-Pearson upper bound on the error of accepted pages is at most 5% (or 2%). It is fitted on the 549 train and validation pages. For a trained classifier those scores are out-of-fold: the pages are split five ways, each fold scored by a model trained on the other four. The same five models are scored on test, and a trained row is their mean. Test is read once, after every cut-off and choice is fixed.

### **The type sentences**

Each type is one sentence in classes.py saying what separates it from its nearest neighbour; "none" is one sentence in d3.py. They were written once, then rewritten once: the confusion matrix on the 549 train and validation pages showed almost every d3-flash error touching "none", so three sentences changed. "None" was defined by what it is (a report or committee paper, court filing, press release or media statement, policy or timeline, data table or list, slide, web page, or a page too garbled to read”") instead of by absence; specification gained "or a product data sheet"; news article gained "not a press release or an organisation's own report". Test was then read once. The version 1 sentences and their results are kept in the repo.

### **What was measured on test**

> * **Coverage**: share of all 365 test pages above the cut-off. The most possible is 274/365 \= 0.7507.  
> * **Error**: share of accepted pages whose type is wrong. A reject page given a type is wrong.  
> * **Reject leak**: share of the 91 reject pages above the cut-off.  
> * **Accuracy**: on the 274 in-class pages.  
> * **Seconds per page**, median, classifier only; OCR reported once.

## **Results**

### **Coverage at 5% and 2% error, all 365 test pages**

| Classifier | Hand labels | Coverage 5% | Error 5% | Reject leak 5% | Coverage 2% | Error 2% |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| d3-flash, definitions \+ none | 0 | **0.7452** | 0.0294 | 8 of 91 | **0.6110** | 0.0045 |
| d3-flash, definitions | 0 | 0.6411 | 0.0256 | 6 of 91 | 0.5534 | 0.0149 |
| d3-flash, few-shot (v1 sentences) | 33 | 0.5753 | 0.0429 | 8 of 91 | 0.4575 | 0.0000 |
| TF-IDF \+ LR | 411 | 0.4975 | 0.0386 | 0.0264 | 0.3342 | 0.0213 |
| UltraBERT \+ LR | 411 | 0.4718 | 0.0174 | 0.0264 | 0 | – |
| LayoutLMv3 | 411 | 0.3742 | 0.0341 | 0.0396 | 0 | – |
| TF-IDF \+ LR | 10 per type | 0.3518 | 0.0311 | 0.0308 | 0 | – |
| UltraBERT \+ LR | 10 per type | 0.3047 | 0.0358 | 0.0242 | 0 | – |
| DiT \+ LR | 411 or 10 per type | 0 | – | 0 | 0 | – |
| LayoutLMv3 | 10 per type | 0 | – | 0 | 0 | – |
| gemma4:e4b, image | 0 | no score, so no cut-off |  |  |  |  |

Trained rows are the mean over five fold models; the README gives each fold's range. Only TF-IDF \+ LR at 2% lands above its level on test (0.0213), by one or two reject pages per fold model.

### **Accuracy on the 274 in-class test pages, and seconds per page**

| Classifier | Hand labels | Accuracy | Seconds per page |
| :---- | :---- | :---- | :---- |
| d3-flash, definitions | 0 | **0.9927** | 1.71 \+ OCR |
| d3-flash, definitions \+ none | 0 | 0.9854 | 1.86 \+ OCR |
| gemma4:e4b, image | 0 | 0.9781 | 2.65 |
| LayoutLMv3 | 411 | 0.9686 | 0.051 \+ OCR |
| UltraBERT \+ LR | 411 | 0.9358 | 0.036 \+ OCR |
| d3-flash, few-shot (v1 sentences) | 33 | 0.9197 | 11.5 \+ OCR |
| TF-IDF \+ LR | 10 per type | 0.8869 | 0.0003 \+ OCR |
| UltraBERT \+ LR | 10 per type | 0.8869 | 0.035 \+ OCR |
| TF-IDF \+ LR | 411 | 0.8693 | 0.0003 \+ OCR |
| DiT \+ LR | 411 | 0.6117 | 0.019 |
| DiT \+ LR | 10 per type | 0.4781 | 0.019 |
| LayoutLMv3 | 10 per type | 0.3839 | 0.049 \+ OCR |

OCR (Tesseract) is 0.673 s a page, median. Hardware: one MacBook Pro, Apple M5 Pro, 48 GB; neural models on the GPU through PyTorch MPS; gemma4:e4b through Ollama 0.40.8.

### **Where the errors are**

d3-flash with "none" makes 4 errors on the 274 in-class test pages and never confuses two of the 11 types with each other. Its other 18 errors are reject pages given a type: 10 called news article (press releases, an annual report, an endorsements list), 6 called form, 1 memo, 1 scientific publication. UltraBERT \+ LR fails the way people do: 22 of its 85 memo scorings are called letter, the pair Larson, Lim and Leach found most often in the human labels. So the decision model's weakness is "is this one of ours", not "which one".

### **Why**

* **Score quality beats accuracy.** Filing without a person needs wrong answers to score lower than right ones. LayoutLMv3 is 96.9% accurate and files 37%; d3-flash is 98.5% and files 75%. Fine-tuning a classifier on 328 pages pushes nearly every score to 1.0, so its cut-off (0.961) sits above most of its right answers. d3-flash’s scores spread out. We measured the spread, not the mechanism.  
* **The model already knows the types.** Invoice, memo, resume are formats a  language model has read many thousands of; one sentence per type is enough to point at them. A linear classifier on 10 to 30 pages per type has to learn the format from those pages alone.  
* **Clean documents say what they are in the first 150 words.** After the quality gate, the header usually carries the type (INVOICE, MEMORANDUM, To:/From:, Abstract). Models that read the image at 224×224 lose that text and fall to 0.6 accuracy; a vision LLM that can read it recovers (0.978) but gives no score.  
* **Few-shot examples anchor on the wrong thing.** Three 50-word snippets per type made the model match topics from the snippets rather than the sentence: 14 of 15 scientific publications went to news article or specifications.  
* **“None” works when it names what it is.** Defined by absence; defined as “a report, court filing, press release, timeline, data table, slide, web page or garbled page” it caught 73, and the remaining leak is press releases, which still read as news.

[Document classification: a short introduction](https://docs.google.com/document/d/1vRxDLM1KMRF5rUioUJEHoAgkwX1ad_fwSKfOy9vFr2s/edit?usp=sharing) 

## **Discussion**

* **Zero labels won.** A decision model asked a multiple-choice question with one sentence per type files more pages, more accurately, than anything trained on 411 hand labels. The sentences are the labour: 12 of them, written twice.  
* **Accuracy and coverage pick different winners.** gemma4:e4b and LayoutLMv3 are among the most accurate and file little or nothing: the first has no score, the second's scores sit so close to 1 that the cut-off lands above most right answers.  
* **The image alone is useless here; layout adds nothing to text.** DiT files nothing. LayoutLMv3, which reads image, words and boxes, files less than TF-IDF on words alone. On 10 labels per type the image models collapse (0.38 to 0.48 accuracy) while the text models hold 0.89.  
* **Reject pages set the cut-off.** Raising the reject share of the calibration set from 10% to 25% cut UltraBERT's in-class coverage from 0.83 to 0.62 and removed its 2% coverage. Letting the classifier answer "none" recovers coverage: for d3-flash it took 5% coverage from 0.64 to 0.75.  
* **Defining "none" by what it is, not by absence, fixed most of the reject leak.** Reject pages labelled "none" went from 65 of 91 to 73\.  
* **The calibration set must be large.** On 141 pages the 5% cut-off swung from 0.67 to 0.82 coverage with the draw, and one draw let 42 of 91 reject pages through. On 549 it settled. At 2%, 141 pages certify nothing on any draw; 276 and 549 both certify about 0.55.  
* **Few-shot examples hurt d3-flash** (0.98 to 0.92 accuracy, 7× the time): 14 of its 22 errors were scientific publications pulled toward the example text.  
* **Runtimes move numbers.** An Ollama auto-update changed gemma4:e4b from 0.949 to 0.978 accuracy and from 0.99 to 2.65 s a page with the same model file. Record the runtime version with every result.

## **Next time**

* Write one sentence per type saying what separates it from its nearest neighbour, and one for "none" saying what the out-of-scope documents are. Start with a decision model given those sentences; measure before labelling anything.  
* Rewrite sentences from the confusion matrix on calibration pages, never on test, and count the rounds.  
* Set the cut-off on at least a few hundred labelled pages, with reject pages at their production share. Use the Clopper-Pearson bound; the plain cut-off flatters.  
* Pick by coverage at the error target, not accuracy.  
* Run OCR once and cache it; it is the slowest step for every text model.  
* Pin model revisions and record runtime versions.

## **Limits**

> * One page per document, page 1\. Multi-page documents were not classified.  
> * Three types have 12 to 15 test pages, so their per-type figures are coarse.  
> * Every number is from one run; LayoutLMv3 on MPS is not bit-for-bit repeatable.  
> * RVL-CDIP-O holds some in-scope documents (a filled form, a survey script, a check register); d3-flash's "errors" on those are the labels' errors.  
> * The type sentences had two rounds on the calibration pages; a third would start to fit them.  
> * DocumentCloud documents keep their own rights; CC BY 3.0 covers the dataset.

> 

## **Use it**

classify.py \<folder\> labels page 1 of every PDF or image in a folder and writes a CSV: file, type, score, and *file* or *review* at the 5% or 2% cut-off. view.py turns the CSV into one HTML page with thumbnails and filters.

## **Where things are**

[layout-classify](https://github.com/peterwilliams97/layout-classify). classes.py: the 11 types and sentences. d3.py: d3-flash and the "none" sentence. fetch.py, quality.py, split.py, render.py: corpus, gate, splits, page images. ocr.py: Tesseract cache. train.py: TF-IDF, UltraBERT, DiT. finetune.py: LayoutLMv3. llm.py: gemma4:e4b. score.py, confidence.py: scores, cut-offs, coverage. classify.py, view.py: the tool and the viewer. Every number above is in a file under results/; the version 1 sentences and results under results/definitions-v1/ and docs/history/.

## **Glossary**

> * **Coverage**: share of pages the classifier files without a person.  
> * **Cut-off** (tau\_cp): the score above which a page is filed; set so the 90% upper bound on the error of filed pages is at most the target.  
> * **Reject page**: a page that fits none of the types; labelled none.  
> * **Reject leak**: share of reject pages that pass the cut-off.  
> * **Out-of-fold**: each page scored by a model that did not train on it.  
> * **Decision model**: a model that answers a multiple-choice question with a probability per option (d3-flash).

> 

## **Sources**

> * [Larson et al., Evaluating Out-of-Distribution Performance on Document Image Classifiers, NeurIPS 2022](https://proceedings.neurips.cc/paper_files/paper/2022/hash/4c0986bd04d747745beba3752bdf4d9d-Abstract-Datasets_and_Benchmarks.html) (RVL-CDIP-N and RVL-CDIP-O)  
> * [Larson, Lim and Leach, On Evaluation of Document Classification using RVL-CDIP, EACL 2023](https://arxiv.org/abs/2306.12550) (human label error rates, Table 4\)  
> * [dmis-lab/UltraBERT-Embed-150M](https://huggingface.co/dmis-lab/UltraBERT-Embed-150M)  
> * [microsoft/dit-base](https://huggingface.co/microsoft/dit-base), [microsoft/layoutlmv3-base](https://huggingface.co/microsoft/layoutlmv3-base)  
> * [vllm-sr/d3-flash](https://huggingface.co/vllm-sr/d3-flash)  
> * [Local text classification: lessons from synth-classify (version 10\)](https://docs.google.com/document/d/1XVe15DlxaYhHGlWTb-hgVU-HXgN_on3i6hR-MXje788/edit)

[^1]:  IDP vendors promote these kinds of results that don't require human checking  as “straight-through processing” (STP). Their STP numbers usually mean “scored above a threshold we picked”. They have no bound on their error rates and they don't publish tests for documents that don't fit in their defined categories.