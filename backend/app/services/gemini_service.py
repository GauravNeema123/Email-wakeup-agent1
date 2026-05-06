import requests
from dotenv import load_dotenv
import os

load_dotenv()

OPEN_ROUTER_API_KEY = os.getenv(
    "OPEN_ROUTER_API_KEY"
)


class Model:

    def generate_content(self, prompt):

        response = requests.post(

            url="https://openrouter.ai/api/v1/chat/completions",

            headers={

                "Authorization":
                f"Bearer {OPEN_ROUTER_API_KEY}",

                "Content-Type":
                "application/json",

                "HTTP-Referer":
                "http://localhost:3000",

                "X-Title":
                "Email Wakeup Agent"
            },

            json={

                "model":
                "openai/gpt-3.5-turbo",

                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        )

        print(response.status_code)
        print(response.text)

        response.raise_for_status()

        data = response.json()

        return type(
            "Response",
            (),
            {
                "text":
                data["choices"][0]["message"]["content"]
            }
        )()


model = Model()