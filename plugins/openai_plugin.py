from .base_plugin import BasePlugin
import openai


class OpenAIPlugin(BasePlugin):
    def __init__(self):
        super().__init__("OpenAI")
        self.client = openai.OpenAI()

    def send_prompt(self, prompt, model, requests, file_paths, output_type, variables):
        settings, template_variables, _ = self.load_prompt(prompt)
        messages = []
        temperature = settings.get("temperature", None)

        # Merge the provided variables with variables found in prompt
        template_variables.update(variables)

        # Set the system context
        system_context = settings.get("system_context", "")
        messages.append({"role": "system", "content": system_context})

        # Attach the file contents
        files = self.load_files(file_paths)
        for file_path, file_content in files.items():
            messages.append({"role": "user", "content": f"FILE_PATH:{file_path}\n\nFILE_CONTENT:\n{file_content}"})

        # Build the user message
        user_message = _.format(**template_variables)
        if output_type == "json":
            user_message += "\n\nFormat the response as json."
        messages.append({"role": "user", "content": user_message})

        # Set the response format
        response_format = "json_object" if output_type == "json" else "text"

        # Send the messages
        try:
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                response_format={"type": response_format}
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Failed to send message: {str(e)}")
            raise

    def send_message(self, message, model, requests, file_paths, output_type, variables):
        system_context = "You are a helpful assistant."
        response_format = {"type": "json_object" if output_type == "json" else "text"}
        messages = []

        # Set the system context
        messages.append({"role": "system", "content": system_context})

        # Attach the file contents
        files = self.load_files(file_paths)
        for file_path, file_content in files.items():
            messages.append({"role": "user", "content": f"FILE_PATH:{file_path}\n\nFILE_CONTENT:\n{file_content}"})

        # Build the user message
        user_message = message.format(**variables)
        if output_type == "json":
            user_message += "\n\nFormat the response as json."
        messages.append({"role": "user", "content": user_message})

        # Set the response format
        response_format = "json_object" if output_type == "json" else "text"

        # Send the messages
        try:
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                response_format={"type": response_format}
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Failed to send message: {str(e)}")
            raise

    def send(self, prompt, message, model, requests, file, output_type, variables):
        if prompt:
            return self.send_prompt(prompt, model, requests, file, output_type, variables)
        elif message:
            return self.send_message(message, model, requests, file, output_type, variables)

