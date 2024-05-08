import frontmatter
from pathlib import Path
from config import PROMPTS_DIR


class BasePlugin:
    def __init__(self, service_name):
        self.service_name = service_name.lower()

    def load_files(self, file_paths=[]):
        loaded_files = {}

        for file_path in file_paths:
            file = Path(file_path)

            if not file.exists():
                raise FileNotFoundError(f"File '{file_path}' does not exist.")

            file_content = file.read_text()
            loaded_files[file_path] = file_content

        return loaded_files

    def load_prompt(self, prompt_name):
        prompt_path = PROMPTS_DIR / f"{prompt_name}.md"
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt '{prompt_name}' does not exist.")

        with open(prompt_path, 'r') as file:
            parsed_prompt = frontmatter.load(file)

        # Normalize keys in _settings to lowercase
        settings = {k.lower(): v for k, v in parsed_prompt.metadata.get('_settings', {}).items()}

        # Extract settings specifically for this plugin, ensuring case insensitivity
        plugin_settings = settings.get(self.service_name, {})

        # Extract all other variables excluding '_settings'
        variables = {k: v for k, v in parsed_prompt.metadata.items() if k != '_settings'}

        content = parsed_prompt.content
        return plugin_settings, variables, content

    def send(self, prompt, message, model, requests, file, output_type, variables):
        raise NotImplementedError("Each plugin must implement the 'send' method.")
