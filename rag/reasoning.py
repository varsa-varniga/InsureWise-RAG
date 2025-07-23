import requests
from config import TOGETHER_API_KEY
from utils.formatter import format_context_chunks

# ✅ Using Together AI's hosted Mistral model
LLM_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"
def clean_text(text: str) -> str:
    return text.replace('\n', ' ').replace('\s', ' ').strip()
def build_prompt(query: str, retrieved_chunks: list) -> str:
    """
    Builds a structured prompt for the LLM using retrieved document chunks.
    """
    context = "\n\n".join([
        f"Clause {i+1}:\n{chunk}" for i, (chunk, _) in enumerate(retrieved_chunks)
    ])

    return f"""
You are an insurance policy expert.

Below is a user query:
"{query}"

And here are the most relevant clauses retrieved from a policy document:

{context}

Your task is to:
1. Decide if the procedure is approved or rejected
2. Specify the payout amount (if mentioned)
3. Reference specific clauses that led to your conclusion

Return your answer in this JSON format:
{{
  "decision": "approved" or "rejected",
  "amount": "₹<number>" or null,
  "justification": {{
    "clause_reference": "Clause 2 or Clause 3.1",
    "clause_text": "....short summary of what the clause says...",
    "mapped_entities": {{
      "age": "...",
      "procedure": "...",
      "location": "...",
      "policy_duration": "..."
    }}
  }}
}}

Only output JSON. Be logical and concise.
""".strip()


def build_definition_prompt(query: str, context_chunks: list) -> str:
    """
    Builds a prompt for simpler, definition-style questions.
    """
    context_text = "\n\n".join(chunk[0] for chunk in context_chunks)

    return f"""
You are an expert insurance assistant.

Based on the following policy context, answer the user's informational question:

Context:
{context_text}

Question:
{query}

Give your answer in simple and clear terms. Respond in the following JSON format:
{{
  "type": "definition",
  "definition": "<your explanation here>"
}}
""".strip()


def get_llm_response(prompt: str) -> str:
    """
    Sends the prompt to Together AI's hosted LLM and returns the response content.
    """
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": LLM_MODEL,
        "max_tokens": 512,
        "temperature": 0.3,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
