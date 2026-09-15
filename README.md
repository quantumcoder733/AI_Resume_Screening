# AI Resume Screening

## 1. Project Overview

AI Resume Screening is a beginner-friendly Python application that compares one or more PDF resumes with a job description. Recruiters often need to read many resumes and manually check whether each candidate has relevant skills. This project helps organize that first comparison by calculating text similarity, checking listed skills, and ranking candidates with an explainable score.

The application is useful as a screening aid for students, recruiters, or hiring teams who want a quick, consistent first-pass comparison. It does not make hiring decisions. A person should review every result and use the score as one input alongside experience, projects, communication, and other job-relevant evidence.

## 2. Problem Statement

Recruiters may receive many resumes for a single role. Manually comparing every resume with a job description takes time and can be inconsistent. This system extracts text from PDF resumes, identifies known skills, measures how similar the resume text is to the job description, and ranks candidates based on those signals.

## 3. Project Objective

The objective is to build a simple, explainable resume-screening tool that:

- Accepts one or more PDF resumes and a job description.
- Extracts and cleans resume text.
- Identifies matched and missing skills from a defined skill list.
- Compares resume and job-description text using TF-IDF and cosine similarity.
- Calculates a weighted screening score and ranks successful candidates.
- Uses Pandas and NumPy to present candidate results and basic score statistics.
- Uses Matplotlib to display simple screening and ranking visualizations.

## 4. Technologies Used

| Technology | What it is | Why this project uses it |
| --- | --- | --- |
| Python | General-purpose programming language | Implements the application logic, functions, modules, file handling, and tests. |
| pypdf | Python PDF-reading library | Extracts available text from uploaded resume PDFs. |
| NumPy | Numerical computing library | Creates rank values and calculates score statistics such as mean, minimum, maximum, and standard deviation. |
| Pandas | Data-analysis library | Converts batch results into a sortable candidate DataFrame. |
| Matplotlib | Python plotting library | Creates simple overall-score and score-comparison charts from the candidate DataFrame. |
| Jupyter Notebook | Interactive document format for Markdown, code, and output | Provides a focused learning companion for the project's data-science workflow. |
| scikit-learn | Machine-learning and data-processing library | Provides `TfidfVectorizer` and `cosine_similarity`. |
| TF-IDF | Text feature-extraction technique from scikit-learn | Converts resume and job-description words into numerical vectors. |
| Cosine similarity | Numerical similarity measure from scikit-learn | Compares the two TF-IDF vectors. |
| Streamlit | Python web-interface library | Provides the single-page upload and results interface. |
| Google GenAI Python SDK | Official Python client for Google's Gemini API | Optionally generates natural-language explanations of existing screening results. |
| pytest | Python testing framework | Runs the automated tests for the core analysis and Stage 1 helpers. |
| Git and GitHub | Version control and hosted repository tools | The project is a Git repository with a configured GitHub remote. |

NLTK and spaCy are not used in the current project.

## 5. Complete Project Architecture

```text
Resume PDF(s) + Job Description
            |
            v
      PDF Text Extraction
            |
            v
         Text Cleaning
            |
            +--------------------+
            |                    |
            v                    v
    Skill Extraction       TF-IDF Vectors
            |                    |
            v                    v
     Skill Matching      Cosine Similarity
            |                    |
            +---------+----------+
                      |
                      v
     Weighted Score (40% similarity + 60% skill match)
                      |
                      v
       Batch Ranking + Pandas/NumPy Analysis
                      |
                      v
      Matplotlib Screening/Ranking Charts
                      |
                      v
             Streamlit Results Page
                      |
                      v
        Optional GenAI Explanation (no score changes)
```

1. **PDF text extraction:** `pypdf` reads each PDF and joins available text from its pages.
2. **Text cleaning:** repeated whitespace and line breaks are normalized into single spaces.
3. **Skill extraction:** the project searches text for skills and supported aliases from its built-in skill dictionary.
4. **TF-IDF:** the resume and job description become numeric word-feature vectors.
5. **Cosine similarity:** the numeric vectors are compared to produce resume similarity as a percentage.
6. **Skill matching:** skills found in both texts are matched; job-description skills absent from the resume are marked missing.
7. **Weighted score:** similarity contributes 40% and skill coverage contributes 60%.
8. **Pandas/NumPy analysis:** successful candidates are sorted in a DataFrame and score statistics are calculated.
9. **Matplotlib charts:** visualize overall screening scores and the similarity/skill-match comparison.
10. **Streamlit:** displays the ranking, statistics, charts, and matched/missing skills.
11. **Optional GenAI feedback:** receives an already-computed candidate result and explains it in natural language. It does not calculate scores or change ranking.

The repository also includes a separate Jupyter Notebook learning companion. It demonstrates the DataFrame, NumPy, Matplotlib, TF-IDF, and cosine-similarity workflow with clearly labeled synthetic data. It is not part of the Streamlit application flow.

## 6. Folder Structure

```text
AI_Resume_Screening/
├── app.py
├── requirements.txt
├── .gitignore
├── data/
│   ├── resumes/
│   │   └── resume1.pdf
│   └── evaluation/
│       ├── sample_labeled_results.csv
│       └── synthetic_screening_evaluation.csv
├── notebooks/
│   └── resume_screening_analysis.ipynb
├── docs/
│   └── INTERVIEW_PREPARATION.md
├── Resume generator/
│   └── ResumeCreator.py
├── src/
│   ├── __init__.py
│   ├── ai_feedback.py
│   ├── analyzer.py
│   ├── batch_screening.py
│   ├── evaluation.py
│   ├── matcher.py
│   ├── pdf_extractor.py
│   ├── results_analysis.py
│   ├── scorer.py
│   ├── skill_extractor.py
│   ├── text_cleaner.py
│   └── visualizations.py
└── tests/
    ├── test_analyzer.py
    ├── test_ai_feedback.py
    ├── test_evaluation.py
    ├── test_results_analysis.py
    └── test_visualizations.py
```

