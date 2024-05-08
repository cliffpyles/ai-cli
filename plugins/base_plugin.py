class BasePlugin:
    def __init__(self, service_name):
        self.service_name = service_name

    def send(self, message, model, requests, file, output_type, variables):
        raise NotImplementedError("Each plugin must implement the 'send' method.")

