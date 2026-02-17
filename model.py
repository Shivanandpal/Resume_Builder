from google import genai
client = genai.Client(api_key="AIzaSyCj8xyFZY1MEMIHAIAJjZ3_DhaD3pOS26o")
for model in client.models.list():
    print(model.name)
