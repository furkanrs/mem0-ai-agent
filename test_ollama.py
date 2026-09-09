import ollama

response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": "Explain what Mem0 is in two simple sentences.",
        }
    ],
)

print(response["message"]["content"])