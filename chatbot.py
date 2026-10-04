import json
from pathlib import Path

# Load Q&A
qa_file = Path("knowledge/qa.json")

with open(qa_file, "r", encoding="utf-8") as f:
    qa = json.load(f)

print("=" * 40)
print("   මගේම AI  (ඉතාම ලේසි)")
print("=" * 40)
print("\nප්‍රශ්න අහන්න (ඉවත් වෙන්න 'exit')\n")

while True:
    question = input("ඔබ: ").strip()

    if question.lower() in ["exit", "quit", "ඉවත්", "bye"]:
        print("AI: බයි! ආයුබෝවන්!")
        break

    if not question:
        continue

    # Simple matching
    answer = None
    q_lower = question.lower()

    # Exact match
    if question in qa:
        answer = qa[question]
    elif q_lower in qa:
        answer = qa[q_lower]
    else:
        # Partial match
        for key, value in qa.items():
            if key.lower() in q_lower or q_lower in key.lower():
                answer = value
                break

    if answer:
        print(f"AI: {answer}\n")
    else:
        print("AI: මට ඒ ගැන තොරතුරු නැහැ.\n")
