from typing import Callable, List, Union
from uuid import uuid4
from Widgets.Exceptions import FUIError

class FWidget:
    def __init__(self, *, id_=None, clas: List[str]|None = None, prop: List[str]|None = None, 
                    style: List[str]|None = None, tag='div', content: Union[List, None] = None):
        self.id = id_ or ((tag or 'div') + uuid4().hex)
        self.clas = clas or []
        self.prop = prop or []
        self.style = style or []
        self.tag = tag or 'div'
        self.content = ([content] if not isinstance(content, list) else content) if content else []
        self.html = self._build_html()
        self._visible = True

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

    def setVisible(self, visible: bool):
        self._visible = visible
        if visible:
            self.style = [s for s in self.style if not s.startswith('display: none')]
        else:
            self.style.append('display: none')
        self._build_html()
        return self

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
        class_attr = ' '.join(self.clas) if self.clas else ''
        style_attr = '; '.join(self.style) if self.style else ''
        prop_attr = ' '.join(self.prop) if self.prop else ''
        attributes = []
        if class_attr: attributes.append(f'class="{class_attr}"')
        if style_attr: attributes.append(f'style="{style_attr}"')
        if prop_attr: attributes.append(prop_attr)
        attr_str = ' '.join(attributes) if attributes else ''
        html = f'<{self.tag} id="{self.id}" {attr_str}>'
        for w in self.content: html += w.toHtml() if isinstance(w, FWidget) else str(w)
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
    def __init__(self, route: str = '/', title: str='', *, 
                    head: List[Union[FWidget, str]]|None = None, 
                    script: List[Union[FWidget, str]]|None = None, 
                    body: List[Union[FWidget, str]]|None = None):
        self.route = route or '#'
        self.title = title
        self.head = head or []
        self.body = body or []
        self.scripts = script or []
        self.content = self.body
        self.html = ''
        self._build_html()
        super().__init__(tag='html', content=body)
    
    def addScript(self, script: Union[FWidget, str]):
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
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
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

class FValueWidget(FWidget):
    def __init__(self, *, id_=None, clas: List[str]|None = None, prop: List[str]|None = None, 
                    style: List[str]|None = None, tag='div', content: List[Union[FWidget, str]]|None = None, 
                    value=None, onchange=lambda:()):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag=tag, content=content)
        self.value = value or ''
        self.onchange = onchange
        self.prop.append('hx-post="/_fui_event"')
        self.prop.append('hx-trigger="change delay:150ms"')
        self.prop.append(f'hx-vals="js:{{ id: \'{self.id}\', value: this.value }}"')
        self.prop.append('hx-target="this"')
        self.prop.append('hx-swap="outerHTML"')

    def setValue(self, value):
        self.value = value
        for i, p in enumerate(self.prop):
            if p.strip().startswith('value='):
                self.prop.pop(i)
                break
        self.prop.append(f'value="{self.value}"')
        self._build_html()
