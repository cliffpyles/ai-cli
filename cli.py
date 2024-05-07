#!/usr/bin/env python3

import click
import json
import os
from commands.commands import create_prompt, list_prompts, remove_prompt, send_message, setup_config

# Function to load settings
def load_settings():
    settings_path = os.path.expanduser('~/.ask-ai/settings.json')
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as file:
            return json.load(file)
    else:
        return {
            'service': 'OpenAI',
            'model': 'gpt-4-turbo-preview',
            'format': 'text'
        }

settings = load_settings()

@click.group()
def cli():
    """This CLI tool facilitates interaction with AI services from the command line."""
    pass

@cli.command('config', help='Set up the initial configuration.')
def config():
    setup_config()

@cli.group(help='Manage prompt files used with AI services.')
def prompt():
    pass

@prompt.command('create', help='Create a prompt file.')
@click.argument('promptname')
@click.option('--content', '-c', default='', help='Specifies the text content of the new prompt.')
def create(promptname, content):
    try:
        create_prompt(promptname, content)
        click.echo(f"Prompt '{promptname}' created successfully.")
    except Exception as e:
        click.echo(f"Failed to create prompt: {str(e)}", err=True)

@prompt.command('list', help='List all existing prompts.')
def list():
    try:
        prompts = list_prompts()
        for prompt in prompts:
            click.echo(prompt)
    except Exception as e:
        click.echo(f"Failed to list prompts: {str(e)}", err=True)

@prompt.command('remove', help='Remove a prompt file.')
@click.argument('promptname')
def remove(promptname):
    try:
        remove_prompt(promptname)
        click.echo(f"Prompt '{promptname}' removed successfully.")
    except Exception as e:
        click.echo(f"Failed to remove prompt: {str(e)}", err=True)

@cli.command('send', help='Send a message or a prompt to an AI service.')
@click.argument('messageorpromptname')
@click.option('--service', '-s', default=settings['service'], help='Specifies which AI service to use.')
@click.option('--model', '-m', default=settings['model'], help='Designates the AI model to employ.')
@click.option('--requests', '-r', default=1, type=int, help='Determines how many requests to break up the message into.')
@click.option('--file', type=click.Path(exists=True), help='Specifies a file to use for the context of the question.')
@click.option('--format', 'outputtype', default=settings['format'], type=click.Choice(['json', 'text']), help='Defines the format of the response.')
@click.argument('promptvariables', nargs=-1)
def send(messageorpromptname, service, model, requests, file, outputtype, promptvariables):
    try:
        variables = {}
        for var in promptvariables:
            key, value = var.split('=')
            variables[key] = value
        send_message(messageorpromptname, service, model, requests, file, outputtype, variables)
        click.echo("Message sent successfully.")
    except ValueError:
        click.echo("Error parsing prompt variables. Use format 'key=value'.", err=True)
    except Exception as e:
        click.echo(f"Failed to send message: {str(e)}", err=True)

@cli.command('help', help='Detailed command usage and help.')
@click.argument('command', required=False)
def help(command):
    if command is None:
        click.echo(cli.get_help(click.Context(cli)))
    else:
        command_obj = cli.get_command(click.Context(cli), command)
        if command_obj is None:
            click.echo(f"No help found for '{command}'", err=True)
        else:
            click.echo(command_obj.get_help(click.Context(command_obj)))

if __name__ == '__main__':
    cli()
