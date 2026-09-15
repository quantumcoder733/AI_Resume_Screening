# AI Resume Screening Interview Preparation

This guide describes the implementation in this repository. The project is an explainable screening and ranking aid, not an automated hiring system and not a trained classifier.

## A. 30-Second Project Explanation

I built a Python application that compares one or more PDF resumes with a job description. It extracts and cleans the text, checks recognized skills, uses TF-IDF and cosine similarity for text relevance, and combines similarity and skill match into a transparent 40/60 screening score. Streamlit displays the ranked candidates, statistics, charts, and matched or missing skills. An optional OpenAI feature explains an existing result in natural language, but it never scores or ranks candidates.

## B. 1-Minute Project Explanation

The user enters a job description and uploads one or more PDF resumes in a single-page Streamlit interface. Each PDF is stored temporarily and sent through a shared batch pipeline. The pipeline uses pypdf to extract text, normalizes whitespace, and checks a fixed skill dictionary with aliases such as `sklearn` for `scikit-learn`.

The application also converts the cleaned resume and job description into TF-IDF vectors and compares them with cosine similarity. Skill match is calculated from recognized required skills found in both texts. The final screening score is `0.40 * resume_similarity + 0.60 * skill_match`. Candidates are sorted by that score, then displayed in a Pandas table with NumPy statistics and Matplotlib screening/ranking charts.

The evaluation module is separate: it applies a threshold to existing scores and compares the resulting suitable/not_suitable decisions with synthetic/manual labels. The optional OpenAI module receives only an already-computed candidate result and produces explanatory feedback. It does not change the score, ranking, or analysis.

## C. Complete Project Architecture

```text
PDF resume(s) + job description
            |
            v
PDF text extraction with pypdf
            |
            v
Basic whitespace cleaning
            |
      +-----+-----+
      |           |
      v           v
Skill aliases   TF-IDF vectors
      |           |
      v           v
Skill match   Cosine similarity
      \           /
       \         /
        v       v
  40% similarity + 60% skill match
            |
            v
Batch ranking and failure handling
            |
            v
Pandas DataFrame and NumPy statistics
            |
            v
Matplotlib screening/ranking charts
            |
            v
Single-page Streamlit results
            |
            v
Optional OpenAI natural-language feedback
```

The evaluation metrics experiment is separate from this main flow. It uses a small synthetic/manual CSV and does not change screening.

## D. Step-by-Step Data Flow

1. Streamlit collects a job description and one or more PDF uploads.
2. The app writes each upload into a temporary directory.
3. `screen_resume_paths` validates each path and calls `analyze_resume`.
4. `extract_text_from_pdf` reads available text from each PDF page.
5. `clean_text` reduces repeated whitespace and trims the result.
6. `extract_skills` finds canonical skills through the fixed alias dictionary.
7. `calculate_similarity` fits TF-IDF on the cleaned resume and job description and calculates cosine similarity.
8. The analyzer calculates skill coverage from required and resume skill sets.
9. `calculate_overall_score` applies the unchanged 40% similarity plus 60% skill-match formula.
10. Batch screening keeps successful candidates and failures separate, then sorts successful candidates by score.
11. `create_candidate_dataframe` creates the ranked Pandas table.
12. NumPy calculates average, minimum, maximum, and standard deviation values.
13. Matplotlib creates the two screening/ranking figures from that table.
14. Streamlit displays scores, skill details, failures, statistics, and charts.
15. Only when the user clicks a candidate's feedback button does `ai_feedback.py` send existing result fields to OpenAI.

## E. Important Concepts

### 1. PDF extraction

**What it is:** Reading text stored inside a PDF document.

**Why this project uses it:** TF-IDF and skill matching need text rather than raw PDF bytes.

**How this project uses it:** `pdf_extractor.py` uses `pypdf.PdfReader` and joins the text returned from each page.

**Simple example:** A PDF page containing `Python SQL` becomes the string `Python SQL` for later analysis.

### 2. Text cleaning

**What it is:** Normalizing messy whitespace and removing unnecessary surrounding spaces.

**Why this project uses it:** PDF extraction can produce line breaks, tabs, and repeated spaces.

**How this project uses it:** `clean_text` replaces any whitespace run with one space before matching and TF-IDF.

**Simple example:** `" Python\n\n SQL\tPandas "` becomes `"Python SQL Pandas"`.

### 3. Skill extraction

**What it is:** Finding known skill names in a piece of text.

**Why this project uses it:** Recruiters need an explainable list of skills that match or are missing.

**How this project uses it:** `skill_extractor.py` lowercases text and checks each configured alias.

