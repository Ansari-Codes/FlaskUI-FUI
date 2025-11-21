from os import PathLike
from typing import Any, Literal
from Widgets.Widget import FPage
from Widgets import FButton, FValueWidget
from flask import Flask, render_template_string, request
from Widgets.utils import Logger
from colorama import Fore, Style, init
import globalVars
import Widgets.globalVars as W_globalVars

init(True)

class App:
    def __init__(self, app: Flask, tc, *, pages=None, prod=False):
        self.fui_pages = pages or []
        self.fui_widgets = {}
        self.fui_logger = Logger()
        self.prod = prod
        self.app:Flask = app
        for i in self.fui_pages: 
            self.fui_widgets.update(i.getAllWidgets())
            self.fui_logger("All widgets collected!")
        @self.app.route('/_fui_event', methods=['POST'])
        def handle_event():
            if self.prod: self.fui_logger("Event started!")
            if request.is_json: data = request.get_json()
            else: data = request.form.to_dict()
            if self.prod: self.fui_logger(f"Data received: {data}")
            wid_id = data.get('id')
            widget = self.fui_widgets.get(wid_id)
            if widget and isinstance(widget, FButton):
                widget.onclick()
                if self.prod: self.fui_logger(Style.BRIGHT + Fore.GREEN + "Widget clicked!" + Style.RESET_ALL)
                response = widget.toHtml()
                response += '<script>htmx.process(document.body)</script>'
                if self.prod: self.fui_logger("Event finished!", "success")
                return response
            elif widget and isinstance(widget, FValueWidget):
                wid_val = data.get('value')
                if self.prod: self.fui_logger(f"Widget value received: {Style.BRIGHT + Fore.GREEN}{wid_val}{Style.RESET_ALL}")
                widget.onchange(wid_val)
                if self.prod: self.fui_logger(f"Widget 'onchange' called")
                widget.setValue(wid_val)
                if self.prod: self.fui_logger(f"Widget value changed")
                response = widget.toHtml()
                response += '<script>htmx.process(document.body)</script>'
                if self.prod: self.fui_logger("Event finished!", "success")
                return response
            if (not widget) and self.prod: self.fui_logger(f"Widget not found", "warning")
            else: self.fui_logger(f"Widget is not an instance of these types: FButton, FValueWidget", "warning")
            if self.prod: self.fui_logger("Event finished without any purpose!", "success")
            return '', 204
        @self.app.route('/_fui_widget_reload', methods=['POST'])
        def handle_widget_reload():
            if self.prod: self.fui_logger("Widget reload request started")
            if request.is_json: data = request.get_json()
            else: data = request.form.to_dict()
            wid_id = data.get('id')
            if self.prod: self.fui_logger(f"Reloading widget '{wid_id}'...")
            if not wid_id:
                if self.prod: self.fui_logger("No widget id provided for reload", "warning")
                return '', 400
            widget = self.fui_widgets.get(wid_id)
            if not widget:
                self.fui_logger(f"Widget '{wid_id}' not found!", "warning")
                return '', 204
            html = widget.toHtml()
            print("From /_fui_widget_reload: ", html)
            if self.prod: self.fui_logger(f"Widget '{wid_id}' reloaded!", "success")
            if html is None: return '', 204
            html += f"<script class='reload-{wid_id}'>window.fuiReloadWidget('{wid_id}');</script>"
            return html
        self.fui_logger("App initalized!", "success")

    def fuiAddPage(self, page: FPage):
        if page.route in [p.route for p in self.fui_pages]: 
            raise self.fui_logger(f"The page at route '{page.route}' already exists!", "warning")
        if self.prod: self.fui_logger(f"Adding page '{page.title}' to the app...")
        self.fui_widgets.update(page.getAllWidgets())
        @self.app.route(page.route)
        def render(): return render_template_string(page.toHtml())
        self.fui_pages.append(page)
        if self.prod: self.fui_logger(f"Page '{page.title}' added to the app!", "success")
        if self.prod: self.fui_logger(f"All pages: {', '.join([p.title for p in self.fui_pages])}", "success")
    
    def run(self, host: str | None = None, port: int | None = None, debug: bool | None = None, load_dotenv: bool = True, **options: Any) -> None:
        for i in self.fui_pages:  self.fui_widgets.update(i.getAllWidgets())
        return self.app.run(host, port, debug, load_dotenv, **options)