from os import PathLike
from typing import Literal
from Widgets.Widget import FPage
from Widgets import FButton, FValueWidget
from flask import Flask, render_template_string, request
from Widgets.utils import Logger

class App(Flask):
    """A wrapper around Flask's own app. All the FUI's methods and attributes start from 'fui'."""
    def __init__(self, import_name: str = '', *, prod = True, pages: list[FPage]|None = None,static_url_path: str | None = None, static_folder: str | PathLike[str] | None = "static", static_host: str | None = None, host_matching: bool = False, subdomain_matching: bool = False, template_folder: str | PathLike[str] | None = "templates", instance_path: str | None = None, instance_relative_config: bool = False, root_path: str | None = None):
        super().__init__(import_name or __name__, static_url_path, static_folder, static_host, host_matching, subdomain_matching, template_folder, instance_path, instance_relative_config, root_path)
        self.fui_pages = pages or []
        self.fui_widgets = {}
        self.fui_logger = Logger()
        self.prod = prod
        for i in self.fui_pages: 
            self.fui_widgets.update(i.getAllWidgets())
            self.fui_logger("All widgets collected!")
        @self.route('/_fui_event', methods=['POST'])
        def handle_event():
            if self.prod: self.fui_logger("Event started!")
            if request.is_json: data = request.get_json()
            else: data = request.form.to_dict()
            if self.prod: self.fui_logger(f"Data received: {data}")
            wid_id = data.get('id')
            widget = self.fui_widgets.get(wid_id)
            if widget and isinstance(widget, FButton):
                widget.onclick()
                if self.prod: self.fui_logger("Widget clicked!")
                if self.prod: self.fui_logger("Event finished!", "success")
                return widget.toHtml()
            elif widget and isinstance(widget, FValueWidget):
                wid_val = data.get('value')
                if self.prod: self.fui_logger(f"Widget value received: {wid_val}")
                widget.onchange(wid_val)
                if self.prod: self.fui_logger(f"Widget 'onchange' called")
                widget.setValue(wid_val)
                if self.prod: self.fui_logger(f"Widget value changed")
                if self.prod: self.fui_logger("Event finished!", "success")
                return widget.toHtml()
            if (not widget) and self.prod: self.fui_logger(f"Widget not found", "warning")
            else: self.fui_logger(f"Widget is not an instance of these types: FButton, FValueWidget", "warning")
            if self.prod: self.fui_logger("Event finished without any purpose!", "success")
            return '', 204
        self.fui_logger("App initalized!", "success")

    def fuiAddPage(self, page: FPage):
        if page.route in [p.route for p in self.fui_pages]: 
            raise self.fui_logger(f"The page at route '{page.route}' already exists!", "warning")
        if self.prod: self.fui_logger(f"Adding page '{page.title}' to the app...")
        self.fui_widgets.update(page.getAllWidgets())
        @self.route(page.route)
        def render(): return render_template_string(page.toHtml())
        self.fui_pages.append(page)
        if self.prod: self.fui_logger(f"Page '{page.title}' added to the app!", "success")
        if self.prod: self.fui_logger(f"All pages: {', '.join([p.title for p in self.fui_pages])}", "success")
