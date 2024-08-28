import openai

openai.api_key = 'your-api-key'

def predict_disaster(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Identify if there is a disaster or emergency in this news text: {text}",
        max_tokens=50
    )
    return response.choices[0].text.strip()