from Widgets.Widget import FValueWidget, FWidget
from typing import List, Literal, Union

class FButton(FWidget):
    def __init__(self, 
                content: List[Union[FWidget, str]]|None = None, 
                onclick=lambda:(),
                *, id_=None, clas: List[str]|None = None, prop: List[str]|None = None, 
                style: List[str]|None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='button', content=content)
        self.prop.append(f'hx-post="/_fui_event"')
        self.prop.append(f'hx-vals=\'{{"id":"{self.id}"}}\'')
        self.prop.append('hx-target="this"')
        self.prop.append('hx-swap="outerHTML"')
        self.onclick = onclick
        self._build_html()

class FInput(FValueWidget):
    def __init__(self, value=None, onchange=lambda x:x, 
                *, id_=None, clas: List[str]|None = None, prop: List[str]|None = None, 
                style: List[str]|None = None, inp_type="text"):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='input', 
                        value=value, onchange=onchange)
        self.prop.append(f'type="{inp_type}"')
        self.prop.append('hx-trigger="input changed delay:500ms"')
        self._build_html()

class FOption(FWidget):
    def __init__(self, value = None, content: List | None = None, *, id_=None, clas: List[str] | None = None, prop: List[str] | None = None, 
                style: List[str] | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='option', content=content)
        self.value = value
        self.prop.append(f"value='{self.value}'")
        self._build_html()

class FSelect(FValueWidget):
    def __init__(self, 
                options: List[dict | str] | None = None, 
                value=None, 
                onchange=lambda x:x,
                *, id_=None, clas: List[str] | None = None, prop: List[str] | None = None, 
                style: List[str] | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='select',
                        value=value, onchange=onchange)
        self.options = options or []
        self.option_widgets = [FOption(**o) for o in self.options] if self.options else [] # type: ignore
        self.content = self.option_widgets
        self.prop.append('hx-trigger="change"')
        self._build_html()

    def setValue(self, value):
        self._setValue(value)
        for opt in self.option_widgets:
            opt.prop = [p for p in opt.prop if not p.startswith("selected")]
            if str(opt.value) == str(value): 
                opt.prop.append("selected")
        self.reload()
        return self

class FTextArea(FValueWidget):
    def __init__(self, value: str | None = None, onchange=lambda v: v, *, id_=None, clas: list[str] | None = None, prop: list[str] | None = None,
                style: list[str] | None = None, content: list | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='textarea', 
                        content=content, value=value, onchange=onchange)
        self.prop.append('hx-trigger="input delay:500ms"')
        self._update_content()

    def _update_content(self):
        self.content = [self.value]
        self._build_html()

    def setValue(self, value: str):
        self.value = value
        self._update_content()
        self.reload()
        return self
