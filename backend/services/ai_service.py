import os

def ask_ai(question, context, history=None):
    # Simple fallback if no OPENAI_API_KEY
    # It will just return context snippet so backend starts
    if not os.getenv("OPENAI_API_KEY"):
        snippet = context[:500] if context else "No document loaded."
        return f"[DEMO MODE - No API key] Your question: '{question}'. Document preview: {snippet}"
    # If you have API key, you can add OpenAI code later
    try:
        from openai import OpenAI
        client = OpenAI()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Use this document: {context[:8000]}"},
                {"role": "user", "content": question}
            ]
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"AI error: {e}"

def generate_quiz(context, num=5):
    # Dummy quiz so app runs
    return [
        {"question": "What is this document about?", "options": ["A", "B", "C", "D"], "answer": "A"},
        {"question": f"Question 2 from document?", "options": ["A", "B", "C", "D"], "answer": "B"},
    ]

def summarize(context):
    if not context:
        return "No document"
    return context[:500] + "... [summary demo]"