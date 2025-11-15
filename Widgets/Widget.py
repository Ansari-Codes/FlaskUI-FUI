from typing import Callable
from uuid import uuid4
from Widgets.Exceptions import FUIError

class FWidget:
    def __init__(self, *, id_=None, clas=None, prop=None, style=None, tag='div', content: list|None=None):
        self.id = id_ or ((tag or 'div') + uuid4().hex)
        self.clas = clas or ''
        self.prop = prop or ''
        self.style = style or ''
        self.tag = tag or 'div'
        self.content = ([content] if not isinstance(content, list) else content) if content else []
        self.html = self._build_html()

    def add(self, widg, index=None):
        if index is not None:
            self.content.insert(index, widg)
        else:
            self.content.append(widg)
        self._build_html()
        return self

    def remove(self, filter: Callable):
        self.content = [w for idx, w in enumerate(self.content) if not filter(idx, w)]
        self._build_html()
        return self

    def toHtml(self):
        return self._build_html()

    def _validate_content(self, content=None):
        content = content or self.content
        for i, w in enumerate(content):
            if not isinstance(w, (FWidget, str)):
                raise FUIError(
                    "Content must be FWidget or str",
                    f"Found {type(w).__name__} at index {i}"
                )
            if isinstance(w, FPage):
                raise FUIError("Cannot add Page inside another FWidget", f"Index {i}")

    def _build_html(self):
        self._validate_content()
        html = f'<{self.tag} id="{self.id}" class="{self.clas}" style="{self.style}" {self.prop}>'
        for w in self.content:
            html += w.toHtml() if isinstance(w, FWidget) else str(w)
        html += f'</{self.tag}>'
        self.html = html
        return html

    def __add__(self, other):
        if isinstance(other, (FWidget, str)):
            container = FWidget(tag='div')
            container.add(self)
            container.add(other)
            return container
        raise FUIError(f"Cannot add {type(other).__name__} to FWidget")

    def __lshift__(self, other):
        return self.add(other)

    def __repr__(self):
        return self.toHtml()

class FPage(FWidget):
    def __init__(self, route: str = '/', title: str='', *, head: list | None = None, script: list|None = None, body: list | None = None):
        self.route = route or '#'
        self.title = title
        self.head = ([head] if not isinstance(head, list) else head) if head is not None else []
        self.body = ([body] if not isinstance(body, list) else body) if body is not None else []
        self.scripts = ([script] if not isinstance(script, list) else script) if script is not None else []
        self.content = self.body
        self.html = ''
        self._build_html()
        super().__init__(tag='html', content=body)
    
    def addScript(self, script):
        self.scripts.append(script)
        self._build_html()
        return self

    def _build_html(self):
        self._validate_content(self.head)
        self._validate_content(self.body)
        self.content = self.body
        head_html = ''.join(i.toHtml() if isinstance(i, FWidget) else str(i) for i in self.head)
        body_html = ''.join(i.toHtml() if isinstance(i, FWidget) else str(i) for i in self.body)
        script_html = ''.join(i.toHtml() if isinstance(i, FWidget) else str(i) for i in self.scripts)
        raw = f"""<html>
        <head>
        <title>{self.title}</title>
        {head_html}
        <script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.8/dist/htmx.min.js" integrity="sha384-/TgkGk7p307TH7EXJDuUlgG3Ce1UVolAOFopFekQkkXihi5u/6OCvVKyz1W+idaz" crossorigin="anonymous"></script>
        {script_html}
        </head>
        <body>
        {body_html}
        </body>
        </html>"""
        self.html = raw
        return raw

    def getAllWidgets(self):
        all_widgets = {}
        def _collect(widget):
            if isinstance(widget, FWidget):
                all_widgets[widget.id] = widget
                for child in getattr(widget, 'content', []):
                    _collect(child)
        for section in [self.head, self.body, self.scripts]:
            for widget in section:
                _collect(widget)
        return all_widgets

class FButton(FWidget):
    def __init__(self, *, id_=None, clas=None, prop=None, style=None, content: list | None = None, onclick=lambda:()):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='button', content=content)
        self.prop += f' hx-post="/_fui_event" hx-vals=\'{{"id":"{self.id}"}}\' hx-target="this" hx-swap="outerHTML"'
        self.onclick = onclick