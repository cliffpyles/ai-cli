from pathlib import Path

# Base directory for configuration and prompts
BASE_DIR = Path.home() / '.ask-ai'
PROMPTS_DIR = BASE_DIR / 'prompts'
CONFIG_FILE = BASE_DIR / 'settings.json'

# Default configuration settings
DEFAULT_SETTINGS = {
    'service': 'OpenAI',
    'model': 'gpt-4-turbo-preview',
    'format': 'text'
}