| File or folder | Purpose, input, output, and connection |
| --- | --- |
| `app.py` | Streamlit user interface. It accepts PDF uploads and a job description, calls batch screening, then displays results. |
| `src/analyzer.py` | Single-resume analysis pipeline. Input: a resume path and job description. Output: similarity, skill match, overall score, matched skills, and missing skills. |
| `src/pdf_extractor.py` | Input: PDF path. Output: available text joined from all PDF pages. Used by `analyzer.py`. |
| `src/text_cleaner.py` | Input: raw text. Output: text with repeated whitespace normalized. Used before matching. |
| `src/skill_extractor.py` | Input: text. Output: canonical skills found through its built-in aliases. Used for resume and job-description skills. |
| `src/matcher.py` | Input: cleaned resume text and cleaned job description. Output: TF-IDF cosine similarity percentage. |
| `src/scorer.py` | Input: similarity and skill-match scores. Output: the 40/60 weighted overall score. |
| `src/results_analysis.py` | Input: successful batch candidate dictionaries. Output: ranked Pandas DataFrame and NumPy-based statistics. |
| `src/visualizations.py` | Input: the ranked candidate DataFrame. Output: reusable Matplotlib figures for overall screening scores and similarity/skill-match comparison. |
| `src/evaluation.py` | A separate evaluation experiment. It applies a fixed threshold to existing overall scores and compares the resulting decisions with manual labels. |
| `src/ai_feedback.py` | Optional Gemini integration. Input: an existing candidate result and optional job description. Output: concise explanatory feedback, or a safe unavailable message. |
| `notebooks/resume_screening_analysis.ipynb` | A separate, focused data-science learning notebook. It uses synthetic demonstration results to show DataFrames, statistics, charts, TF-IDF, cosine similarity, and score terminology. |
| `docs/INTERVIEW_PREPARATION.md` | Interview study guide based on the implemented screening, evaluation, and optional GenAI components. |
| `Resume generator/ResumeCreator.py` | Separate optional PDF resume-generation utility; it is not part of the screening application flow. |
| `src/batch_screening.py` | Input: PDF paths and a job description. Output: ranked successful candidates plus failures. It calls `analyzer.py` once per PDF. |
| `tests/` | Automated tests for PDF extraction, analysis result structure, ranking, failure preservation, text cleaning, DataFrames, statistics, charts, evaluation metrics, and mocked AI feedback. |
| `data/evaluation/sample_labeled_results.csv` | Small synthetic/manual candidate results used by the separate threshold-based evaluation experiment. |
| `requirements.txt` | Declares the Python packages required by the project. |
| `.gitignore` | Prevents virtual environments, caches, coverage files, build files, notebook checkpoints, and `.env` files from being committed. |

## 7. How the Application Works

1. The user enters a job description and uploads one or more PDF resumes in Streamlit.
2. `app.py` stores each upload in a temporary directory for the duration of the request.
3. `screen_resume_paths` processes each file independently.
4. `analyze_resume` extracts and cleans its text, finds skills, calculates similarity, and calculates the overall score.
5. Successful candidates are sorted by overall score. Failures are recorded without stopping successful files.
6. `results_analysis.py` creates a DataFrame and calculates score statistics.
7. `visualizations.py` builds two Matplotlib figures from the same DataFrame: overall screening score by candidate, and resume similarity versus skill match.
8. Streamlit displays the ranking, average/highest/lowest scores, standard deviation, screening/ranking charts, and each candidate's matched and missing skills.

**Streamlit is the user interface.** It collects input and shows output. The backend modules in `src/` perform the actual PDF processing, text analysis, scoring, ranking, and numerical analysis.

## 8. PDF Text Extraction

Computers cannot compare a PDF directly as meaningful language. The resume PDF must first be converted into text. `pdf_extractor.py` uses `pypdf.PdfReader` and joins the text returned from every page. If a page has no extractable text, the code uses an empty string for that page.

For an unreadable or corrupt PDF, `pypdf` can raise an error. In the batch pipeline that error is caught for that candidate, recorded as a failure, and shown in the UI while valid candidates continue. The current project does not perform OCR, so scanned-image PDFs may not provide useful text.

## 9. Text Cleaning

PDF extraction often produces extra spaces, tabs, and line breaks. `text_cleaner.py` replaces any run of whitespace with one space and removes whitespace at the beginning and end.

```text
Before: " Python\n\n  SQL\tPandas "
After:  "Python SQL Pandas"
```

Cleaning happens before skill extraction and TF-IDF so those later steps receive more consistent text. It is deliberately small: it does not remove stop words, stem words, or use an external NLP library.

## 10. Skill Extraction and Matching

`skill_extractor.py` contains a fixed dictionary of canonical skill names and aliases. For example, `scikit-learn` can be detected from `scikit-learn`, `scikit learn`, or `sklearn`; `c++` can be detected from `c++` or `cpp`; and `aws` can be detected from `aws` or `amazon web services`.

