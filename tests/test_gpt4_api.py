from openai import OpenAI

client = OpenAI(api_key="OPENAI_API_KEY")

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Você é um assistente útil."},
        {"role": "user", "content": "Escreva uma frase curta sobre segurança em IA."}
    ], 
    max_tokens=20
)

print(completion.choices[0].message.content)