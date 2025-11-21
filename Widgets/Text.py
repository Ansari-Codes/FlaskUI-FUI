from Widgets.Widget import FValueWidget, FWidget
from typing import List, Literal, Union
from markdown import markdown

class FLabel(FWidget):
    def __init__(self,
                content: List | str | None = None,
                tag:Literal["h1", "h2", "h3", "h4", "h5", "h6", "p"]="p", 
                *, 
                id_=None, clas: List[str] | None = None, prop: List[str] | None = None, 
                style: List[str] | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag=tag, content=content if isinstance(content, list) else [content])

class FCode(FWidget):
    def __init__(self,
                content: List | str | None = None,
                *, 
                id_=None, clas: List[str] | None = None, prop: List[str] | None = None, 
                style: List[str] | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='code', content=content if isinstance(content, list) else [content])

class FMarkdown(FWidget):
    def __init__(self, markdown_text: str = "", *, id_=None, clas: List[str]|None = None, 
                prop: List[str]|None = None, style: List[str]|None = None):
        self.markdown_text = markdown_text
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='div', content=[])
        self.prop.append(f'hx-post="/_fui_widget_reload"')
        self.prop.append(f'hx-vals=\'{{"id":"{self.id}"}}\'')
        self.prop.append('hx-target="this"')
        self.prop.append('hx-swap="outerHTML"')
        self._build_html()

    def setMarkdown(self, text: str):
        self.markdown_text = text
        self._build_html()
        self.reload()
        return self

    def _build_html(self):
        html_content = markdown(self.markdown_text)
        self.content = [html_content]
        return super()._build_html()

class FPre(FWidget):
    def __init__(self,
                content: List | str | None = None,
                *, 
                id_=None, clas: List[str] | None = None, prop: List[str] | None = None, 
                style: List[str] | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag="pre", content=content if isinstance(content, list) else [content])

class FBlockquote(FWidget):
    def __init__(self,
                content: List | str | None = None,
                *, 
                id_=None, clas: List[str] | None = None, prop: List[str] | None = None, 
                style: List[str] | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='blockquote', content=content if isinstance(content, list) else [content])
