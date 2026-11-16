from dotenv import load_dotenv
import os


load_dotenv()  # Load environment variables from .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Get the value of GEMINI_API_KEY from environment variables

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing. Please configure it in your .env file.")