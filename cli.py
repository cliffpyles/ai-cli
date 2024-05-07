#!/usr/bin/env python3

import click
import json
import os

from commands.commands import create_prompt, list_prompts, remove_prompt, send_message

# Function to load settings
def load_settings():
    settings_path = os.path.expanduser('~/.ask-ai/settings.json')
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as file:
            return json.load(file)
    return {}

@click.group()
def cli():
    """This CLI tool facilitates interaction with AI services from the command line."""
    pass

@cli.group(help='Manage prompt files used with AI services.')
def prompt():
    pass

@prompt.command('create', help='Create a prompt file.')
@click.argument('promptname')
@click.option('--content', '-c', default='', help='Specifies the text content of the new prompt.')
def create(promptname, content):
    create_prompt(promptname, content)

@prompt.command('list', help='List all existing prompts.')
def list():
    list_prompts()

@prompt.command('remove', help='Remove a prompt file.')
@click.argument('promptname')
def remove(promptname):
    remove_prompt(promptname)

@cli.command('send', help='Send a message or a prompt to an AI service.')
@click.argument('messageorpromptname')
@click.option('--service', '-s', default='OpenAI', help='Specifies which AI service to use.')
@click.option('--model', '-m', default='gpt-4-turbo-preview', help='Designates the AI model to employ.')
@click.option('--requests', '-r', default=1, type=int, help='Determines how many requests to break up the message into.')
@click.option('--file', type=click.Path(exists=True), help='Specifies a file to use for the context of the question.')
@click.option('--format', 'outputtype', default='text', type=click.Choice(['json', 'text']), help='Defines the format of the response.')
@click.argument('promptvariables', nargs=-1)
def send(messageorpromptname, service, model, requests, file, outputtype, promptvariables):
    send_message(messageorpromptname, service, model, requests, file, outputtype, promptvariables)

@cli.command('help', help='Detailed command usage and help.')
@click.argument('command', required=False)
def help(command):
    if command is None:
        click.echo(cli.get_help(click.Context(cli)))
    else:
        command_obj = cli.get_command(click.Context(cli), command)
        if command_obj is None:
            click.echo(f"No help found for '{command}'")
        else:
            click.echo(command_obj.get_help(click.Context(command_obj)))

if __name__ == '__main__':
    cli()
