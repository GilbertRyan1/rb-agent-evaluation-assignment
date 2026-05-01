# Agent Evaluation Assignment

This repository contains an evaluation pipeline for comparing human survey answers with AI-generated answers. The task is not only to check whether both answers are semantically similar, but also to understand whether the AI answer preserves the specific behaviour, preferences, motivations, details, and response style of the human respondent.

The pipeline uses three evaluation layers:

1. **Semantic similarity** using sentence-transformer embeddings  
2. **LLM-as-judge evaluation** using Gemini  
3. **Content-level comparison** using structured content preservation metrics  

The final outputs are saved as Excel and CSV files under `outputs/`.

---

## Repository Structure

```text
rb-agent-evaluation-assignment/
│
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── assignment_materials/
│   └── RB_GenAI_Assignment.pdf
│
├── data/
│   └── RB_GenAI_Datatest.xlsx
│
├── src/
│   └── agent_eval/
│       ├── __init__.py
│       ├── io_utils.py
│       ├── semantic_similarity.py
│       ├── llm_client.py
│       ├── llm_as_judge.py
│       ├── content_comparison.py
│       ├── prompts.py
│       ├── schemas.py
│       └── analysis.py
│
├── notebooks/
│   └──agent_evaluation_pipeline.ipynb
│
├── outputs/
│
│
└── submission/
```

---

## Setup


If you want to run it, clone the repo : 
```bash
GITHUB_REPO_URL = "https://github.com/GibertRyan1/rb-agent-evaluation-assignment.git"

!rm -rf /content/rb-agent-evaluation-assignment
```
install the required packages:

```bash
pip install -r requirements.txt
```

The main dependencies are:

- `pandas`
- `openpyxl`
- `sentence-transformers`
- `transformers`
- `torch`
- `google-genai`
- `python-dotenv`

---

## API Key

The LLM-as-judge and content-level comparison steps use Gemini.

Create `GEMINI_API_KEY` as an environment variable.

---

## How to Run

Open and run:

```text
notebooks/agent_evaluation_pipeline.ipynb
```

The notebook runs the full pipeline in this order:

1. Load the input Excel file
2. Run semantic similarity scoring
3. Run LLM-as-judge evaluation
4. Run content-level comparison
5. Generate final summary tables
6. Save all outputs under `outputs/`

The notebook uses a short pause between Gemini calls to reduce rate-limit issues.

---

## Evaluation Layers

### 1. Semantic Similarity

This layer compares each human answer with the corresponding AI answer using sentence-transformer embeddings.

It produces:

```text
semantic_similarity_score
```

This score is useful for measuring broad semantic overlap, but it does not fully capture whether the AI preserved the exact human preference, motivation, or response style. Similarity ranges from –1 (opposite meaning) to +1 (identical meaning).

---

### 2. LLM-as-Judge Evaluation

This layer uses Gemini to evaluate how well the AI answer simulates the specific human respondent. the LLM scores each dimension on an integer scale from 1 to 5, where 1 = very poor match, 2 = weak match, 3 = partial match, 4 = good match and 5 = very strong match.

The judge scores each answer pair across the following dimensions:

| Metric | Meaning |
|---|---|
| `behavior_match_score` | Whether the AI preserves what the human actually does or would do |
| `preference_match_score` | Whether the AI preserves the human's stated preferences or choices |
| `reasoning_match_score` | Whether the AI preserves the human's stated reasons or motivations |
| `detail_preservation_score` | Whether the AI preserves concrete details such as brands, stores, products, or examples |
| `unsupported_additions_control_score` | Whether the AI avoids adding unsupported information |
| `response_style_match_score` | Whether the AI preserves tone, length, confidence, vagueness, or casualness |
| `overall_simulation_match_score` | Overall match between the AI answer and the human answer |

The judge also returns:

```text
final_verdict
main_failure_type
short_summary
```

---

### 3. Content-Level Comparison

This layer breaks each human and AI answer into small meaningful content elements. It checks what was preserved, omitted, changed, contradicted, or added without support. Note: Content‑level metrics – produced by the content‑comparison layer. The metrics are real numbers between 0 and 1.

Content element types include:

| Content element type | Meaning |
|---|---|
| `stated_action_or_behavior` | What the person does, did, buys, uses, chooses, avoids, or would do |
| `stated_preference_or_choice` | What the person likes, prefers, trusts, chooses, or prioritizes |
| `stated_reason_or_motivation` | Why the person does something or why they gave that answer |
| `specific_detail_or_example` | Specific stores, brands, products, people, platforms, examples, or constraints |
| `response_style_or_uncertainty` | Casual tone, uncertainty, vagueness, confidence, shortness, or hesitation |
| `stated_feeling_or_attitude` | Positive, negative, neutral, emotional, skeptical, or indifferent attitude |

Match labels include:

