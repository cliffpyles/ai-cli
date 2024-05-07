# commands/commands.py

def create_prompt(prompt_name, content):
    print(f"Creating prompt '{prompt_name}' with content: {content}")

def list_prompts():
    print("Listing all prompts...")

def remove_prompt(prompt_name):
    print(f"Removing prompt '{prompt_name}'")

def send_message(message_or_prompt_name, service, model, requests, file, output_type, prompt_variables):
    print(f"Sending '{message_or_prompt_name}' to service {service} using model {model} with {requests} requests")
    # Add additional functionality here
