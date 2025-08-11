from src.chatbot.llm_model import LLM 
import dotenv 
import os 

dotenv.load_dotenv()

endpoint = os.getenv("LLM_ENDPOINT")
model = os.getenv("MODEL_NAME")

llm_model = LLM(endpoint=endpoint, 
                model_name=model,
                stream=False)