The text is lowercased, then each alias is checked with a simple substring search. The analyzer turns the resume and job-description skill lists into sets:

```text
Resume skills:       {python, pandas, sql}
Required skills:     {python, sql, numpy}
Matched skills:      {python, sql}
Missing skills:      {numpy}
```

This is explainable and easy to understand, but it only knows skills present in the dictionary and does not understand context. For example, it may not distinguish a skill used in a project from a skill merely mentioned in a sentence.

## 11. TF-IDF

TF-IDF means **Term Frequency-Inverse Document Frequency**. It turns text into numerical features.

- **Term frequency (TF):** how often a word appears in one document.
- **Inverse document frequency (IDF):** gives less importance to words that appear in many documents and more importance to words that help distinguish documents.

In this project, the two documents are the cleaned resume and cleaned job description. `TfidfVectorizer` learns a vocabulary from those two texts and creates one numeric vector for each text. A vector is simply a list of numbers representing word importance.

Small example:

```text
Resume:          "python pandas sql"
Job description: "python sql machine learning"
Vocabulary:       [python, pandas, sql, machine, learning]
```

Both texts receive values for the same vocabulary, so they can be compared numerically. TF-IDF is not a trained predictive hiring model here. It is feature extraction performed for the two texts in the current screening request.

## 12. Cosine Similarity

Cosine similarity measures how closely two numeric vectors point in the same direction. In simple terms, it checks how similar the important words in the resume are to the important words in the job description.

If two documents emphasize many of the same words, their vectors are more aligned and the similarity is higher. If they share few relevant words, the similarity is lower. The project multiplies scikit-learn's 0-to-1 result by 100 to display a percentage.

Example: a resume containing `python`, `sql`, and `pandas` will generally be more similar to a Python data role than a resume that contains only unrelated terms. Similarity is still not proof of suitability: wording, extracted text quality, and missing context all affect it.

## 13. Skill Match Score

The actual calculation is:

```text
Skill Match (%) = (number of matched required skills / number of required skills) * 100
```

Example: if the job description contains four recognized required skills and the resume contains three of them:

```text
Skill Match = (3 / 4) * 100 = 75%
```

If the job description contains no skills recognized by the current dictionary, the code returns a skill-match score of `0`. The skill dictionary is intentionally explicit, so users can see which skills are recognized.

## 14. Final Scoring Formula

```text
Overall Score = (Resume Similarity * 0.40) + (Skill Match * 0.60)
```

For example, with 50% resume similarity and 75% skill match:

```text
Overall Score = (50 * 0.40) + (75 * 0.60) = 65%
```

The project gives skill coverage more weight because it is a direct, explainable comparison with the skills recognized in the job description. This is a **weighted screening score**, not model accuracy. It has not been validated against labeled hiring outcomes, and it should not be described as accuracy in an interview.

## 15. Pandas

Pandas is a Python library for working with tabular data. A **DataFrame** is similar to a spreadsheet: rows represent candidates and columns represent their scores.

`create_candidate_dataframe` creates the following columns, sorts by `Overall Score` in descending order, and adds a rank:

| Rank | Candidate | Resume Similarity | Skill Match | Overall Score |
| ---: | --- | ---: | ---: | ---: |
| 1 | candidate_a.pdf | 68.20 | 80.00 | 75.28 |
| 2 | candidate_b.pdf | 55.10 | 60.00 | 58.04 |

The values above are an illustrative example, not stored project output. The DataFrame makes candidate ranking and comparison easier than manually reading a list of dictionaries.

## 16. NumPy

NumPy is a Python library for numerical operations. After Pandas creates the candidate table, the project converts the `Overall Score` column into a NumPy array. It then calculates:

- **Mean:** the average candidate score.
- **Minimum:** the lowest score.
- **Maximum:** the highest score.
- **Standard deviation:** how spread out the scores are.

For scores `[52, 72]`, the mean is `62`, the minimum is `52`, the maximum is `72`, and the population standard deviation is `10`. NumPy is used because these operations are clear and reliable for numeric data.

## 17. Matplotlib Visualizations

Matplotlib is a Python library for creating charts. The project uses it only after candidate screening results have already been calculated and converted to a Pandas DataFrame. The charts do not change the scores or perform a new ML calculation.

`visualizations.py` provides two reusable functions:

- `create_overall_score_chart`: a bar chart showing each candidate's overall screening score.
- `create_similarity_skill_match_chart`: a grouped bar chart comparing each candidate's resume-similarity and skill-match scores.

Both charts use a 0-to-100 score axis and are displayed on the same single Streamlit page below the score statistics. They are **screening/ranking visualizations, not accuracy charts**. The overall score remains the existing 40% similarity plus 60% skill-match calculation.

## 18. Data-Science Notebook

`notebooks/resume_screening_analysis.ipynb` is a focused companion for learning the data-science workflow outside the web interface. It is not a second Streamlit application and it does not change the analyzer or score calculation.

It is a standard Jupyter Notebook JSON document that can be opened in VS Code or Jupyter. Each notebook section uses Markdown explanations and Python examples so beginners can follow the workflow from candidate results to charts and text similarity.

The notebook:

- Imports the existing DataFrame, statistics, and visualization helpers.
- Uses clearly labeled synthetic candidate screening results, not real applicant or hiring data.
- Builds and inspects the ranked Pandas DataFrame.
- Calculates mean, minimum, maximum, and standard deviation with NumPy.
- Reuses the two simple Matplotlib screening/ranking figures.
- Demonstrates TF-IDF and cosine similarity with a small, separate text example.
- Explains why similarity, skill match, weighted screening score, and model accuracy are different concepts.

