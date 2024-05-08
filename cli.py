#!/usr/bin/env python3

import click
import json
import os
from commands.commands import create_prompt, list_prompts, remove_prompt, setup_config
from plugins.plugin_manager import PluginManager
from plugins.openai_plugin import OpenAIPlugin

# Initialize Plugin Manager and register plugins
plugin_manager = PluginManager()
openai_plugin = OpenAIPlugin()
plugin_manager.register_plugin(openai_plugin)


# Load settings
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
    """CLI tool for interacting with AI services from the command line."""
    pass


@cli.command('config', help='Set up the initial configuration.')
def config():
    setup_config()


@cli.group(help='Manage prompts used for service interactions.')
def prompt():
    pass

@prompt.command('create', help='Create a prompt file.')
@click.argument('promptname')
@click.option('--content', '-c', default='', help='Specifies the text content of the new prompt.')
def prompt_create(promptname, content):
    try:
        create_prompt(promptname, content)
        click.echo(f"Prompt '{promptname}' created successfully.")
    except Exception as e:
        click.echo(f"Failed to create prompt: {str(e)}", err=True)


@prompt.command('list', help='List all existing prompts.')
def prompt_list():
    try:
        prompts = list_prompts()
        for prompt in prompts:
            click.echo(prompt)
    except Exception as e:
        click.echo(f"Failed to list prompts: {str(e)}", err=True)


@prompt.command('remove', help='Remove a prompt file.')
@click.argument('promptname')
def prompt_remove(promptname):
    try:
        remove_prompt(promptname)
        click.echo(f"Prompt '{promptname}' removed successfully.")
    except Exception as e:
        click.echo(f"Failed to remove prompt: {str(e)}", err=True)


@cli.command('send', help='Send a message or prompt to a service.')
@click.option('--prompt', '-p', help='Specifies the name of a prompt to use.')
@click.option('--message', '-m', help='Specifies a raw message to send.')
@click.option('--service', '-s', default=settings['service'], help='Specifies which service to use.')
@click.option('--model', '-m', default=settings['model'], help='Designates the AI model to employ.')
@click.option('--requests', '-r', default=1, type=int, help='Determines how many requests to break up the message into.')
@click.option('--file', type=click.Path(exists=True),  multiple=True, help='Specifies a file to use for the context of the question.')
@click.option('--format', 'outputtype', default=settings['format'], type=click.Choice(['json', 'text']), help='Defines the format of the response.')
@click.argument('promptvariables', nargs=-1)
def send(prompt, message, service, model, requests, file, outputtype, promptvariables):
    if not (prompt or message):
        click.echo("You must specify either a prompt or a message.", err=True)
        return

    if prompt and message:
        click.echo("You must specify either a prompt or a message, but not both.", err=True)
        return

    try:
        variables = {}
        for var in promptvariables:
            key, value = var.split('=')
            variables[key] = value

        response = plugin_manager.send(prompt, message, service, model, requests, file, outputtype, variables)
        click.echo(response)
    except ValueError:
        click.echo("Error parsing prompt variables. Use format 'key=value'.", err=True)
    except Exception as e:
        click.echo(f"Failed to send message: {str(e)}", err=True)


@cli.group(help='Manage plugins used for extending service support.')
def plugin():
    pass


@plugin.command('list', help='List all plugins.')
def plugin_list():
    try:
        for plugin in plugin_manager.list_plugins():
            click.echo(f"{plugin['name']} - {plugin['description']}")
    except Exception as e:
        click.echo(f"Failed to list plugins: {str(e)}", err=True)


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
