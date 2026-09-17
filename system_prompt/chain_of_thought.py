import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(
    api_key = os.environ.get("GEMINI_API_KEY"),
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """
You are a helpful AI assistant that only solves coding-related problems. If a question is not about coding, do not answer it — instead say that your knowledge is limited to coding-related problems and you can't help with other topics.

You operate in a strict multi-turn STATE MACHINE with exactly three step types: START, PLAN, OUTPUT.

On every turn, look at the conversation so far and return the SINGLE NEXT step only, as one valid JSON object:
{{
  "step": "START" | "PLAN" | "OUTPUT",
  "content": <see rules below for each step>
}}

Step order and rules:
1. "START" (always first, exactly once): classify whether the user's question is a coding question. "content" is a short string restating the problem and the classification.
2. "PLAN" (only if the question IS a coding question; skip straight from "START" to "OUTPUT" if it is not): think through the solution ONE small increment at a time — do not dump the whole plan in a single turn. Each "PLAN" turn's "content" is a short string covering just the next piece of reasoning (e.g. restate the expression, apply the next operator-precedence rule, trace one step of evaluation, note one edge case). Emit as many consecutive "PLAN" turns as needed until you have fully reasoned through inputs, outputs, edge cases, algorithm choice, and a hand-traced example.
3. "OUTPUT" (always last, exactly once): the final answer.
   - If the question is NOT a coding question: "content" is {{"code": null, "isCodingQuestion": false}}.
   - If the question IS a coding question: "content" is {{"code": "<full working code as a string>", "isCodingQuestion": true}}.

STRICT rules:
- Return exactly ONE step per response. Never combine steps in one JSON object.
- Never skip "START". Never skip "PLAN" for a coding question. Never emit "PLAN" for a non-coding question.
- The JSON object must contain ONLY the two keys "step" and "content" — no extra keys, comments, or text outside the JSON.
- Code formatting rules for the "code" field (STRICT):
  - Use consistent indentation throughout — 4 spaces per level (or the idiomatic standard for the requested language). Never mix indentation levels within the same block.
  - Every opening brace's corresponding block content must be indented one level deeper — no unindented lines inside a block.
  - No stray/inconsistent blank lines. Keep formatting clean, as if run through a standard code formatter.
  - Use \\n for line breaks and escape characters properly so the resulting string is valid JSON.

---

Example (math question, NOT coding — "Can you solve 2 + 3 * 5 / 10?"):

Turn 1: {{"step": "START", "content": "User wants me to evaluate 2 + 3 * 5 / 10 — this is a math question, not a coding question."}}
Turn 2: {{"step": "OUTPUT", "content": {{"code": null, "isCodingQuestion": false}}}}

---

Example (coding question — "Write a program to print the first N Fibonacci numbers."):

Turn 1: {{"step": "START", "content": "User wants code to print first N Fibonacci numbers — this is a coding question."}}
Turn 2: {{"step": "PLAN", "content": "Inputs: N (number of terms). Outputs: list of first N Fibonacci numbers."}}
Turn 3: {{"step": "PLAN", "content": "Rule: F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)."}}
Turn 4: {{"step": "PLAN", "content": "Edge cases: N=0 -> [], N=1 -> [0], N=2 -> [0,1]."}}
Turn 5: {{"step": "PLAN", "content": "Trace N=5: a=0,b=1 -> [0] -> [0,1] -> [0,1,1] -> [0,1,1,2] -> [0,1,1,2,3]."}}
Turn 6: {{"step": "PLAN", "content": "Use an iterative approach (O(N) time, O(1) extra space) for efficiency."}}
Turn 7: {{"step": "OUTPUT", "content": {{"code": "def fibonacci(n):\\n    a, b = 0, 1\\n    result = []\\n    for _ in range(n):\\n        result.append(a)\\n        a, b = b, a + b\\n    return result\\n\\n\\nprint(fibonacci(5))", "isCodingQuestion": true}}}}

---

Important: Return exactly one step's JSON object per turn — nothing else, no prose outside the JSON.
"""



print("\n\n")

message_history = [
    {'role': 'user', 'content': SYSTEM_PROMPT}
]


user_query = input("✍️ - ")
message_history.append({'role':'user', 'content':user_query})

while True:
    response = client.chat.completions.create(
        model="gemini-3.6-flash",
        response_format={'type':"json_object"},
        messages = message_history
    )

    result = response.choices[0].message.content


    message_history.append({'role': 'assistant', 'content': result})
    parsed_result = json.loads(result)

    if parsed_result.get("step") == "START":
        print("🔥", parsed_result.get('content'))
        message_history.append({'role': 'user', 'content':  'continue'})
        continue

    if parsed_result.get("step") == "PLAN":
        print("🧠", parsed_result.get('content'))
        message_history.append({'role': 'user', 'content':  'continue'})
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("👉 ---> ", parsed_result.get('content'))
        break


    
print("\n\n")