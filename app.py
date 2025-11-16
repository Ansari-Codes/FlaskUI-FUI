from os import PathLike, makedirs
from typing import Any
from Widgets.Widget import FPage, FWidget, FButton, FValueWidget
from flask import Flask, render_template_string, request
from bs4 import BeautifulSoup

class App(Flask):
    """A wrapper around Flask's own app. All the FUI's methods and attributes start from 'fui'."""
    def __init__(self, import_name: str = '', *, pages: list[FPage]|None = None,static_url_path: str | None = None, static_folder: str | PathLike[str] | None = "static", static_host: str | None = None, host_matching: bool = False, subdomain_matching: bool = False, template_folder: str | PathLike[str] | None = "templates", instance_path: str | None = None, instance_relative_config: bool = False, root_path: str | None = None):
        super().__init__(import_name or __name__, static_url_path, static_folder, static_host, host_matching, subdomain_matching, template_folder, instance_path, instance_relative_config, root_path)
        self.fui_pages = pages or []
        self.fui_widgets = {}
        for i in self.fui_pages: 
            self.fui_widgets.update(i.getAllWidgets())
        @self.route('/_fui_event', methods=['POST'])
        def handle_event():
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()
            wid_id = data.get('id')
            print(wid_id)
            widget = self.fui_widgets.get(wid_id)
            print(widget)
            if widget and isinstance(widget, FButton):
                widget.onclick()
                return widget.toHtml()
            elif widget and isinstance(widget, FValueWidget):
                wid_val = data.get('value')
                widget.onchange(wid_val)
                widget.setValue(wid_val)
                return widget.toHtml()
            return '', 204

    def fuiAddPage(self, page: FPage):
        if page.route in [p.route for p in self.fui_pages]: 
            raise Warning(f"The page at route '{page.route}' already exists!")
        self.fui_widgets.update(page.getAllWidgets())
        @self.route(page.route)
        def render(): return render_template_string(page.toHtml())
        self.fui_pages.append(page)
