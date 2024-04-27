import json
import requests


# Subject to the traffic to OpenAI and might return an error if their API is busy.
class OpenaiApiGPT3Turbo:
    def get_summary(self, prompt) -> str:
        with open('env.json', 'r') as f:
            data = json.load(f)

        url = 'https://api.openai.com/v1/chat/completions'

        key = data['OPENAI_API_KEY']
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {key}'}

        payload = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {
                    'role': 'user',
                    'content': f'Briefly summarize the following: {prompt}',
                }
            ],
            'temperature': 0.7,  # Value between 0 and 2, lower values mean more random responses.
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            response_data = json.loads(response.content)

            # According to the docs the api can return multiple choices, this is a way to handle that before the return.
            choices = []
            for choice in response_data['choices']:
                choices.append(choice['message']['content'])

            string_from_list = '\n\n'.join(choices)

            print(string_from_list)

            return string_from_list
        else:
            return f'Error: {response.status_code}, {response.reason}'
