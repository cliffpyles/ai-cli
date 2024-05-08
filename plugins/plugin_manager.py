class PluginManager:
    def __init__(self):
        self.plugins = {}

    def register_plugin(self, plugin):
        self.plugins[plugin.key] = plugin

    def list_plugins(self):
        all_plugins = []
        for plugin in self.plugins.values():
            all_plugins.append(plugin.get_info())
        return all_plugins

    def send(self, prompt, message, service_name, model, requests, file, output_type, variables):
        plugin = self.plugins.get(service_name.lower())
        if not plugin:
            raise ValueError(f"No plugin found for service {service_name}")
        return plugin.send(prompt, message, model, requests, file, output_type, variables)