**Simple example:** Text containing `Python and pandas` produces canonical skills `python` and `pandas`.

### 4. Aliases

**What it is:** Alternate spellings or names that represent the same canonical skill.

**Why this project uses it:** Candidates and job descriptions may use different common spellings.

**How this project uses it:** The dictionary maps `sklearn`, `scikit learn`, and `scikit-learn` to `scikit-learn`; it maps `cpp` to `c++`.

**Simple example:** `"Experience with sklearn"` can match a required `scikit-learn` skill.

### 5. TF-IDF

**What it is:** A method that converts document words into numeric importance values using term frequency and inverse document frequency.

**Why this project uses it:** It provides a simple, explainable baseline for comparing resume and job-description wording.

**How this project uses it:** `TfidfVectorizer` fits on the two cleaned documents for the current comparison.

**Simple example:** The words in `Python Pandas SQL` become columns in a numeric vector.

### 6. Cosine similarity

**What it is:** A measure of how aligned two numeric vectors are.

**Why this project uses it:** It compares TF-IDF representations without depending only on document length.

**How this project uses it:** `cosine_similarity` compares the resume vector with the job-description vector and the result is shown as a percentage.

**Simple example:** Two documents sharing important terms have a higher cosine similarity than documents with unrelated terms.

### 7. Skill match

**What it is:** The percentage of recognized required skills also found in the resume.

**Why this project uses it:** It provides a direct and explainable coverage signal.

**How this project uses it:** The analyzer computes matched and missing set values, then divides matched required skills by required skills. If no required skills are recognized, it returns zero.

**Simple example:** Three matched skills out of four required skills gives `75%` skill match.

### 8. Weighted scoring

**What it is:** Combining multiple signals with fixed weights.

**Why this project uses it:** It produces one transparent ranking value while keeping both signals visible.

**How this project uses it:** `scorer.py` returns `0.40 * resume_similarity + 0.60 * skill_match`.

**Simple example:** Similarity `50` and skill match `75` produce `65`: `50 * 0.40 + 75 * 0.60`.

### 9. Pandas

**What it is:** A Python library for tabular data, including DataFrames.

**Why this project uses it:** Candidate results are easier to sort, inspect, and display as a table.

**How this project uses it:** `results_analysis.py` converts candidate dictionaries into columns for rank, candidate, similarity, skill match, and overall score.

**Simple example:** Three candidate dictionaries become three sorted DataFrame rows.

### 10. NumPy

**What it is:** A library for numeric arrays and calculations.

**Why this project uses it:** It makes score statistics explicit and reliable.

**How this project uses it:** The project converts the overall-score column to an array and calculates mean, minimum, maximum, standard deviation, and extreme positions.

**Simple example:** Scores `[52, 72]` have mean `62` and population standard deviation `10`.

### 11. Matplotlib

**What it is:** A Python plotting library.

**Why this project uses it:** It provides simple charts for candidate screening and ranking.

**How this project uses it:** `visualizations.py` creates an overall-score bar chart and a grouped similarity/skill-match bar chart.

**Simple example:** A bar chart can show that Candidate A has a higher screening score than Candidate B.

### 12. Batch screening

**What it is:** Processing multiple files in one workflow.

**Why this project uses it:** Users commonly compare more than one resume for a role.

**How this project uses it:** `batch_screening.py` validates each path, analyzes each PDF, records failures separately, and sorts successful candidates.

**Simple example:** If one of three PDFs is corrupt, the two valid candidates still appear and the corrupt file is reported.

### 13. Evaluation metrics

**What it is:** Measures such as accuracy, precision, recall, and F1 that compare predictions with known labels.

**Why this project uses it:** It demonstrates how a chosen threshold could be assessed separately from the screening heuristic.

**How this project uses it:** `evaluation.py` turns scores at or above a threshold into `suitable`, compares them with synthetic/manual labels, and uses scikit-learn metrics.

**Simple example:** A threshold can predict `suitable` for scores at least `60`, then compare those decisions with manually assigned labels.

### 14. Streamlit

**What it is:** A Python library for building simple data applications.

**Why this project uses it:** It provides a beginner-friendly interface for uploads, text input, results, charts, and optional feedback.

**How this project uses it:** `app.py` calls backend functions and renders their results on one page.

**Simple example:** A user clicks `Screen Resumes` and sees the ranked DataFrame without the UI implementing TF-IDF itself.

### 15. Gemini API

**What it is:** An external API accessed through Google's official Python SDK to generate natural-language text.

**Why this project uses it:** It can explain an already-computed screening result in a more readable way.

