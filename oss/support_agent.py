import ollama
from mem0 import Memory
from dotenv import load_dotenv
from config import config

load_dotenv()


class CustomerSupportAIAgent:

    def __init__(self):
        self.memory = Memory.from_config(config)
        self.model = "qwen2.5:3b"

    def handle_query(self, query, user_id):

        print("\n" + "=" * 60)
        print("CUSTOMER QUERY")
        print("=" * 60)
        print(query)

        # 1. Search existing memories for this customer
        print("\nSearching existing memories...")

        relevant_memories = self.memory.search(
            query=query,
            filters={"user_id": user_id},
            limit=5,
        )

        memories = relevant_memories.get("results", [])

        print("\nRelevant Memories:")

        if memories:
            for memory in memories:
                print(f"- {memory['memory']}")
        else:
            print("No relevant memories found.")

        # 2. Prepare memories as context for Qwen
        if memories:
            memory_context = "\n".join(
                f"- {memory['memory']}"
                for memory in memories
            )
        else:
            memory_context = "No previous customer information available."

        # 3. Generate response using Qwen
        messages = [
            {
                "role": "system",
                "content": f"""
You are a helpful customer support AI agent.

You have access to memories from previous conversations
with this customer.

Use the memories when they are relevant.

Do not invent order information or delivery information.

You cannot access a real external order database.

Customer memories:
{memory_context}
"""
            },
            {
                "role": "user",
                "content": query
            }
        ]

        response = ollama.chat(
            model=self.model,
            messages=messages,
        )

        ai_response = response["message"]["content"]

        # 4. Store important customer information in Mem0
        print("\nAdding customer information to memory...")

        memory_messages = [
            {
                "role": "user",
                "content": f"""
Remember the following customer information for future support conversations:

The customer's message was:

{query}

Extract and remember any important customer information
from this message.
"""
            }
        ]

        memory_result = self.memory.add(
            memory_messages,
            user_id=user_id,
        )

        print("\nMemory Add Result:")
        print(memory_result)

        # 5. Display response
        print("\nAI Response:")
        print(ai_response)

        print("\n" + "=" * 60)

        return ai_response

    def get_memories(self, user_id):

        return self.memory.get_all(
            filters={"user_id": user_id}
        )


# ---------------------------------------------------------
# Start Customer Support Agent
# ---------------------------------------------------------

support_agent = CustomerSupportAIAgent()

print("\n" + "=" * 60)
print("CUSTOMER SUPPORT AI AGENT")
print("=" * 60)

# Ask for customer ID
customer_id = input("\nEnter your Customer ID: ").strip()

if not customer_id:
    print("Customer ID cannot be empty.")
    exit()

print(f"\nWelcome, Customer {customer_id}!")
print("Type 'exit' to end the conversation.")


# ---------------------------------------------------------
# Continuous conversation
# ---------------------------------------------------------

while True:

    query = input("\nYou: ").strip()

    if not query:
        continue

    if query.lower() == "exit":
        break

    support_agent.handle_query(
        query,
        user_id=customer_id,
    )


# ---------------------------------------------------------
# Display customer's memories
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("CUSTOMER MEMORIES")
print("=" * 60)

memories = support_agent.get_memories(
    user_id=customer_id
)

print(memories)