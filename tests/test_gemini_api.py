import google.generativeai as genai

genai.configure(api_key="API_KEY")

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
response = model.generate_content("Explique como funciona a inteligência artificial")

print(response.text)