## Evaluation Metrics - Separate Demonstration

Evaluation metrics are kept separate from the current screening algorithm. The existing score remains the ranking heuristic:

```text
Overall Score = (Resume Similarity * 0.40) + (Skill Match * 0.60)
```

`data/evaluation/sample_labeled_results.csv` is a small synthetic/manual dataset containing a candidate, an existing-style `screening_score`, and an `actual_label` of `suitable` or `not_suitable`. It is for learning only and is not a real-world validation dataset.

`src/evaluation.py` applies a chosen threshold, predicts `suitable` when the screening score reaches that threshold, and compares those predictions with the manually assigned labels. It reports:

- **Accuracy:** how many predictions were correct overall.
- **Precision:** among candidates predicted suitable, how many were actually suitable.
- **Recall:** among actually suitable candidates, how many were identified as suitable.
- **F1-score:** a combined measure of precision and recall.

These metrics evaluate threshold-based decisions against labeled examples. They do not mean the existing screening score is 40% accurate or 60% accurate. This experiment does not add a trained classification model, train/test split, or new screening behavior.

## Generative AI - Optional Candidate Feedback

The optional GenAI feature follows this architecture:

```text
Resume -> Existing analysis -> Screening result -> Optional GenAI explanation
```

The existing system remains the source of truth:

- **Traditional NLP-style analysis:** TF-IDF, cosine similarity, dictionary-based skill matching, and the deterministic 40% similarity + 60% skill-match score.
- **Generative AI:** natural-language explanation of the supplied result, candidate strengths, matched and missing skills, and practical resume suggestions.

When the user clicks **Generate AI Feedback** for a displayed candidate, `src/ai_feedback.py` sends only the existing candidate fields, such as matched skills, missing skills, resume similarity, skill match, overall screening score, and optional job-description text. The prompt tells Gemini not to invent skills or experience and not to calculate or change scores. Gemini is never used for ranking or screening.

The API key must be supplied through the `GEMINI_API_KEY` environment variable and is never hardcoded. Local development can load it from `.env` or the ignored `key.env` fallback. The integration uses Google's `gemini-2.5-flash` model. If the key is missing, or if a Gemini response fails or is malformed, the existing screening result remains available and the UI shows a clear status message. The feature is optional and does not call Gemini automatically for every resume.

The notebook uses a synthetic mock payload only, so it executes without an API key. `tests/test_ai_feedback.py` mocks the Gemini client and makes no network calls.

## 19. Batch Resume Screening

The UI accepts multiple PDFs. `batch_screening.py` loops through the uploaded file paths, validates that each path is a PDF and exists, then calls the single-resume analyzer for every valid path.

Successful candidate results are stored with their filenames and sorted by overall score. If one candidate fails, such as because its PDF cannot be read, the failure is stored with its filename and error message. The remaining valid resumes are still ranked and displayed.

## 20. Streamlit UI

The current UI is intentionally one page and beginner-friendly. It contains:

- **Title:** identifies the application.
- **Job-description input:** a text area for role requirements and desired skills.
- **PDF uploader:** accepts one or more PDF resumes.
- **Screen Resumes button:** starts screening after validating both inputs.
- **Results:** shows success or warning/error messages.
- **Ranking table:** displays the Pandas candidate DataFrame.
- **Score statistics:** shows average, highest, lowest, and standard-deviation values.
- **Screening and ranking visualizations:** shows an overall-score chart and a similarity-versus-skill-match chart.
- **Skill details:** shows matched and missing skills for each candidate.

There are no UI tabs, custom CSS, session state, or accuracy charts in the current version. The optional AI-feedback button appears for each displayed candidate and runs only when clicked.

## 21. Testing

Tests protect expected behavior when the project changes. pytest discovers and runs the tests in `tests/`.

The current tests verify:

- The sample PDF returns extractable text.
- A single analysis returns the expected serializable fields and valid score range.
- Directory screening uses the sample resume and ranks results.
- Batch screening sorts candidates correctly.
- One failing candidate does not remove successful candidates.
- Text cleaning normalizes whitespace.
- The DataFrame has expected columns and rank order.
- NumPy statistics are calculated correctly.
- Empty DataFrames are handled safely.
- The overall-score chart uses the candidate overall scores.
- The comparison chart includes separate similarity and skill-match series.
- Threshold-based evaluation compares screening decisions with synthetic/manual labels using accuracy, precision, recall, and F1-score.

The latest validation result for this version was **`21 passed`**. That means all twenty-one automated test functions completed successfully. It does not mean the screening score has 100% real-world accuracy.

## 22. Error Handling

- The UI warns when no resume is uploaded or no job description is entered.
- The uploader only accepts files with a `.pdf` extension; the batch backend also checks the file extension and whether the file exists.
- A PDF-analysis exception for one candidate becomes a `ScreeningFailure`; valid candidates continue to be processed.
- If no candidate can be analyzed, the UI shows an error message.
- Uploaded files are written inside `TemporaryDirectory`, which is cleaned up after processing.
- The current code does not have a separate, custom message for an empty-text PDF. If empty text causes analysis to fail, batch screening records that candidate as a failure.

## 23. Security and Good Practices

