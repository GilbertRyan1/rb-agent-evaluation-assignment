JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "behavior_match": {
            "type": "object",
            "properties": {
                "score": {"type": "integer", "minimum": 1, "maximum": 5},
                "reason": {"type": "string"},
            },
            "required": ["score", "reason"],
        },
        "preference_match": {
            "type": "object",
            "properties": {
                "score": {"type": "integer", "minimum": 1, "maximum": 5},
                "reason": {"type": "string"},
            },
            "required": ["score", "reason"],
        },
        "reasoning_match": {
            "type": "object",
            "properties": {
                "score": {"type": "integer", "minimum": 1, "maximum": 5},
                "reason": {"type": "string"},
            },
            "required": ["score", "reason"],
        },
        "detail_preservation": {
            "type": "object",
            "properties": {
                "score": {"type": "integer", "minimum": 1, "maximum": 5},
                "reason": {"type": "string"},
            },
            "required": ["score", "reason"],
        },
        "unsupported_additions_control": {
            "type": "object",
            "properties": {
                "score": {"type": "integer", "minimum": 1, "maximum": 5},
                "reason": {"type": "string"},
            },
            "required": ["score", "reason"],
        },
        "response_style_match": {
            "type": "object",
            "properties": {
                "score": {"type": "integer", "minimum": 1, "maximum": 5},
                "reason": {"type": "string"},
            },
            "required": ["score", "reason"],
        },
        "overall_simulation_match_score": {
            "type": "integer",
            "minimum": 1,
            "maximum": 5,
        },
        "final_verdict": {
            "type": "string",
            "enum": [
                "strong simulation match",
                "partial simulation match",
                "weak simulation match",
            ],
        },
        "main_failure_type": {
            "type": "string",
            "enum": [
                "good match",
                "missing human detail",
                "unsupported additions",
                "changed reasoning",
                "changed preference",
                "changed behavior",
                "changed style",
                "major mismatch",
            ],
        },
        "short_summary": {"type": "string"},
    },
    "required": [
        "behavior_match",
        "preference_match",
        "reasoning_match",
        "detail_preservation",
        "unsupported_additions_control",
        "response_style_match",
        "overall_simulation_match_score",
        "final_verdict",
        "main_failure_type",
        "short_summary",
    ],
}


CONTENT_ELEMENT_TYPES = [
    "stated_action_or_behavior",
    "stated_preference_or_choice",
    "stated_reason_or_motivation",
    "specific_detail_or_example",
    "response_style_or_uncertainty",
    "stated_feeling_or_attitude",
]


CONTENT_MATCH_LABELS = [
    "fully_preserved",
    "partly_preserved",
    "missing_from_ai_answer",
    "not_supported_by_human_answer",
    "changed_or_contradicted",
]


CONTENT_SCHEMA = {
    "type": "object",
    "properties": {
        "human_content_elements": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "element_id": {"type": "string"},
                    "content": {"type": "string"},
                    "content_type": {
                        "type": "string",
                        "enum": CONTENT_ELEMENT_TYPES,
                    },
                },
                "required": ["element_id", "content", "content_type"],
            },
        },
        "ai_content_elements": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "element_id": {"type": "string"},
                    "content": {"type": "string"},
                    "content_type": {
                        "type": "string",
                        "enum": CONTENT_ELEMENT_TYPES,
                    },
                },
                "required": ["element_id", "content", "content_type"],
            },
        },
        "content_matches": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "human_element_id": {"type": "string"},
                    "ai_element_id": {"type": "string"},
                    "match_label": {
                        "type": "string",
                        "enum": CONTENT_MATCH_LABELS,
                    },
                    "reason": {"type": "string"},
                },
                "required": [
                    "human_element_id",
                    "ai_element_id",
                    "match_label",
                    "reason",
                ],
            },
        },
        "missing_human_content": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "human_element_id": {"type": "string"},
                    "reason": {"type": "string"},
                },
                "required": ["human_element_id", "reason"],
            },
        },
        "unsupported_ai_content": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "ai_element_id": {"type": "string"},
                    "reason": {"type": "string"},
                },
                "required": ["ai_element_id", "reason"],
            },
        },
        "content_recall": {"type": "number"},
        "content_precision": {"type": "number"},
        "content_f1": {"type": "number"},
        "unsupported_addition_rate": {"type": "number"},
        "omission_rate": {"type": "number"},
        "content_comparison_summary": {"type": "string"},
    },
    "required": [
        "human_content_elements",
        "ai_content_elements",
        "content_matches",
        "missing_human_content",
        "unsupported_ai_content",
        "content_recall",
        "content_precision",
        "content_f1",
        "unsupported_addition_rate",
        "omission_rate",
        "content_comparison_summary",
    ],
}
