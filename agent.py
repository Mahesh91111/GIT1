import os
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

# ===============================
# Load API Key
# ===============================
load_dotenv() ## this is a load the .env file and set the environment variables

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ===============================
# System Prompt
# ===============================
SYSTEM_PROMPT = """
You are an intelligent AI Assistant.

Your Responsibilities:
- Answer user questions.
- Think step by step.
- Be accurate and concise.
- Use available tools whenever required.
"""

# ===============================
# Tool Functions
# ===============================

def get_current_time():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def calculator(expression):
    try:
        return eval(expression)
    except Exception:
        return "Invalid mathematical expression."


# ===============================
# AI Agent
# ===============================

class AIAgent: ## agnt

    def __init__(self):
        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

    def check_tool(self, query):

        q = query.lower()

        if "time" in q or "date" in q:
            return get_current_time()

        if "calculate" in q:
            exp = q.replace("calculate", "").strip()
            return calculator(exp)

        if any(op in q for op in ["+", "-", "*", "/", "%"]):
            return calculator(q)

        return None

    def chat(self, user_input):

        # Tool Calling
        tool_result = self.check_tool(user_input)

        if tool_result:
            return f"Tool Result:\n{tool_result}"

        self.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=self.messages,
            temperature=0.7,
            max_tokens=2048,
        )

        answer = response.choices[0].message.content

        self.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        return answer


# ===============================
# Main Function
# ===============================

def main():

    print("=" * 60)
    print("🚀 Groq AI Agent")
    print("Type 'exit' to quit")
    print("=" * 60)

    agent = AIAgent()

    while True:

        query = input("\nYou : ")

        if query.lower() == "exit":
            print("\n👋 Goodbye!")
            break

        try:
            response = agent.chat(query)
            print("\nAgent :", response)

        except Exception as e:
            print("\nError :", e)


if __name__ == "__main__":
    main()