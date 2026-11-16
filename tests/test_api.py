from urllib import response

from fastapi.testclient import TestClient
from app.main import app
from app.schemas.study import QuizResponse

from app.services.llm_service import LLMServiceError

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to AI Study Assistant!"}

# helper function
def mock_generate_reponse(prompt):
      raise LLMServiceError("Simulated Gemini failure")


# Summary Endpoint tests #

def test_summarize(monkeypatch):
    monkeypatch.setattr("app.routes.study.generate_response", lambda prompt: "This is a summary.")
    response = client.post("/api/v1/summarize", 
        json={
            "text": "An API allows software systems to communicate.",
            "max_length": 100
        }
    )
    assert response.status_code == 200
    assert "summary" in response.json()
    assert response.json() == {"summary": "This is a summary."}

def test_summarize_rejects_whitespace():
        response = client.post("/api/v1/summarize", 
            json={
                "text": "   ",
                "max_length": 100
            }
        )
        assert response.status_code == 422


def test_summarize_handles_llm_error(monkeypatch):
    monkeypatch.setattr("app.routes.study.generate_response", mock_generate_reponse) 
    response = client.post("/api/v1/summarize", 
        json={
            "text": "An API allows software systems to communicate.",
            "max_length": 100
        }
    )
    assert response.status_code == 503



# Explanation Endpoint tests #

def test_explain(monkeypatch):
    monkeypatch.setattr("app.routes.study.generate_response", lambda prompt: "This is an explanation.")
    response = client.post(
        "/api/v1/explain", 
        json={
            "text": "An API stands for Application Programming Interface. It is a set of rules and protocols that lets different software programs talk to and share data with each other",
            "difficulty": "beginner"
            }
            )
    assert response.status_code == 200
    assert "explanation" in response.json()
    assert response.json() == {"explanation":"This is an explanation."}

def test_explain_rejects_whitespace():
        response = client.post("/api/v1/explain", 
            json={
                "text": "   ",
                "difficulty": "beginner"
            }
        )
        assert response.status_code == 422

def test_explain_handles_llm_error(monkeypatch):
    monkeypatch.setattr("app.routes.study.generate_response", mock_generate_reponse) 
    response = client.post("/api/v1/explain", 
        json={
            "text": "An API stands for Application Programming Interface. It is a set of rules and protocols that lets different software programs talk to and share data with each other",
            "difficulty": "beginner"
        }
    )
    assert response.status_code == 503

# Quiz Endpoint tests #

def test_quiz(monkeypatch):
    monkeypatch.setattr("app.routes.study.generate_quiz", lambda prompt:
        QuizResponse(
            questions=[
            {
                "question": "What does API stand for?",
                "options": ["Application Programming Interface", "Advanced Programming Interface", "Application Protocol Interface", "Automated Programming Interface"],
                "correct_answer": 0,
                "explanation": "API stands for Application Programming Interface."
            },
            {
                "question": "What is the purpose of an API?",
                "options": ["To allow software systems to communicate", "To create user interfaces", "To manage databases", "To compile code"],
                "correct_answer": 0,
                "explanation": "APIs allow different software systems to communicate and share data."
            },
            {
                "question": "Which of the following is NOT a function of an API?",
                "options": ["Data sharing", "Communication between software", "User interface design", "Protocol definition"],
                "correct_answer": 2,
                "explanation": "APIs do not handle user interface design; they facilitate communication and data sharing."
            }
        ]
    ))

    response = client.post(
        "/api/v1/quiz", 
        json={
            "text": "An API stands for Application Programming Interface. It is a set of rules and protocols that lets different software programs talk to and share data with each other",
            "num_questions": 3,
            "difficulty": "beginner"
        }
    )
    assert response.status_code == 200
    assert "questions" in response.json()
    assert len(response.json()["questions"]) == 3
    for question in response.json()["questions"]:
        assert len(question["options"]) == 4
        assert type(question["correct_answer"]) is int
        assert 0 <= question["correct_answer"] <= 3
        assert question["question"].strip() != ""
        assert question["explanation"].strip() != ""
        for option in question["options"]:
            assert option.strip() != ""

def test_quiz_rejects_whitespace():
     response = client.post("/api/v1/quiz", 
             json={
                 "text": "   ",
                 "num_questions": 3,
                 "difficulty": "beginner"
             }
         )
     assert response.status_code == 422

def test_quiz_rejects_invalid_question_count():
    response = client.post("/api/v1/quiz", 
    json={
        "text": "An API stands for Application Programming Interface. It is a set of rules and protocols that lets different software programs talk to and share data with each other",
        "num_questions": 11,
         "difficulty": "beginner"
        }
    )
    assert response.status_code == 422

def test_quiz_rejects_invalid_difficulty():
    response = client.post("/api/v1/quiz", 
    json={
        "text": "An API stands for Application Programming Interface. It is a set of rules and protocols that lets different software programs talk to and share data with each other",
        "num_questions": 3,
         "difficulty": "expert"
         }
        )
    assert response.status_code == 422

def test_quiz_handles_llm_error(monkeypatch):
    monkeypatch.setattr("app.routes.study.generate_response", mock_generate_reponse) 
    response = client.post("/api/v1/quiz", 
    json={
        "text": "An API stands for Application Programming Interface. It is a set of rules and protocols that lets different software programs talk to and share data with each other",
        "num_questions": 3,
        "difficulty": "beginner"
        }
    )
    assert response.status_code == 503

def test_quiz_rejects_wrong_question_count(monkeypatch):
    monkeypatch.setattr("app.routes.study.generate_quiz", lambda prompt:
        QuizResponse(
            questions=[
            {
                "question": "What does API stand for?",
                "options": ["Application Programming Interface", "Advanced Programming Interface", "Application Protocol Interface", "Automated Programming Interface"],
                "correct_answer": 0,
                "explanation": "API stands for Application Programming Interface."
            },
            {
                "question": "What is the purpose of an API?",
                "options": ["To allow software systems to communicate", "To create user interfaces", "To manage databases", "To compile code"],
                "correct_answer": 0,
                "explanation": "APIs allow different software systems to communicate and share data."
            }
            ]
    ))

    response = client.post(
        "/api/v1/quiz", 
        json={
            "text": "An API stands for Application Programming Interface. It is a set of rules and protocols that lets different software programs talk to and share data with each other",
            "num_questions": 3,
            "difficulty": "beginner"
        }
    )
    assert response.status_code == 502