- Uploads are stored temporarily, not in the project data folder.
- Each upload receives a separate temporary subdirectory so duplicate filenames do not overwrite one another during a request.
- The temporary directory is automatically cleaned up.
- `.gitignore` excludes virtual environments, cache files, test/coverage output, build output, notebook checkpoints, and `.env` files.
- The optional Gemini integration reads `GEMINI_API_KEY` from the environment and never hard-codes or displays credentials.
- The UI displays candidate filenames, not temporary filesystem paths.

## 24. Current Limitations

- This is not a trained classification model and does not predict hiring outcomes.
- The weighted score is a ranking heuristic, not accuracy. The separate evaluation experiment uses a small synthetic/manual dataset and is not real-world validation.
- GenAI feedback depends on optional API access and can be unavailable or imperfect; it must not be treated as a source of new candidate facts.
- The skill list is fixed in source code and uses simple substring matching.
- TF-IDF compares word importance, not deep semantic meaning.
- The project does not use embeddings, OCR, a database, authentication, or interactive chart controls. It uses the optional Gemini API only for natural-language feedback.
- Scanned PDF resumes may have little or no extractable text because OCR is not implemented.
- The tool does not automatically accept, reject, or hire candidates.

## 25. Syllabus Mapping

| Syllabus area | Status | Current connection |
| --- | --- | --- |
| Python foundations | Directly used | Functions, modules, conditionals, loops, lists, dictionaries, sets, exceptions, dataclasses, and file paths. |
| Jupyter Notebook | Directly used | A focused notebook demonstrates the project's data-science workflow with synthetic sample data. |
| NumPy arrays and operations | Directly used | Converts overall scores to NumPy arrays and calculates statistics. |
| Pandas DataFrames | Directly used | Builds and ranks the candidate comparison DataFrame. |
| Data cleaning | Directly used | Normalizes PDF-extracted whitespace before matching. |
| Matplotlib visualization | Directly used | Creates two simple candidate screening/ranking charts from the Pandas DataFrame. |
| Machine-learning workflow | Indirectly used | Inputs are transformed into features and compared, but there is no train/test dataset. |
| Linear regression | Not currently used | The project does not predict a continuous target from training data. |
| Classification algorithms | Not currently used | The project does not train a classifier. |
| Model evaluation metrics | Used in a separate experiment | A threshold converts existing screening scores into decisions that are compared with synthetic/manual labels using accuracy, precision, recall, and F1-score. This does not train a classifier. |
| Clustering/recommendation | Not currently used | The project does not cluster candidates or recommend jobs. |
| Generative AI and LLMs | Used optionally | Gemini explains supplied screening results in natural language; it does not score or rank candidates. |
| API integration/automation | Used optionally | The official Google GenAI SDK is called only after a user requests feedback and only when an environment key is configured. |
| Streamlit capstone development | Directly used | Streamlit provides the application interface for the capstone. |
| Git/GitHub | Directly used | The project is version-controlled with a configured GitHub remote. |

## 26. Interview Questions and Answers

### A. Basic Project Questions

**1. What problem does your project solve?**  
**Short answer:** It helps compare PDF resumes with a job description and ranks candidates using text relevance and skill coverage.  
**Deeper explanation:** The project reduces repetitive first-pass comparison. It extracts resume text, checks known skills, measures TF-IDF similarity, and presents an explainable score rather than making a final hiring decision.

**2. What is the input and output?**  
**Short answer:** The input is one or more PDF resumes plus a job description; the output is ranked candidates, scores, and matched/missing skills.  
**Deeper explanation:** The backend returns similarity, skill match, overall score, sorted matched skills, and sorted missing skills for each successful file. Batch results also keep failures separately.

**3. Is this an automated hiring system?**  
**Short answer:** No. It is an assistive screening and ranking tool.  
**Deeper explanation:** Its score uses only text and a fixed skill list, so it cannot evaluate the full context of a candidate. A human must review the resume and make decisions.

### B. Python Questions

**4. Why did you separate the project into modules?**  
**Short answer:** Each module has one clear responsibility, which makes the code easier to understand and test.  
**Deeper explanation:** For example, PDF extraction is separate from scoring, and Pandas analysis is separate from the Streamlit UI. This limits the effect of a change and allows reusable functions to be tested independently.

**5. Why are sets used for skills in `analyzer.py`?**  
**Short answer:** Sets make intersection and difference operations simple and remove duplicates.  
**Deeper explanation:** `resume_skills & required_skills` gives matched skills, while `required_skills - resume_skills` gives missing skills. The result is converted back to sorted lists for a stable, serializable output.

**6. How does the batch code handle a failure?**  
**Short answer:** It catches the exception for that candidate, saves a failure record, and continues processing the other files.  
**Deeper explanation:** This is important for batch work because one corrupt PDF should not prevent valid resumes from being ranked.

### C. PDF and Text Processing Questions

**7. Why do you extract PDF text first?**  
**Short answer:** Text analysis needs words, while a PDF is a document container rather than directly comparable text.  
**Deeper explanation:** `pypdf` reads each page and returns available text, which then becomes input for cleaning, skill extraction, and TF-IDF.

**8. What happens with scanned-image PDFs?**  
**Short answer:** They may not produce useful text because this project does not use OCR.  
**Deeper explanation:** `pypdf` extracts embedded PDF text; it does not read words from an image. OCR would be future work.

**9. Why is text cleaning needed?**  
**Short answer:** PDF extraction can create extra spaces, tabs, and line breaks that make downstream text less consistent.  
**Deeper explanation:** The cleaner normalizes whitespace while preserving the words. It is a small, explainable preprocessing step.

