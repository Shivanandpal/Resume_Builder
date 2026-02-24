from google import genai
client = genai.Client(api_key="AIzaSyBrhb_1Et5G-Yd7z1UBv54q9lyWvcr8bLg")
for model in client.models.list():
    print(model.name)
