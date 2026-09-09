import ollama
from mem0 import Memory
from dotenv import load_dotenv

from config import config


load_dotenv("../.env")

# Create the Mem0 memory system using our configuration
memory = Memory.from_config(config)


def chat_with_memories(message: str, user_id: str = "default_user") -> str:

    # -----------------------------------
    # 1. Retrieve relevant old memories
    # -----------------------------------
    relevant_memories = memory.search(
        query=message,
        filters={"user_id": user_id},
        limit=3
    )

    memories_str = "\n".join(
        f"- {entry['memory']}"
        for entry in relevant_memories["results"]
    )

    print("\nRelevant memories:")
    print(memories_str)

    # -----------------------------------
    # 2. Create prompt for the AI
    # -----------------------------------
    system_prompt = f"""
You are a helpful AI.

Answer the user's question using the relevant memories when they are useful.

User Memories:
{memories_str}
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": message
        },
    ]

    # -----------------------------------
    # 3. Generate response using local LLM
    # -----------------------------------
    response = ollama.chat(
        model="qwen2.5:3b",
        messages=messages,
    )

    assistant_response = response["message"]["content"]

    # -----------------------------------
    # 4. Create conversation text for Mem0
    # -----------------------------------
    conversation = f"""
User: {message}

Assistant: {assistant_response}
"""

    # -----------------------------------
    # 5. Mem0 extracts and stores memories
    # -----------------------------------
    memory_result = memory.add(
        conversation,
        user_id=user_id,
        metadata={"source": "demo"}
    )

    print("\nMemory add result:")
    print(memory_result)

    return assistant_response


def main():

    print("Chat with AI (type 'exit' to quit)")

    while True:

        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        ai_response = chat_with_memories(user_input)

        print(f"\nAI: {ai_response}")


if __name__ == "__main__":
    main()