### D. NLP Questions

**10. What NLP is used in this project?**  
**Short answer:** Basic text preprocessing, dictionary-based skill extraction, TF-IDF features, and cosine similarity.  
**Deeper explanation:** The project does not use a large NLP model, NLTK, or spaCy. Its NLP approach is deliberately lightweight and explainable.

**11. How are skills extracted?**  
**Short answer:** The project searches lowercased text for aliases in a built-in skill dictionary.  
**Deeper explanation:** For instance, `sklearn` is mapped to the canonical skill `scikit-learn`. This makes the displayed result consistent even when common alternate spellings are used.

**12. What is a limitation of substring skill matching?**  
**Short answer:** It can miss skills outside the dictionary and does not understand context.  
**Deeper explanation:** It is transparent but simple. A more advanced system could use token boundaries, a maintained skill ontology, or semantic matching.

### E. TF-IDF Questions

**13. What is TF-IDF?**  
**Short answer:** It is a method that gives each word a numeric importance value in a document.  
**Deeper explanation:** Term frequency measures occurrence in a document, while inverse document frequency reduces the importance of words common across documents. The resulting vectors can be compared.

**14. Why use TF-IDF for resumes?**  
**Short answer:** It is a simple way to compare the important words in a resume and a job description.  
**Deeper explanation:** It works well as an understandable baseline for text relevance and is available in scikit-learn. It does not understand synonyms or sentence meaning as well as embeddings can.

**15. Did you train TF-IDF on a dataset?**  
**Short answer:** No. It fits a vectorizer on the resume and job description for the current comparison.  
**Deeper explanation:** There is no labeled training phase. TF-IDF is used here for feature extraction, not as a predictive model trained on hiring labels.

### F. Cosine Similarity Questions

**16. What does cosine similarity measure?**  
**Short answer:** It measures how aligned two numeric vectors are.  
**Deeper explanation:** After TF-IDF turns both documents into vectors, cosine similarity compares their direction. More shared important terms generally produce a higher value.

**17. Why not just count common words?**  
**Short answer:** TF-IDF plus cosine similarity weighs word importance and compares the whole vector.  
**Deeper explanation:** A simple word count treats every word equally. TF-IDF reduces the effect of less informative shared terms and provides a normalized vector comparison.

**18. Does a high similarity score guarantee a good candidate?**  
**Short answer:** No. It only indicates textual similarity based on extracted words.  
**Deeper explanation:** Experience quality, projects, context, and wording are not fully captured, so the score should guide review rather than replace it.

### G. Pandas and NumPy Questions

**19. Why use a Pandas DataFrame?**  
**Short answer:** It gives the batch results a clear table structure for ranking and comparison.  
**Deeper explanation:** Candidate dictionaries are converted into named columns, sorted by overall score, and assigned ranks before display in Streamlit.

**20. Why use NumPy if Pandas already has statistics?**  
**Short answer:** NumPy is used explicitly for the numerical statistics required in this learning stage.  
**Deeper explanation:** The project converts the score column to a NumPy array and uses `mean`, `min`, `max`, `std`, `argmax`, and `argmin`, making the numerical calculation path clear.

**21. What does standard deviation show here?**  
**Short answer:** It shows how spread out the overall candidate scores are.  
**Deeper explanation:** A low value means scores are close together, while a higher value means candidates vary more according to this scoring heuristic.

### H. Machine Learning Questions

**22. Is this a machine-learning model?**  
**Short answer:** It uses an ML-related text-feature technique, but it is not a trained predictive model.  
**Deeper explanation:** scikit-learn creates TF-IDF features and calculates similarity. The project has no labeled training data, train/test split, classifier, or model-fit evaluation.

**23. Is the overall score accuracy?**  
**Short answer:** No. It is a weighted screening score.  
**Deeper explanation:** Accuracy requires predictions compared with known labels. This project combines two calculated percentages and has not evaluated those scores against hiring outcomes.

**24. What data would you need to evaluate it properly?**  
**Short answer:** A carefully labeled dataset of resume-job pairs and an agreed suitability label.  
**Deeper explanation:** With ethical, privacy-aware labels, a chosen threshold could be evaluated using accuracy, precision, recall, and F1. That would be a separate evaluation task.

### I. Streamlit Questions

**25. What does Streamlit do in your project?**  
**Short answer:** It provides the web interface for entering a job description, uploading PDFs, and seeing results.  
**Deeper explanation:** It does not contain the core scoring logic. It calls backend modules and renders their returned data.

**26. How does the UI support one and multiple resumes?**  
**Short answer:** It uses one multi-file uploader, so the same flow works for one or more PDFs.  
**Deeper explanation:** All uploads go to the batch pipeline. A single uploaded PDF simply produces a batch result with one candidate.

**27. Why keep the UI simple?**  
**Short answer:** A simple interface makes the workflow clear and keeps attention on the analysis.  
**Deeper explanation:** The current page avoids tabs, custom CSS, session state, and advanced dashboard elements so the implementation remains explainable for the project scope.

### J. Testing and Git Questions

**28. What does your test suite cover?**  
**Short answer:** It covers extraction, analysis result fields, ranking, failure handling, cleaning, DataFrame creation, and statistics.  
**Deeper explanation:** The tests focus on reusable backend behavior rather than trying to automate every visual detail of the Streamlit interface.

**29. What does a passing pytest result mean?**  
**Short answer:** All current pytest test functions ran successfully.  
**Deeper explanation:** It increases confidence that tested behavior works, but it does not prove every possible PDF or real-world screening situation will work perfectly.

