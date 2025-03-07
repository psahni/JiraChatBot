from openai import OpenAI
import json

model_name = "codellama:13b-instruct"
api_key = "ollama"

query = ("Please generate detailed summary of the audit response, cover every important detail like comment left, issue status change etc."
         "Give me bulleted list")

def generate_summary(audit_data) -> str:
    """
    Send a question about audit of activities to the LLM for processing
    Args:
        question (str): Natural language question about audit of activities
    Returns:
        str: LLM's response to the question
    """

    context = json.dumps(audit_data, indent=2)
    prompt = (
        "You are an JIRA analytics assistant. Use the following audit data to answer the question or summary generation:\n\n"
        f"{context}\n\n"
        f"Query: {query}\n\n"
        "Answer:"
    )

    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )

    response = client.chat.completions.create(
        model=model_name,
        temperature=0.2,
        messages=[
            {
             "role": "system",
              "content": "You are a helpful JIRA analytics assistant skilled at extracting insights from audit data\n"
              "You are capable of generating summary\n"
              "Always generate text response. Do not give json response"
             },
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()