**How this project uses it:** `ai_feedback.py` sends supplied scores, matched skills, missing skills, and optional job-description text only after the user requests feedback.

**Simple example:** Given matched `python` and missing `sql`, it may explain those supplied facts and suggest adding concrete SQL evidence, without inventing experience.

### 16. Environment variables

**What it is:** Configuration supplied outside source code by the operating system or shell.

**Why this project uses it:** API credentials should not be written into source files.

**How this project uses it:** The Gemini key is read from `GEMINI_API_KEY`; local development can load it from `.env` or the ignored `key.env` fallback.

**Simple example:** PowerShell can set `$env:GEMINI_API_KEY` for a local session without placing the key in Git-tracked code.

### 17. Git

**What it is:** A version-control system that records file changes.

**Why this project uses it:** It supports review, history, rollback, and collaboration.

**How this project uses it:** The repository tracks the application, tests, documentation, and configuration while `.gitignore` excludes caches and `.env` files.

**Simple example:** `git diff` shows changes before a commit; this project intentionally created no commit during the staged work.

### 18. pytest

**What it is:** A Python testing framework.

**Why this project uses it:** It checks repeatable behavior in the analyzer, batch handling, analysis helpers, charts, evaluation experiment, and mocked AI feedback.

**How this project uses it:** Tests use local sample data and mock the Gemini client, so they do not need network access.

**Simple example:** `pytest -q -p no:cacheprovider` runs the current test suite without creating a pytest cache.

## F. Scoring Explanation

The existing formula is:

```text
overall_score = 0.40 * resume_similarity + 0.60 * skill_match
```

For a resume with `50%` similarity and `75%` skill match:

```text
overall_score = 0.40 * 50 + 0.60 * 75
              = 20 + 45
              = 65%
```

This is a screening and ranking heuristic. It is not accuracy because it does not compare predictions with known ground-truth labels. Similarity and skill match are input signals; the weighted score is a combined ranking value.

## G. Evaluation Explanation

The evaluation experiment uses the synthetic/manual file `data/evaluation/sample_labeled_results.csv`. Each row has an existing-style screening score and a manually assigned `suitable` or `not_suitable` label.

A threshold rule such as `screening_score >= 60` predicts `suitable`; lower scores predict `not_suitable`. Those predictions can be compared with actual labels:

- **Accuracy:** correct predictions divided by all predictions.
- **Precision:** among predicted suitable candidates, the proportion actually suitable.
- **Recall:** among actually suitable candidates, the proportion identified as suitable.
- **F1-score:** a combined measure of precision and recall.

These metrics evaluate a threshold decision against labels. They do not say that the underlying 40/60 screening score is 40% or 60% accurate. The dataset is a learning demonstration, not a real-world validation dataset, and no classifier is trained.

## H. GenAI Explanation

GenAI is downstream of screening:

```text
screening result -> optional AI feedback
```

It receives already-computed candidate information, including matched skills, missing skills, similarity, skill match, overall score, and optional job-description text. Its job is to explain strengths, relevant gaps, the screening result, and practical resume suggestions using only supplied information.

It does not perform PDF extraction, text cleaning, TF-IDF, cosine similarity, skill matching, scoring, ranking, or evaluation. It is optional because the core application must work without an API key or network access. The key is read from `OPENAI_API_KEY` and is not hardcoded. Tests replace the client with a mock and make no real API calls.

## I. Likely Internship Interview Questions

### 1. What problem does your project solve?

**Short answer:** It organizes a first-pass comparison of PDF resumes against a job description.

**Deeper explanation:** It extracts text, checks recognized skills, calculates word-level similarity, combines the signals into a transparent screening score, and ranks candidates. It supports human review rather than making hiring decisions.

### 2. Why did you choose this project?

**Short answer:** Resume comparison is a practical problem that lets me demonstrate Python, NLP basics, data analysis, visualization, testing, and a simple UI.

**Deeper explanation:** The project has a clear input/output flow and keeps the scoring explainable. It also lets me separate deterministic analysis from optional natural-language feedback.

### 3. Explain your project architecture.

**Short answer:** Streamlit collects input, backend modules analyze each PDF, and presentation modules rank and visualize the results.

**Deeper explanation:** Batch screening calls the analyzer. The analyzer calls extraction, cleaning, skills, similarity, and scoring modules. Results analysis creates the DataFrame and statistics, while optional AI feedback runs only after a user request.

### 4. How do you extract text from a PDF?

**Short answer:** I use `pypdf.PdfReader` and join available page text.

**Deeper explanation:** Each page contributes `page.extract_text() or ""`. The project does not use OCR, so scanned image PDFs may produce little text.

