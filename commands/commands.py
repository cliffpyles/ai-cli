# commands/commands.py
from pathlib import Path
import json

# Base directory for storing prompts
BASE_DIR = Path.home() / '.ask-ai'
PROMPTS_DIR = BASE_DIR / 'prompts'
CONFIG_FILE = BASE_DIR / 'settings.json'

def setup_config():
    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        # Default configuration settings
        config_data = {
            'service': 'OpenAI',
            'model': 'gpt-4-turbo-preview',
            'format': 'text'
        }
        CONFIG_FILE.write_text(json.dumps(config_data, indent=4))
        print("Configuration file created.")
    else:
        print("Configuration file already exists.")

def create_prompt(prompt_name, content):
    """
    Create a new prompt file with specified content.
    
    Args:
        prompt_name (str): Name of the prompt file to create.
        content (str): Content to write into the prompt file.
    """
    prompt_path = PROMPTS_DIR / f"{prompt_name}.md"
    if prompt_path.exists():
        raise FileExistsError(f"Prompt '{prompt_name}' already exists.")
    prompt_path.write_text(content)
    print(f"Prompt '{prompt_name}' created successfully.")


def list_prompts():
    """
    List all existing prompt files in the directory.
    
    Returns:
        list of str: List of names of all prompt files.
    """
    return [file.stem for file in PROMPTS_DIR.glob('*.md')]

def remove_prompt(prompt_name):
    """
    Remove a specified prompt file.
    
    Args:
        prompt_name (str): Name of the prompt file to remove.
    """
    prompt_path = PROMPTS_DIR / f"{prompt_name}.md"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt '{prompt_name}' does not exist.")
    prompt_path.unlink()
    print(f"Prompt '{prompt_name}' removed successfully.")


def send_message(message_or_prompt_name, service, model, requests, file, output_type, prompt_variables):
    print(f"Sending '{message_or_prompt_name}' to service {service} using model {model} with {requests} requests")
    # Add additional functionality here
