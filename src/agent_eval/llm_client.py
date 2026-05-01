import json
import os
import time
from typing import Any, Dict, Optional

from google import genai
from google.genai import types


def get_api_key() -> str:
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY")

    return api_key


def is_rate_limit_error(error: Exception) -> bool:
    message = str(error)
    return "429" in message or "RESOURCE_EXHAUSTED" in message


def call_llm(
    prompt: str,
    model_name: str = "gemini-2.5-flash",
    response_schema: Optional[Dict[str, Any]] = None,
    temperature: float = 0,
    max_retries: int = 5,
    retry_wait_seconds: int = 30,
) -> str:
    client = genai.Client(api_key=get_api_key())

    config_args = {
        "temperature": temperature,
        "response_mime_type": "application/json",
    }

    if response_schema is not None:
        config_args["response_json_schema"] = response_schema

    last_error = None

    for attempt in range(max_retries + 1):
        try:
            try:
                config = types.GenerateContentConfig(**config_args)

            except TypeError:
                config_args.pop("response_json_schema", None)

                if response_schema is not None:
                    config_args["response_schema"] = response_schema

                config = types.GenerateContentConfig(**config_args)

            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config,
            )

            return response.text

        except Exception as error:
            last_error = error

            if attempt >= max_retries:
                break

            if is_rate_limit_error(error):
                wait_time = retry_wait_seconds * (attempt + 1)
            else:
                wait_time = 3 * (attempt + 1)

            print(f"LLM call failed. Retry {attempt + 1}/{max_retries} after {wait_time}s")
            time.sleep(wait_time)

    raise RuntimeError(f"LLM call failed: {last_error}")


def parse_json_response(response_text: str) -> Dict[str, Any]:
    try:
        return json.loads(response_text)

    except json.JSONDecodeError:
        start = response_text.find("{")
        end = response_text.rfind("}") + 1

        if start == -1 or end == 0:
            raise ValueError("No JSON object found in response")

        return json.loads(response_text[start:end])
