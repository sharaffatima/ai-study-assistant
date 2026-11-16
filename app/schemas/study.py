from pydantic import BaseModel, Field, field_validator
from enum import Enum


class SummaryRequest(BaseModel): # Basemodel gives our class Pydantic's validation and data-handling capabilities
    text: str = Field(min_length= 1, max_length= 10000)
    max_length: int = Field(ge= 20, le = 500)

    @field_validator("text")
    @classmethod
    def not_empty(cls, text):
        if not text.strip():
            raise ValueError("Text cannot be empty or whitespace.")
        return text


class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class ExplainRequest(BaseModel):
    text:str = Field(min_length=1, max_length=10000)
    difficulty:DifficultyLevel

    @field_validator("text")
    @classmethod
    def not_empty(cls, text):
        if not text.strip():
            raise ValueError("Text cannot be empty or whitespace.")
        return text



class QuizRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10000)
    num_questions: int = Field(ge=1, le=10)
    difficulty: DifficultyLevel

    @field_validator("text")
    @classmethod
    def not_empty(cls, text):
        if not text.strip():
            raise ValueError("Text cannot be empty or whitespace.")
        return text

class QuizQuestion(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: int = Field(ge=0, le=3)
    explanation: str = Field(min_length=1, max_length=1000)

    @field_validator("question", "explanation")
    @classmethod
    def not_empty(cls, value:str):
        if not value.strip():
            raise ValueError("Field cannot be empty or whitespace.")
        return value

    @field_validator("options")
    @classmethod
    def validate_options(cls, options:list[str]) -> list[str]:
        if len(options) != len(set(options)):
            raise ValueError("Options must be unique.")
        if any(not option.strip() for option in options):  # since when does Python look like Haskell
            raise ValueError("Options cannot be empty or whitespace.")
        return options


class QuizResponse(BaseModel):
    questions: list[QuizQuestion] = Field(min_length=1, max_length=10)