**30. Why use Git and GitHub?**  
**Short answer:** Git tracks changes, and GitHub stores and shares the repository.  
**Deeper explanation:** They make it easier to review development history, collaborate, recover earlier versions, and present the project professionally.

### K. Project Design Questions

**31. Why is the scoring logic in a separate module?**  
**Short answer:** It keeps the 40/60 formula easy to find, explain, test, and change intentionally.  
**Deeper explanation:** `scorer.py` has one responsibility. The UI and analysis pipeline call it instead of duplicating the formula.

**32. Why do you have both single analysis and batch screening code?**  
**Short answer:** The single analyzer is reusable core logic, and batch screening adds looping, sorting, and failure handling.  
**Deeper explanation:** This separation avoids duplicating extraction and scoring behavior for each uploaded file.

**33. Why are failures stored separately from candidates?**  
**Short answer:** It lets the user see what failed without losing valid results.  
**Deeper explanation:** The `BatchScreeningResult` contains a candidate list and a failure list, making the batch outcome explicit and resilient.

### L. Difficult Follow-up Questions

**34. Could the skill dictionary produce false matches?**  
**Short answer:** Yes, because it uses simple substring matching.  
**Deeper explanation:** The current approach is easy to understand but does not check grammatical context or all word boundaries. Improving matching would require careful tests so it does not create new errors.

**35. Why is skill match weighted more than similarity?**  
**Short answer:** The project uses 60% skill match because direct required-skill coverage is an explicit and explainable signal.  
**Deeper explanation:** This is a project design decision, not a scientifically validated optimum. The formula remains visible in `scorer.py` and should be reviewed with real stakeholder feedback before use in practice.

**36. How would you improve this project responsibly?**  
**Short answer:** I would add better skill matching and a labeled evaluation dataset before considering a predictive model.  
**Deeper explanation:** Any improvements should preserve privacy, avoid automatic hiring decisions, test for bias and errors, and keep explanations available to users.

## 27. Explain My Project in 30 Seconds

"I built an AI Resume Screening application in Python that compares PDF resumes with a job description. It extracts and cleans resume text, checks for recognized skills, uses TF-IDF and cosine similarity to measure text relevance, and calculates an explainable score using 40% similarity and 60% skill match. For multiple resumes, it ranks candidates in a Pandas DataFrame and uses NumPy for score statistics. It is a screening aid, not a hiring decision system."

## 28. Explain My Project in 2 Minutes

"My project is an AI Resume Screening tool designed to help with the first stage of comparing resumes to a job description. A user enters a job description and uploads one or more PDF resumes through a simple Streamlit page. The application temporarily stores the uploads, extracts available text using pypdf, and cleans repeated whitespace.

Then it performs two comparisons. First, it uses a fixed skill dictionary with aliases, such as `sklearn` for `scikit-learn`, to find skills in both the resume and the job description. This gives matched and missing skills and a skill-match percentage. Second, it uses scikit-learn's TF-IDF vectorizer to convert the resume and job description into numerical word vectors. Cosine similarity compares those vectors and produces a text-similarity percentage.

The final score is a transparent weighted calculation: 40% resume similarity and 60% skill match. For batch screening, the project ranks valid candidates, keeps failures separate so one bad PDF does not stop the others, and displays a Pandas table. NumPy calculates the average, highest, lowest, and standard deviation of scores, while Matplotlib shows two simple screening/ranking charts. I use pytest to test the main pipeline, data-analysis helpers, and chart functions. I would describe it as an explainable screening and ranking tool, not a trained model or an automated hiring system."

## 29. Explain My Project Technically

"The application has a single-page Streamlit frontend and a modular Python backend. Uploaded PDFs are written to a `TemporaryDirectory` and passed to `screen_resume_paths`. For each path, the batch layer validates the file, invokes `analyze_resume`, collects a success dictionary or `ScreeningFailure`, and sorts successes by overall score.

The analyzer calls `PdfReader` through `extract_text_from_pdf`, applies regex whitespace normalization, and runs dictionary-based alias extraction for both texts. It calculates skill coverage as `|resume_skills intersection required_skills| / |required_skills| * 100`, defaulting to zero when no required skills are recognized. In parallel, scikit-learn's `TfidfVectorizer` fits on the resume and job-description pair, and `cosine_similarity` compares their sparse TF-IDF vectors. The score module returns `0.40 * similarity + 0.60 * skill_match`.

For presentation, successful candidate dictionaries become a Pandas DataFrame sorted descending by overall score. NumPy calculates population standard deviation and identifies min/max positions. Matplotlib receives that same DataFrame and returns two figures without changing its values. Tests cover extraction, output contract, ranking, per-file failure isolation, cleaning, DataFrame construction, numerical statistics, and chart data/labels."

## 30. Important Interview Concepts

