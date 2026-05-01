def build_judge_prompt(row) -> str:
    return f"""
You are an expert evaluator for an AI-human simulation task.

You will receive:
1. A market-research question
2. A real human answer
3. An AI-generated answer that attempts to simulate the human answer

Your task is to evaluate how well the AI-generated answer matches the specific human respondent's answer.

Important evaluation rules:
- Do not reward the AI answer just because it is fluent, polished, detailed, or plausible.
- Do not judge whether the AI answer is a good general answer to the question.
- Judge whether the AI answer preserves the specific human answer.
- Penalize unsupported additions, invented reasons, changed preferences, changed behavior, missing details, and changed tone.
- If the human answer is short, uncertain, casual, or vague, the AI should not be rewarded for making it long, confident, or overly rational.
- A response can be semantically related but still have a weak simulation match if it changes the human's actual meaning.
- Be strict but fair.

Evaluate the AI answer across six dimensions using integer scores from 1 to 5.

Scoring scale:
1 = Very poor match
2 = Weak match
3 = Partial match
4 = Good match
5 = Very strong match

Dimensions:

1. Behavior Match
Does the AI preserve what the human actually does, did, or would do?

2. Preference Match
Does the AI preserve what the human likes, chooses, prefers, trusts, avoids, or values?

3. Reasoning Match
Does the AI preserve the human's stated reasons and motivations?

4. Detail Preservation
Does the AI preserve concrete details from the human answer?

5. Unsupported Additions Control
Does the AI avoid adding claims that are not supported by the human answer?

6. Response Style Match
Does the AI preserve the human's response style?

After scoring each dimension, provide:
- overall_simulation_match_score from 1 to 5
- final_verdict
- main_failure_type
- short_summary

The overall_simulation_match_score should reflect the full match between the AI answer and the human answer.
Do not calculate it as a simple average if there is a serious issue such as changed preference, changed behavior, or many unsupported additions.

Final verdict options:
- strong simulation match
- partial simulation match
- weak simulation match

Main failure type options:
- good match
- missing human detail
- unsupported additions
- changed reasoning
- changed preference
- changed behavior
- changed style
- major mismatch

Return only valid JSON.
Do not include markdown.
Do not include extra explanation outside the JSON.

Input:

Question category:
{row["question_category"]}

Question:
{row["question"]}

Human answer:
{row["human_answers"]}

AI-generated answer:
{row["ai_answers"]}
""".strip()


def build_content_prompt(row) -> str:
    return f"""
You are evaluating how well an AI-generated answer preserves a specific human answer.

Break the human answer and the AI-generated answer into small content elements.
Each content element should capture one meaningful part of the answer.

Content element types:
- stated_action_or_behavior: what the person does, did, buys, uses, chooses, avoids, or would do
- stated_preference_or_choice: what the person likes, prefers, trusts, chooses, or prioritizes
- stated_reason_or_motivation: why the person does something or why they gave that answer
- specific_detail_or_example: specific stores, brands, products, people, platforms, examples, or constraints
- response_style_or_uncertainty: casual tone, uncertainty, vagueness, confidence, shortness, or hesitation
- stated_feeling_or_attitude: positive, negative, neutral, emotional, skeptical, or indifferent attitude

Match labels:
- fully_preserved: the AI keeps the human content element clearly and accurately
- partly_preserved: the AI keeps part of the human content element but loses detail, strength, or context
- missing_from_ai_answer: a human content element is not represented in the AI answer
- not_supported_by_human_answer: the AI adds a content element that the human did not say
- changed_or_contradicted: the AI changes the meaning or contradicts the human

Metrics:
- content_recall: how much of the human answer was preserved by the AI
- content_precision: how much of the AI answer is supported by the human answer
- content_f1: balanced score between content_recall and content_precision
- unsupported_addition_rate: how much unsupported extra content the AI added
- omission_rate: how much human content the AI missed

Rules:
- Be strict.
- Do not count generic, plausible, or invented content as preserved.
- If the AI changes a reason, preference, behavior, or specific detail, mark it as changed or unsupported.
- Keep content elements short and specific.
- Return only valid JSON.

Input:

Question category:
{row["question_category"]}

Question:
{row["question"]}

Human answer:
{row["human_answers"]}

AI-generated answer:
{row["ai_answers"]}
""".strip()
