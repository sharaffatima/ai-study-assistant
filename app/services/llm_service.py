from urllib import response

from google import genai
from app.core.config import GEMINI_API_KEY
from google.genai import types
from app.schemas.study import QuizResponse

class LLMServiceError(Exception):
    pass


client = genai.Client(api_key=GEMINI_API_KEY)


def generate_response(prompt:str)->str:
    try:
        response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents=prompt
        )

    except Exception as error:
        print(f"Gemini API Error: {error}")
        raise LLMServiceError(
            "Failed to generate a response from Gemini."
            ) from error # exception chaining: the original error remains attached as the cause

    if not response or not response.text or not response.text.strip():
        raise LLMServiceError(
            "Received an invalid response from Gemini."
            )
    return response.text


def generate_quiz(prompt: str) -> QuizResponse:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=QuizResponse
            )
        )

    except Exception as error:
        print(f"Gemini API Error: {error}")
        raise LLMServiceError(
            "Failed to generate a quiz from Gemini."
        ) from error

    quiz = QuizResponse.model_validate(response.parsed)

    if quiz is None:
        raise LLMServiceError(
            "Received an invalid response from Gemini."
        )

    return quiz