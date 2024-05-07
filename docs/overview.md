# Overview

This CLI tool facilitates interaction with AI services, providing a streamlined way to manage prompts and send queries directly from the command line. It's designed for developers, data scientists, and AI enthusiasts looking to leverage AI models without the need for a GUI.

## Installation
To install the CLI tool, run the following command:
```
pip install ai-cli
```

## Commands

### Config

Set up the initial configuration.

**Syntax:** `ai config`

### Prompt

Manage prompt files used with AI services.

**Syntax:** `ai prompt <subcommand> [...arguments]`

#### Subcommands

##### Create

Create a prompt file.

**Syntax:** `ai prompt create <promptName> [--options]`

**Examples:**
```
ai prompt create "new_prompt_name"
ai prompt create "new_prompt_name" --content "Describe the current trends in AI."
```

###### Options

- **--content, -c <promptContent>**: Specifies the text content of the new prompt.

##### List

List all existing prompts.

**Syntax:** `ai prompt list [--options]`

##### Remove

Remove a prompt file.

**Syntax:** `ai prompt remove <promptName> [--options]`

##### Send

Send a message or a prompt to an AI service.

**Syntax:** `ai send <messageOrPromptName> [--options] [...promptVariables]`

**Examples:**
```
ai send "Give me a list of 25 major cities"
ai send "Give me a list of {count} major cities" count=25
```

###### Options

- **--service, -s <serviceName>**: Specifies which AI service to use (default is OpenAI).
- **--model, -m <modelName>**: Designates the AI model to employ (default is gpt-4-turbo-preview).
- **--requests, -r**: Determines how many requests to break up the message into (default is 1).
- **--file <filePath>**: Specifies a file to use for the context of the question.
- **--format <outputType>**: Defines the format of the response (e.g., `json`, `text`).

## Configuration

Settings are stored in the `~/.ask-ai/settings.json` file, which allows you to configure default values for services, models, and other options. Prompts are managed within the `~/.ask-ai/prompts` folder.

## Getting Help

For detailed command usage and help, use the `--help` flag with any command:

```
ai --help
ai prompt --help
```

## Troubleshooting

For common issues:
- **File Not Found**: Ensure the file path in the `--file` option is correct.
- **Service Unreachable**: Check your network settings and service availability.

Should you encounter error messages such as "Invalid command syntax", make sure to check the command syntax and available options by running `ai --help`.
