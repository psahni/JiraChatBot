from openai import OpenAI
from bot.actions import filterIssuesByStatus
from bot.prompt import system_prompt

model_name = "interstellarninja/hermes-2-pro-llama-3-8b-tools:latest"
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

available_functions = {
    "filterIssuesByStatus": filterIssuesByStatus
}

filterIssuesByStatus = {
    "name": "filterIssuesByStatus",
    "description": "Filter issues by status based on status parameter provided",
    "parameters": {
        "status": {
            "type": "string",
            "description": "status of issues need to filtered"
        },
        "required": ["status"]
    },
}


def genAIResponse(response):
    response = client.chat.completions.create(
        model=model_name,
        temperature=0.7,
        messages=[
            {
                "role": "assistant",
                "content": f"You are AI assistant, you generate meaningful response from text input. Context: {response}. Generate meaningful response from the context given"
            }
        ],
    )

    return response.choices[0].message.content

def process(query):
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": query
        }
    ]


    response = client.chat.completions.create(
        model=model_name,
        temperature=0.7,
        messages=messages,
        tools=[filterIssuesByStatus],
        function_call="auto"
    )

    message = response.choices[0].message
    response_messages = []
    print(message)
    for tool in message.tool_calls:
        function_to_call = available_functions.get(tool.function.name)
        if function_to_call:
            resp = function_to_call(tool.function.arguments)
            response_messages.append(genAIResponse(resp))

    return response_messages

# output = main("List all the issues on which comment has been added. Please also tell ticket ID")
# print('\n'.join(output))
# List all the issues on which MULTIPLE_UPDATE. Please give Jira issue ID also.