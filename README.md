# RB Agent Evaluation Assignment

This repository is structured for an agent response evaluation assignment.

The goal is to evaluate how well an AI agent's generated answers align with real human answers in the provided dataset.

## Repository Structure

```text
rb-agent-evaluation-assignment/
├── assignment_materials/        # Original assignment PDF
├── data/                        # Input Excel dataset
├── src/agent_eval/              # Reusable evaluation modules
├── notebooks/                   # Notebook-driven execution workflow
├── outputs/                     # Generated evaluation results
├── reports/                     # Written report and figures
├── presentation/                # PPT deck and slide assets
└── submission/                  # Final files to submit
```

## Planned Evaluation Layers

1. Semantic similarity evaluation
2. Gemini-as-judge agent response evaluation
3. Optional claim-based comparison

## How to Run

This project will be notebook-driven. The main execution notebook is:

```text
notebooks/01_agent_evaluation_pipeline.ipynb
```

The notebook will import reusable functions from `src/agent_eval/` and save results under `outputs/`.

## API Key

Create a local `.env` file based on `.env.example`:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

Do not commit `.env` to GitHub.
