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

This score is useful for measuring broad semantic overlap, but it does not fully capture whether the AI preserved the exact human preference, motivation, or response style.

---

### 2. LLM-as-Judge Evaluation

This layer uses Gemini to evaluate how well the AI answer simulates the specific human respondent.

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

This layer breaks each human and AI answer into small meaningful content elements. It checks what was preserved, omitted, changed, contradicted, or added without support.

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

| Output | Explanation |
|---|---|
| `semantic_similarity_results.xlsx` | Input data with semantic similarity scores added |
| `llm_judge_results.xlsx` | Input data with Gemini-as-judge evaluation scores added |
| `content_comparison_results.xlsx` | Input data with content-level comparison metrics added |
| `final_combined_results.xlsx` | Main final file containing all evaluation layers |
| `analysis_summary.xlsx` | Excel workbook containing all summary tables in separate sheets |
| `metric_summary.csv` | Overall summary of each evaluation metric |
| `category_summary.csv` | Aggregated results grouped by question category |
| `person_summary.csv` | Aggregated results grouped by respondent/person ID |
| `failure_type_summary.csv` | Counts of the main failure types identified by the judge |
| `verdict_summary.csv` | Counts of strong, partial, and weak simulation matches |
| `correlation_summary.csv` | Correlation between semantic similarity, judge scores, and content-level metrics |
| `high_semantic_low_alignment.csv` | Cases where semantic similarity is high but actual alignment is weak |
| `best_examples.csv` | Strongest examples based on content-level F1 |
| `worst_examples.csv` | Weakest examples based on content-level F1 |

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
- The notebook is portable and is not tied to Google Colab.
- The Gemini API key should not be committed to the repository.