### 5. Why do you clean the text?

**Short answer:** PDF text often contains inconsistent whitespace.

**Deeper explanation:** Normalizing whitespace makes skill checks and TF-IDF input more consistent while keeping the cleaning logic small and explainable.

### 6. How do you extract skills?

**Short answer:** I lowercase the text and search for aliases in a fixed skill dictionary.

**Deeper explanation:** The extractor returns canonical names. The analyzer compares resume and required skill sets to produce matched and missing lists.

### 7. What is TF-IDF?

**Short answer:** TF-IDF converts document words into numeric importance values.

**Deeper explanation:** Term frequency reflects use in a document, while inverse document frequency reduces the influence of words common across documents. It is a feature representation, not a trained classifier here.

### 8. Why use TF-IDF?

**Short answer:** It is a simple, understandable baseline for comparing resume and job-description wording.

**Deeper explanation:** It is available in scikit-learn and produces vectors that can be compared. It does not understand deep meaning or all synonyms.

### 9. What is cosine similarity?

**Short answer:** It measures how aligned two numeric vectors are.

**Deeper explanation:** The project compares the two TF-IDF vectors and multiplies the 0-to-1 result by 100 for a displayed similarity percentage.

### 10. Why cosine similarity?

**Short answer:** It compares vector direction and is less dependent on document length than a raw word count.

**Deeper explanation:** Shared important terms generally make the vectors more aligned, giving an intuitive text-relevance signal.

### 11. How is skill matching different from text similarity?

**Short answer:** Similarity compares word patterns; skill matching checks explicit recognized skills.

**Deeper explanation:** A resume can have similar wording without containing every required skill, so both signals are displayed separately.

### 12. Explain your 40/60 scoring.

**Short answer:** The score is 40% resume similarity plus 60% skill match.

**Deeper explanation:** Skill match contributes more because it is a direct comparison with recognized required skills. The formula is implemented in `scorer.py`.

### 13. Why did you choose 40/60?

**Short answer:** It is an explainable project design choice that gives greater weight to direct skill coverage.

**Deeper explanation:** It is not a scientifically validated optimum. A real deployment would need stakeholder agreement and careful labeled evaluation before changing weights.

### 14. Is your score accuracy?

**Short answer:** No. It is a weighted screening and ranking heuristic.

**Deeper explanation:** Accuracy requires predictions compared with known labels. The screening score is calculated from similarity and skill match and should not be called accuracy.

### 15. How did you evaluate the system?

**Short answer:** I added a separate threshold experiment using synthetic/manual labels.

**Deeper explanation:** It converts existing scores into suitable/not_suitable predictions and calculates accuracy, precision, recall, and F1. This does not change screening or create a classifier.

### 16. What are precision, recall and F1?

**Short answer:** Precision measures correctness among positive predictions, recall measures coverage of actual positives, and F1 combines both.

**Deeper explanation:** They are calculated against manual labels in the separate experiment, not against the internal score formula.

### 17. Why did you use Pandas?

**Short answer:** Pandas turns candidate dictionaries into a sortable, readable table.

**Deeper explanation:** The DataFrame contains rank, candidate, similarity, skill match, and overall score and is displayed in Streamlit.

### 18. Why did you use NumPy?

**Short answer:** NumPy provides clear array-based score statistics.

**Deeper explanation:** The project uses it for mean, minimum, maximum, standard deviation, and locating highest or lowest scores.

### 19. Why did you use Matplotlib?

**Short answer:** It creates simple charts directly from the ranked DataFrame.

**Deeper explanation:** The project has an overall-score bar chart and a grouped similarity/skill-match chart. They are screening charts, not accuracy charts.

### 20. Why did you use Streamlit?

**Short answer:** It gives the project a simple Python interface without building a separate frontend.

**Deeper explanation:** Streamlit handles text input, PDF uploads, buttons, tables, messages, charts, and optional feedback while backend modules keep the business logic separate.

### 21. How does batch screening work?

**Short answer:** It loops over PDF paths, analyzes each valid file, stores failures separately, and sorts successful candidates by score.

**Deeper explanation:** `BatchScreeningResult` contains both `candidates` and `failures`, so one bad file does not stop the rest.

### 22. What happens if one PDF is invalid?

**Short answer:** That file produces a user-facing failure message while valid candidates remain available.

**Deeper explanation:** The batch layer catches analysis errors per path. The temporary upload directory is cleaned after the request.

### 23. What does GenAI do in your project?

**Short answer:** It explains an existing candidate result in natural language.