| Concept | Quick revision |
| --- | --- |
| NLP | Processing human language as text. Here it means cleaning text, extracting known skills, TF-IDF, and similarity. |
| TF-IDF | Numeric importance representation of words in documents; not a trained classifier by itself. |
| Cosine similarity | Measures alignment of TF-IDF vectors; higher generally means more word-level relevance. |
| Skill matching | Set intersection for matched recognized skills and set difference for missing recognized skills. |
| Weighted scoring | Combines two signals using the fixed formula: 40% similarity and 60% skill match. |
| Pandas DataFrame | Table used to compare and rank batch candidates. |
| NumPy | Numerical array library used for statistics on overall scores. |
| Matplotlib | Plotting library used to show screening/ranking scores; its charts are not accuracy measurements. |
| Jupyter Notebook | Learning companion that combines Markdown explanations and code cells; it uses synthetic demonstration data. |
| Streamlit | Interface layer; it does not perform the core analysis itself. |
| Train/test split | A method for evaluating trained models on unseen labeled data; it is not used here because no trained model or labeled dataset exists. |
| Classification vs. similarity | Classification predicts predefined labels from training data. Similarity compares how alike two texts are. This project does similarity, not classification. |
| Accuracy vs. screening score | Accuracy compares predictions with known labels. The overall screening score is a heuristic combination of two calculated values, not accuracy. |

## 31. Common Mistakes to Avoid in an Interview

- Do not call the weighted overall score "accuracy."
- Do not say that you trained a classification model.
- Do not claim the tool makes hiring, rejection, or suitability decisions.
- Do not claim that NLTK, spaCy, embeddings, or OCR are implemented. Gemini is optional feedback only, not a scoring or ranking system.
- Do not claim that the notebook uses real applicant or hiring data.
- Do not call the Matplotlib screening/ranking charts "accuracy charts."
- Do not say TF-IDF understands meaning like a human; it is a word-based feature representation.
- Do not say every PDF works; scanned or corrupt PDFs can fail or yield little text.
- Do not hide limitations of the fixed skill dictionary or simple substring matching.

## 32. Future Improvements

The following are **future work**, not current features:

- Add OCR support for scanned PDF resumes.
- Improve the skill ontology and use more precise matching rules.
- Add semantic embeddings to compare meaning beyond shared words.
- Create a privacy-aware labeled evaluation dataset and measure suitable threshold decisions.
- Explore a classification model only after obtaining appropriate labeled data and evaluation practices.
- Improve the optional AI feedback prompts and response presentation while keeping the API boundary secure.
- Add interactive visualization controls or deployment after the core workflow is evaluated.

## 33. Commands

Run these commands from the project root in PowerShell:

```powershell
# Activate the existing virtual environment
.\venv\Scripts\Activate.ps1

# Install the declared dependencies
.\venv\Scripts\python.exe -m pip install -r requirements.txt

# Run the Streamlit application
.\venv\Scripts\python.exe -m streamlit run app.py

# Run tests without creating a pytest cache
.\venv\Scripts\python.exe -m pytest -q -p no:cacheprovider

# Check that the Streamlit file compiles
.\venv\Scripts\python.exe -m py_compile app.py
```

If PowerShell blocks activation because of an execution policy, the other commands still use the virtual environment directly and do not require activation.

## 34. Development History

The repository history and current code show these development stages:

1. Project setup with Python package structure, dependencies, tests, and Git repository.
2. PDF text extraction using pypdf.
3. Dictionary-based skill extraction and alias support.
4. TF-IDF feature extraction and cosine-similarity comparison.
5. Separate 40/60 weighted scoring module.
6. Streamlit interface for resume uploads and results.
7. Batch screening, ranking, and per-file failure handling.
8. Stage 1 additions: whitespace cleaning plus Pandas/NumPy candidate analysis and tests.
9. Stage 2 additions: reusable Matplotlib screening/ranking charts integrated into Streamlit and covered by focused tests.
10. Stage 3 addition: focused Jupyter Notebook demonstrating the data-science workflow with synthetic example data.
11. Stage 4 addition: separate threshold-based evaluation metrics using synthetic/manual labels.
12. Stage 5 addition: optional Gemini feedback that explains existing screening results without scoring or ranking.
13. Stage 6 integration check: verified the single-page Streamlit flow and end-to-end batch behavior.
14. Stage 7 cleanup: audited dependencies, documentation, notebook structure, security, and test coverage.

## 35. Final Interview Cheat Sheet

| Topic | Answer |
| --- | --- |
| Problem | Comparing many resumes with a job description is time-consuming. |
| Solution | An explainable PDF-resume screening and ranking tool. |
| Input | One or more PDF resumes and a job description. |
| Output | Ranked candidates, similarity, skill match, overall score, and matched/missing skills. |
| Main technologies | Python, pypdf, scikit-learn, Pandas, NumPy, Matplotlib, Jupyter Notebook, Streamlit, Google GenAI SDK, pytest, Git/GitHub. |
| Main algorithm | TF-IDF vectors compared with cosine similarity, plus dictionary-based skill matching. |
| Scoring | `0.40 * resume similarity + 0.60 * skill match`. |
| Why TF-IDF? | It creates understandable numeric word features for text comparison. |
| Why cosine similarity? | It compares how aligned the TF-IDF text vectors are. |
| Why Pandas? | It creates a sortable candidate comparison table. |
| Why NumPy? | It calculates score statistics efficiently and clearly. |
| Why Matplotlib? | It displays simple screening/ranking charts from the candidate DataFrame. |
| Why Jupyter Notebook? | It teaches and demonstrates the data-science workflow with synthetic example results. |
| Why Streamlit? | It provides a simple interface for uploads, input, and results. |
| Testing | pytest verifies the core analysis, ranking, failure handling, cleaning, analysis helpers, charts, evaluation metrics, and mocked AI feedback; latest run: 21 passed. |
| Main limitation | It is a heuristic, not a trained or evaluated hiring model. |
| Future improvement | Improve skill matching and evaluate against a carefully labeled dataset. |
