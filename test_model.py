from openai import OpenAI
import json
from sample_audit_data import audit_data

model_name = "interstellarninja/hermes-2-pro-llama-3-8b-tools:latest"
api_key = "ollama"

# query = ("Please generate detailed summary of the audit response. "
#          "Please cover every comment left. "
#          "Please list every issue has status transition"
#          "Please list every issue has assignee changed"
#          "Give me summary in bulleted list")

query = ("Please give list of tickets with IDs with ASSIGNEE_CHANGED. Include all detail of the ticket. Please give text response in bulleted list")
def generate_summary(audit_data) -> str:
    """
    Send a question about audit of activities to the LLM for processing
    Args:
        audit_data (list[dict]): This is array of audit data in json format, contains activity information as each json element
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
        temperature=0.7,
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

output = generate_summary(audit_data)
print(output)