import re

from markdown import Extension
from markdown.treeprocessors import Treeprocessor

RE_CHECKBOX = re.compile(r"^(?P<checkbox> *\[(?P<state>(?:x|X| ){1})\] +)(?P<line>.*)", re.DOTALL)


class LocalFileTreeprocessor(Treeprocessor):
    """Tasklist tree processor that finds lists with checkboxes."""

    def __init__(self, md, page, config, files):
        """Initialize."""
        self.page = page
        self.page_config = config
        self.files = files

        super(LocalFileTreeprocessor, self).__init__(md)

    def find_abs_path(self, name):
        for file_name, file in self.files.src_paths.items():
            if name[2:] in file_name:
                return file.url
        return  name

    def run(self, root):
        """Find list items that start with [ ] or [x] or [X]."""
        for element in root.iter():
            if element.tag == 'a':
                key = 'href'
            elif element.tag == "img":
                key = 'src'
            else:
                continue
            url: str = element.get(key, "")
            if url.startswith("$$"):
                abs_url = self.find_abs_path(url)
                element.set(key, "/"+abs_url)
        return root


class LocalFileExtension(Extension):
    """Tasklist extension."""

    def __init__(self, page, config, files):
        """Initialize."""
        self.page = page
        self.page_config = config
        self.files = files
        super(LocalFileExtension, self).__init__()

    def extendMarkdown(self, md):
        """Add checklist tree processor to Markdown instance."""

        local_file = LocalFileTreeprocessor(md, self.page, self.page, self.files)
        local_file.config = self.getConfigs()
        md.treeprocessors.register(local_file, "local_file", 1)  # 设置优先级
        md.registerExtension(self)


def makeExtension(*args, **kwargs):
    """Return extension."""
    return LocalFileExtension(*args, **kwargs)
