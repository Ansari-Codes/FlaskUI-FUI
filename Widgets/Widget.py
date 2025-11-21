from typing import TYPE_CHECKING, Callable, List, Union, Optional
from uuid import uuid4
from flask import Flask, current_app, has_app_context
from Widgets.Exceptions import FUIError
from requests import post

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
        from Widgets.globalVars import m as m
        if m: m.fui_widgets[self.id] = self

    def add(self, widg, index=None):
        if index is not None:
            self.content.insert(index, widg)
        else:
            self.content.append(widg)
        self._build_html()
        self.reload()
        return self

    def remove(self, filter: Callable):
        self.content = [w for idx, w in enumerate(self.content) if not filter(idx, w)]
        self._build_html()
        self.reload()
        return self

    def toHtml(self):
        return self._build_html()

    def reload(self):
        """Mark this widget to be reloaded on the client.
        
        When in an application context, makes an HTTP call to reload the widget.
        Otherwise, just rebuilds the HTML.
        """
        self._build_html()
        from Widgets.globalVars import tc
        if not tc:
            print("No tc")
            return
        try:
            print("reloading..." + self.id)
            response = tc.post(
                '/_fui_widget_reload',
                json={'id': self.id},
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 204:
                return self
            if response.status_code != 200:
                raise FUIError(
                    f"Widget reload failed with status {response.status_code}",
                    response.get_data(as_text=True)
                )
            self.html = response.get_data(as_text=True)
            print("reloaded - " + self.id)
        except Exception as e:
            raise FUIError("Failed to reload widget", str(e))
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

    def __rshift__(self, other):
        return other.add(self)

    def __repr__(self):
        return self.toHtml()

class FPage(FWidget):
    def __init__(self, route: str = '/', title: str='', *, 
                 head: List[Union[FWidget, str]]|None = None, 
                 scripts: List[Union[FWidget, str]]|None = None, 
                 styles: List[Union[FWidget, str]]|None = None, 
                 body: List[Union[FWidget, str]]|None = None):
        self.route = route or '#'
        self.title = title
        self.head = head or []
        self.body = body or []
        self.scripts = scripts or []
        self.styles = styles or []
        self.content = self.body
        self.html = ''
        super().__init__(tag='html', content=body)
        self._build_html()
    
    def addScript(self, script: str|FWidget):
        self.scripts.append(script)
        self._build_html()
        self.reload()
        return self
    
    def addStyle(self, style: str|FWidget):
        self.styles.append(style)
        self._build_html()
        return self

    def _build_html(self):
        self._validate_content(self.head)
        self._validate_content(self.body)
        self.content = self.body
        head_html = ''.join(i.toHtml() if isinstance(i, FWidget) else str(i) for i in self.head)
        body_html = ''.join(i.toHtml() if isinstance(i, FWidget) else str(i) for i in self.body)
        script_html = ''.join(i.toHtml() if isinstance(i, FWidget) else str(i) for i in self.scripts)
        style_html = ''.join(i.toHtml() if isinstance(i, FWidget) else str(i) for i in self.styles)
        raw = f"""<html>
        <head>
        <title>{self.title}</title>
        {head_html}
        <script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.8/dist/htmx.min.js" integrity="sha384-/TgkGk7p307TH7EXJDuUlgG3Ce1UVolAOFopFekQkkXihi5u/6OCvVKyz1W+idaz" crossorigin="anonymous"></script>
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <script src="https://cdn.tailwindcss.com"></script>
        <!-- FUI reload helper: call `fuiReloadWidget(id)` to fetch updated HTML and replace the element -->
        <script>
        window.fuiReloadWidget = async function(id) {{
            try {{
                console.log('Reloading: ${{id}}')
                const res = await fetch('/_fui_widget_reload', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ id: id }})
                }});
                if (res.status === 204) return; // nothing to update
                if (!res.ok) {{
                    console.warn('FUI reload failed', res.status);
                    return;
                }}
                const html = await res.text();
                const el = document.getElementById(id);
                if (!el) return;
                // Replace the element's outerHTML with the new HTML
                el.outerHTML = html;
                // Process the new element with htmx to ensure htmx attributes work
                htmx.process(document.getElementById(id));
                // Remove any reload-script tags emitted for this id
                // try {{
                //     const scripts = document.querySelectorAll('script.reload-' + id);
                //     scripts.forEach(s => s.remove());
                // }} catch (e) {{ /* ignore DOM removal errors */ }}
            }} catch (err) {{
                console.error('FUI reload error', err);
            }}
        }};
        </script>
        </head>
        <body>
        <page id="{self.id}">
        {style_html}
        {script_html}
        {body_html}
        </page>
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
    def __init__(self, value=None, onchange=lambda:(), *, id_=None, clas: List[str]|None = None, 
                prop: List[str]|None = None, style: List[str]|None = None, tag='div', 
                content: List[Union[FWidget, str]]|None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag=tag, content=content)
        self.value = value or ''
        self.onchange = onchange
        # common htmx attributes
        self.prop.append('hx-post="/_fui_event"')
        self.prop.append(f'hx-vals="js:{{ id: \'{self.id}\', value: this.value }}"')
        self.prop.append('hx-target="this"')
        self.prop.append('hx-swap="outerHTML"')
        self.prop.append('hx-swap-oob="true"')
        # Set initial value without reloading
        self._setValue(self.value)
    
    def setValue(self, value):
        self._setValue(value)
        self.reload()
        return self

    def _setValue(self, value):
        self.value = value
        for i, p in enumerate(self.prop):
            if p.strip().startswith('value='):
                self.prop.pop(i)
                break
        self.prop.append(f'value="{self.value}"')
        self._build_html()
