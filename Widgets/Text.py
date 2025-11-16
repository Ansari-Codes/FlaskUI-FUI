from Widgets.Widget import FValueWidget, FWidget
from typing import List, Literal, Union
from markdown import markdown

class FLabel(FWidget):
    def __init__(self, *, id_=None, clas: List[str] | None = None, prop: List[str] | None = None, style: List[str] | None = None, 
                tag:Literal["h1", "h2", "h3", "h4", "h5", "h6", "p"]="p", content: List | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag=tag, content=content)

class FCode(FWidget):
    def __init__(self, *, id_=None, clas: List[str] | None = None, prop: List[str] | None = None, style: List[str] | None = None, 
                text: str | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='code', content=[text or ""])

class FMarkdown(FWidget):
    def __init__(self, *, id_=None, clas: List[str] | None = None, prop: List[str] | None = None, style: List[str] | None = None, 
                text: str | None = None, **md):
        content = markdown(text or "", **md)
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='code', content=[content])

class FPre(FWidget):
    def __init__(self, *, id_=None, clas=None, prop=None, style=None, content=None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag="pre", content=content)

class FBlockquote(FWidget):
    def __init__(self, *, id_=None, clas=None, prop=None, style=None, content=None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag="blockquote", content=content)
