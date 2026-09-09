from mem0 import Memory
from email.parser import Parser
from dotenv import load_dotenv

from config import config

load_dotenv("../.env")

# Initialize local Mem0

memory = Memory.from_config(config)

class EmailProcessor:
def **init**(self):
"""Initialize the Email Processor with local Mem0 memory"""
self.memory = memory

```
def process_email(self, email_content, user_id):
    """
    Process an email and store it in Mem0 memory
    """

    # Parse email
    parser = Parser()
    email = parser.parsestr(email_content)

    # Extract email details
    sender = email["from"]
    recipient = email["to"]
    subject = email["subject"]
    date = email["date"]
    body = self._get_email_body(email)

    # Create message object for Mem0
    message = {
        "role": "user",
        "content": f"Email from {sender}: {subject}\n\n{body}",
    }

    # Create metadata for better retrieval
    metadata = {
        "email_type": "incoming",
        "sender": sender,
        "recipient": recipient,
        "subject": subject,
        "date": date,
        "category": "email",
    }

    # Store using local Mem0
    response = self.memory.add(
        messages=[message],
        user_id=user_id,
        metadata=metadata,
    )

    return response

def _get_email_body(self, email):
    """Extract the body content from an email"""

    # Simplified extraction
    if email.is_multipart():
        for part in email.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode()
    else:
        return email.get_payload(decode=True).decode()

def search_emails(self, query, user_id):
    """
    Search through stored emails
    """

    # Search relevant memories for this user
    results = self.memory.search(
        query=query,
        filters={"user_id": user_id},
        limit=10,
    )

    # Keep only email-related memories
    email_results = [
        result
        for result in results["results"]
        if result.get("metadata", {}).get("category") == "email"
    ]

    return {"results": email_results}

def get_email_thread(self, subject, user_id):
    """
    Retrieve all emails in a thread based on subject
    """

    # Get all memories for this user
    results = self.memory.get_all(
        filters={"user_id": user_id}
    )

    # Filter email memories by subject
    thread = [
        result
        for result in results["results"]
        if result.get("metadata", {}).get("category") == "email"
        and subject.lower()
        in result.get("metadata", {}).get("subject", "").lower()
    ]

    return {"results": thread}
```

# Initialize the processor

processor = EmailProcessor()

# Example raw email

sample_email = """From: [alice@example.com](mailto:alice@example.com)
To: [bob@example.com](mailto:bob@example.com)
Subject: Meeting Schedule Update
Date: Mon, 15 Jul 2024 14:22:05 -0700

Hi Bob,

I wanted to update you on the schedule for our upcoming project meeting.
We'll be meeting this Thursday at 2pm instead of Friday.

Could you please prepare your section of the presentation?

Thanks,
Alice
"""

# Process and store the email

user_id = "[bob@example.com](mailto:bob@example.com)"

response = processor.process_email(
sample_email,
user_id
)

print("\nMemory result:")
print(response)

# Search for emails about meetings

meeting_emails = processor.search_emails(
"meeting schedule",
user_id
)

print(
f"\nFound {len(meeting_emails['results'])} "
f"relevant emails"
)

print(meeting_emails)

# Retrieve email thread

thread = processor.get_email_thread(
"Meeting Schedule",
user_id
)

print(
f"\nFound {len(thread['results'])} "
f"emails in the thread"
)

print(thread)
