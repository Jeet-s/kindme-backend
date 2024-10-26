from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "meta-llama/Meta-Llama-3-8B"  
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)

# Move the model to the GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)


def generate_response(prompt, max_length=100):
    # Tokenize the prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    
    # Generate the response
    outputs = model.generate(
        **inputs,
        max_length=max_length,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Example usage
prompt = "What are the applications of artificial intelligence?"
response = generate_response(prompt)
print("Response:", response)


