# Evaluation of Human Simulation Agents for Consumer Interview Responses

## 1. Objective and Evaluation Context

The objective of this evaluation is to assess how accurately AI-based human simulations reproduce the responses of real consumers in an open-ended market-research interview setting. The dataset contains 30 paired responses: 3 real human participants answered 10 questions each, and the corresponding human simulation agents answered the same questions. The questions cover consumer-relevant contexts such as shopping behaviour, product preferences, brand loyalty and purchase influences.

The key evaluation question is not whether the agent gives a fluent or plausible answer. The key question is whether the agent answer preserves the specific human respondent’s behaviour, preferences, motivations, details and response style. This distinction is important because an answer can sound realistic while still misrepresenting the actual person.

## 2. Evaluation Framework

A multi-layer evaluation framework was used because no single metric is sufficient for open-ended human simulation assessment.


| Evaluation criterion | What is evaluated | Measurement method | Why it matters |
| :-- | :-- | :-- | :-- |
| Semantic similarity | Whether the human and agent answers discuss the same broad topic | Sentence-transformer embeddings and cosine similarity | Gives a fast baseline for topic overlap |
| Behaviour match | Whether the agent preserves what the human actually does | LLM-as-judge, 1 to 5 scale | Captures actions such as buying online, using stores or switching products |
| Preference match | Whether the agent preserves likes, choices, brands, channels or product preferences | LLM-as- judge, 1 to 5 scale | Important for market-research validity |
| Reasoning match | Whether the agent preserves the human’s stated motivation | LLM-as-judge, 1 to 5 scale | Prevents false conclusions about why consumers behave a certain way |
| Detail preservation | Whether concrete details are retained | LLM-as-judge, 1 to 5 scale | Checks names, stores, brands, platforms and product examples |
| Unsupported additions control | Whether the agent avoids invented claims | LLM-as-judge, 1 to 5 scale | Detects hallucinated motivations, brands or values |
| Response style match | Whether the agent preserves the human’s tone and level of detail | LLM-as-judge, 1 to 5 scale | Human responses are often short, casual or uncertain, unlike polished agent answers |
| Content-level comparison | Which specific content elements are preserved, missed or invented | Claim/content recall, precision, F1, unsupported-addition rate and omission rate | Gives an auditable view of exact preservation and failure patterns |

The evaluation therefore measures three levels of alignment: broad semantic overlap, rubric-based simulation quality and fine-grained content preservation.

## 3. Main Results

The semantic similarity score is moderately high, with a mean of approximately 0.668. This indicates that the agents usually stay within the same broad topic as the human response. However, the LLM-judge and content-level results show that topic overlap does not equal accurate human simulation.

The overall simulation-match score is low, with a mean of approximately 1.39 out of 5. The weakest dimensions are reasoning match, detail preservation and unsupported additions control. This means the agents often respond in the right domain but fail to preserve the individual respondent’s actual motivation, specific details and style.


| Metric | Mean result | Interpretation |
| :-- | --: | :-- |
| Semantic similarity | 0.668 | The agent usually stays on the same broad topic, such as skincare, shopping channels or product choice |
| Behaviour match | 1.83 / 5 | Some broad actions are captured, but the agent often changes the context, for example turning “I buy online” into “I use supermarkets and online platforms” |
| Preference match | 1.56 / 5 | Specific preferences are often replaced with generic consumer preferences, such as “good value” or “safe ingredients” |
| Reasoning match | 1.22 / 5 | Human motivations such as discounts, flexibility or smell are often changed into invented reasons like convenience or ingredient transparency |
| Detail preservation | 1.44 / 5 | Concrete details such as YesStyle, Korean skincare, DM or body shampoo are often missed or diluted |
| Unsupported additions control | 1.00 / 5 | The agent frequently adds unsupported claims, including non-harmful ingredients, free samples, reliability or time-saving |
| Response style match | 1.94 / 5 | Human answers are often short and casual, while agent answers are longer, polished and more rationalised |
| Overall simulation match | 1.39 / 5 | The agents are weak at reproducing the specific human respondent |
| Content recall | ~0.50 | Around half of human content is preserved |
| Content precision | ~0.33 | Much agent content is unsupported by the human answer |
| Content F1 | ~0.40 | The balance between preserving human content and avoiding invented content is low |

## 4. Key Findings

The agents are better at reproducing general consumer themes than individual consumer behaviour. For example, when a human says they buy personal-care products online because it offers flexibility and discounts, the agent may still mention online shopping. However, it may also add supermarkets, convenience, value for money or non-harmful ingredients. The topic is similar, but the person-specific motivation has changed.

The largest failure pattern is unsupported addition. Agents often fill gaps with plausible consumer logic that was not stated by the human. This creates a serious risk for market research because invented motivations can be mistaken for real consumer insight. Examples include adding ingredient transparency, free samples, non-greasy texture, natural ingredients or convenience when the human did not mention these factors.

A second major issue is motivation drift. Human answers are often simple, vague or practical. Agents tend to rationalise them into more elaborate explanations. For instance, if a human simply selects a product option without giving a reason, the agent may invent a detailed explanation about hydration, quality or texture. This makes the response sound better but less faithful.

A third issue is style mismatch. Real respondents often answer briefly, casually and with uncertainty. The agents produce longer, structured and confident responses. This polished style makes the simulations less authentic and may bias downstream interpretation.

## 5. Strengths and Weaknesses of the Evaluation Approach

The main strength of the approach is that it does not rely on one metric. Semantic similarity provides a quick baseline, the LLM judge captures behavioural and qualitative alignment, and content-level comparison shows exactly what was preserved, omitted or invented. This makes the evaluation both quantitative and interpretable.

However, the approach also has limitations. The LLM judge may still introduce subjectivity, even with a strict rubric. The dataset is small, with only 30 response pairs, so the results should be interpreted as directional rather than statistically final. Another limitation is that the evaluation only compares the second-interview human answer with the agent answer. If the agent used information from the first interview, some details may appear unsupported from the evaluator’s perspective even if they were grounded in the original persona-building interview.

## 6. Recommendations

The most important improvement is to reduce unsupported additions. The agent should be instructed to answer only from known persona evidence and to avoid adding motivations or details that are not clearly grounded. A retrieval-based persona memory could help by forcing the agent to use evidence from the first interview before answering.

Second, the agent should be calibrated for response style. If the human usually gives short, casual or uncertain answers, the simulation should do the same. The prompt should discourage over-explaining, over-rationalising and adding polished marketing-style language.

Third, the evaluation should be expanded. More respondents, more questions and repeated evaluations would make the findings more robust. A small human-evaluator calibration set should also be added to check whether the LLM as a judge is scoring consistently with human judgement.

Finally, the content-level comparison should become a standard evaluation layer. It is the most useful diagnostic component because it shows exactly which human details were preserved, missed or invented. This makes the results actionable for improving future agent prompts, grounding mechanisms and persona construction.

## 7. Conclusion

The evaluation shows that the human simulation agents remain broadly on topic but do not yet reliably reproduce individual human responses. Their main weakness is not fluency, but fidelity to the specific person. The agents often omit concrete human details, change motivations and add plausible but unsupported claims. For consumer-insights use cases, this is a critical limitation because the added details may look like real customer insight even when they are not grounded in the respondent. A multi-layer evaluation framework combining semantic similarity, LLM as a judge and content-level comparison provides a clearer and more actionable assessment of human simulation quality.