**Deeper explanation:** It can organize supplied strengths, matched skills, missing skills, score context, and resume suggestions. It does not calculate or change any screening value.

### 24. Why is GenAI optional?

**Short answer:** The deterministic screening workflow should work without a network service or API key.

**Deeper explanation:** The user explicitly clicks the feedback button, and missing-key or API-failure messages do not remove screening results.

### 25. How do you protect the API key?

**Short answer:** The key comes from `OPENAI_API_KEY` and is never hardcoded.

**Deeper explanation:** `.env` is ignored, tests use a harmless placeholder and mock client, and error messages do not include the key.

### 26. What are the limitations of your project?

**Short answer:** The skill dictionary is fixed, substring matching lacks context, TF-IDF is word-based, and scanned PDFs may fail without OCR.

**Deeper explanation:** The score is not validated hiring accuracy, GenAI can be unavailable or imperfect, and the application should remain a human screening aid.

### 27. What would you improve in the future?

**Short answer:** I would improve skill matching, support OCR, and collect an ethical labeled dataset for evaluation.

**Deeper explanation:** Further work could explore embeddings or a classifier only after privacy, bias, labels, and evaluation practices are addressed. Those features are not currently implemented.

### 28. Why did you not use a classifier?

**Short answer:** The project does not have an appropriate labeled training dataset and the goal is an explainable baseline.

**Deeper explanation:** A classifier would need training, validation, labels, and careful interpretation. The current workflow compares texts and ranks them instead.

### 29. Why did you not use embeddings?

**Short answer:** TF-IDF is simpler to explain and is enough for this learning-focused baseline.

**Deeper explanation:** Embeddings could capture broader semantic meaning, but they would add another model and dependency and are outside the implemented scope.

### 30. What part of the project did you personally implement or understand?

**Short answer:** I understand the full path from PDF input through cleaning, skills, similarity, scoring, ranking, visualization, evaluation, and optional feedback.

**Deeper explanation:** I can explain the module boundaries, the fixed formula, batch failure handling, tests, notebook demonstrations, and why GenAI is downstream rather than the source of truth.

## J. Explain Your Project Like I Am a Recruiter

I built a tool that helps a recruiter make an organized first comparison of resumes. They enter a job description and upload several PDF resumes. The tool reads the available text, checks which recognized skills appear, compares the resume wording with the job description, and produces a transparent screening score. It then ranks the candidates and shows the matched and missing skills in a table with simple charts.

The score is only a screening aid, not a hiring decision or accuracy percentage. There is also an optional button that can turn an existing result into clearer written feedback, but that AI feature does not decide the ranking or invent candidate qualifications.

## K. Technical Deep Dive

```text
PDF
  -> extracted text
  -> cleaned text
  -> canonical skills from aliases
  -> TF-IDF vectors
  -> cosine similarity
  -> required/resume skill sets
  -> skill match percentage
  -> 40/60 weighted screening score
  -> batch ranking and failure separation
  -> Pandas DataFrame
  -> NumPy statistics
  -> Matplotlib screening/ranking charts
  -> optional GenAI feedback from the existing result
```

The analyzer owns the per-resume calculation. `matcher.py` owns TF-IDF and cosine similarity, `skill_extractor.py` owns aliases, and `scorer.py` owns the weighted formula. `batch_screening.py` adds multi-file handling and ranking. `app.py` orchestrates input and presentation but does not duplicate those calculations.

The evaluation module is intentionally outside this pipeline. It takes an existing-style score, applies a threshold, and compares the decision with manual labels. That makes evaluation a separate experiment rather than part of screening.

## L. Limitations and Future Improvements

### Current implementation

- PDF extraction uses available embedded text and does not perform OCR.
- Skill recognition uses a fixed dictionary and simple substring aliases.
- TF-IDF is word-based and does not capture all semantic relationships.
- The 40/60 score is a ranking heuristic, not accuracy or a hiring decision.
- Evaluation uses a small synthetic/manual dataset, not real-world validation data.
- OpenAI feedback is optional, can fail or be unavailable, and must use only supplied facts.
- The application has no classifier, embeddings, RAG, database, authentication, Docker, REST API, or deployment infrastructure.

### Possible future improvements

- Add OCR for scanned-image resumes.
- Improve skill matching with token boundaries and a maintained skill ontology.
- Add privacy-aware, representative labeled data and a stronger evaluation protocol.
- Study whether the fixed weights are appropriate before changing the formula.
- Explore embeddings or a classifier only after obtaining suitable data and defining safeguards.
- Improve optional AI feedback presentation while preserving the downstream-only boundary.
- Add deployment and access controls only as a separate, security-reviewed project stage.
