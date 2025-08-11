import requests
from src.chatbot.prompt import SYSTEM_PROMPT, USER_PROMPT


class LLM:
    def __init__(self, endpoint, model_name, stream=False):
        self.endpoint = endpoint
        self.model = model_name 
        self.stream = stream
        self.temperature = 0.7
        self.headers = {
            "Content-Type": "application/json"
        }

    def create_system_prompt(self):
        return SYSTEM_PROMPT
    
    
    def create_user_prompt(self):
        return USER_PROMPT
    

    def send_messages(self, inputs: list):
        print(inputs)
        data = {
            "model": self.model,
            "stream": self.stream,
            "temperature": self.temperature,
            "messages": [
                {"role": "system", "content": self.create_system_prompt()},
                {"role": "user", "content": self.create_user_prompt()},
                *[user_input for user_input in inputs]
            ],
        }

        response = requests.post(self.endpoint, json=data, headers=self.headers)
        return response.json()["message"]["content"]
