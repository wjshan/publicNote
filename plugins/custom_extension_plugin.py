from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin


class CustomExtensionPlugin(BasePlugin):
    config_scheme = (
        ("include_extensions", config_options.Type(list, default=[])),
    )

    def on_pre_page(self, page, config, files):
        for name in self.config["include_extensions"]:
            extension = __import__(name, fromlist=(name,))
            config["markdown_extensions"].append(extension.makeExtension(page=page, config=config, files=files))
        return page
