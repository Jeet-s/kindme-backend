import requests
import json
from prompt import issue_type_prompt

LLAMA_URL = "https://Meta-Llama-3-70B-Instruct-jpuky-serverless.eastus2.inference.ai.azure.com/v1/chat/completions"
LLAMA_API_KEY = "RTnzabZ71DBrS2vbT26fvVdUzX1a9MDn"

def call_llama(prompt):
    
    raw_output = None
    payload = json.dumps({
    "messages": [
        {
            "role": "user",
            "content":prompt
        }
        ],
        "max_tokens": 256,
        "temperature": 0.8,
        "top_p": 0.1,
        "best_of": 1,
        "presence_penalty": 0,
        "use_beam_search": False,
        "ignore_eos": False,
        "skip_special_tokens": False,
        "logprobs": False,
        "top_logprobs": None
    })

    headers = {
    'Authorization': 'Bearer ' + LLAMA_API_KEY,
    'Content-Type': 'application/json'
    }

    response = requests.post(LLAMA_URL, headers=headers, data=payload)
    choices = json.loads(response.text)["choices"]
    raw_output = choices[0].get("message").get("content")
    #result = json.loads(raw_output)
    
    data = json.loads(raw_output)
    print(data)
    return data
        
#text = call_llama(issue_type_prompt)
#print(text)