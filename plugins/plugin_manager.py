class PluginManager:
    def __init__(self):
        self.plugins = {}

    def register_plugin(self, plugin):
        self.plugins[plugin.service_name] = plugin

    def send_message(self, service_name, message, model, requests, file, output_type, variables):
        plugin = self.plugins.get(service_name)
        if not plugin:
            raise ValueError(f"No plugin found for service {service_name}")
        return plugin.send(message, model, requests, file, output_type, variables)