| Match label | Meaning |
|---|---|
| `fully_preserved` | The AI keeps the human content element clearly and accurately |
| `partly_preserved` | The AI keeps part of the human content element but loses detail, strength, or context |
| `missing_from_ai_answer` | A human content element is not represented in the AI answer |
| `not_supported_by_human_answer` | The AI adds a content element that the human did not say |
| `changed_or_contradicted` | The AI changes the meaning or contradicts the human |

The main content-level metrics are:

| Metric | Meaning |
|---|---|
| `content_recall` | How much of the human answer was preserved by the AI |
| `content_precision` | How much of the AI answer is supported by the human answer |
| `content_f1` | Balanced score between content recall and content precision |
| `unsupported_addition_rate` | How much unsupported extra content the AI added |
| `omission_rate` | How much human content the AI missed |

---

## Final Outputs

The pipeline creates the following files under `outputs/`:

## Output Files

| Output file | What it contains | Why it matters |
|---|---|---|
| `semantic_similarity_results.xlsx` | The original input data plus one embedding-based similarity score for each human-answer/AI-answer pair. | This is the baseline layer. It shows whether the two answers are broadly close in meaning, but it does not prove that the AI preserved the specific human respondent. |
| `llm_judge_results.xlsx` | The first LLM-as-judge evaluation output, including scores for behavior match, preference match, reasoning match, detail preservation, unsupported additions control, response style match, and overall simulation match. | This is the first structured evaluator output. It shows how well the AI answer simulates the human answer across human-relevant dimensions, but some rows may fail because of API rate limits. |
| `llm_judge_results_repaired.xlsx` | The completed LLM-as-judge file after failed or rate-limited rows have been rerun. | This is the judge file used for final analysis. It should contain complete judge scores for all rows. |
| `content_comparison_results.xlsx` | The full row-level output after content-level comparison is added. It includes recall, precision, F1, unsupported addition rate, omission rate, and a short content-level explanation for each answer pair. | This is the most interpretable evaluation layer. It shows what the AI preserved, missed, changed, or invented. |
| `final_combined_results.xlsx` | The main final result file containing the original data, semantic similarity scores, Gemini-as-judge scores, and content-level comparison metrics in one place. | This is the primary result file for submission and review. It allows the reviewer to inspect the full evaluation for every row. |
| `analysis_summary.xlsx` | An Excel workbook with the main summary tables saved as separate sheets. | This gives a compact overview of the results without requiring the reviewer to inspect every individual row. |
| `metric_summary.csv` | Overall average, median, minimum, maximum, valid-row count, and missing-row count for each metric. | This shows the overall performance pattern of the AI answers across all evaluation dimensions. |
| `category_summary.csv` | Average scores grouped by question category. | This shows whether the AI performs better or worse for certain types of market-research questions. |
| `person_summary.csv` | Average scores grouped by respondent/person ID. | This helps identify whether some simulated respondents are represented more accurately than others. |
| `failure_type_summary.csv` | Counts of the main failure types assigned by the Gemini-as-judge evaluation. | This shows the most common failure patterns, such as unsupported additions, missing human detail, changed reasoning, or changed preference. |
| `verdict_summary.csv` | Counts of strong, partial, and weak simulation matches. | This gives a high-level view of how many AI answers are acceptable simulations versus weak matches. |
| `correlation_summary.csv` | Correlations between semantic similarity, judge scores, and content-level metrics. | This shows whether broad semantic similarity agrees with stricter simulation-quality measures. A weak correlation would suggest that semantic similarity alone is not enough. |
| `high_semantic_low_alignment.csv` | Cases where semantic similarity is relatively high but judge/content-level alignment is weak. | These are important failure cases. They show answers that look similar at a topic level but fail to preserve the specific human answer. |
| `best_examples.csv` | The strongest answer pairs based on content-level F1 and related alignment scores. | These examples show where the AI successfully preserved the human answer. They can be used as positive examples in the report or presentation. |
| `worst_examples.csv` | The weakest answer pairs based on content-level F1 and related alignment scores. | These examples show the clearest failures, such as major omissions, unsupported additions, or changed meaning. They are useful for explaining why stricter evaluation is needed. |

---

## Main Evaluation Idea

Semantic similarity is useful, but it can overestimate quality when the AI answer stays on the same topic while changing the human's actual meaning. The LLM-as-judge layer captures broader simulation quality, while content-level comparison explains the exact source of mismatch.

Together, the three layers show whether the AI answer is:

- topically similar,
- behaviourally and motivationally aligned,
- grounded in the human answer,
- and specific enough for reliable market-research simulation.

---

## Notes

- The input file is expected at `data/RB_GenAI_Datatest.xlsx`.
- All generated files are saved under `outputs/`.
- The notebook is portable and is not tied to Google Colab, jupyter notebook, etc.
- The Gemini API key should not be committed to the repository. 
