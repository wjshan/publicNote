import os

import dateutil.parser
from mkdocs.plugins import BasePlugin


class LastModifyAt(BasePlugin):

    def on_page_markdown(self, content, page, config, **kwargs):
        abs_src_path = page.file.abs_src_path
        with os.popen(f"git log -n 1 --pretty=format:%cd '{abs_src_path}'") as f:
            last_write_at = f.read()
        revision_date = dateutil.parser.parse(last_write_at).isoformat() if last_write_at else ""
        if "revision_date" not in page.meta:
            page.meta["revision_date"] = revision_date

        return content
