from Widgets.Widget import FValueWidget, FWidget
from typing import List, Literal, Union

class FRow(FWidget):
    def __init__(self, content: List | None = None, *, id_=None, clas: List[str] | None = None, prop: List[str] | None = None, style: List[str] | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='row', content=content)

class FCol(FWidget):
    def __init__(self, content: List | None = None, *, id_=None, clas: List[str] | None = None, prop: List[str] | None = None, style: List[str] | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='col', content=content)

class FGrid(FWidget):
    def __init__(self, content: List | None = None, *, id_=None, clas: List[str] | None = None, prop: List[str] | None = None, style: List[str] | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='grid', content=content)

class FCard(FWidget):
    def __init__(self, content: List | None = None, *, id_=None, clas: List[str] | None = None, prop: List[str] | None = None, style: List[str] | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='card', content=content)

class FHeader(FWidget):
    def __init__(self, content: List | None = None, *, id_=None, clas: List[str] | None = None, prop: List[str] | None = None, style: List[str] | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='header', content=content)

class FFooter(FWidget):
    def __init__(self, content: List | None = None, *, id_=None, clas: List[str] | None = None, prop: List[str] | None = None, style: List[str] | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='footer', content=content)

class FSpacer(FWidget):
    def __init__(self, width=None, height=None, *, id_=None):
        style = []
        if width: style.append(f'width:{width}px')
        if height: style.append(f'height:{height}px')
        super().__init__(id_=id_, style=style, tag='div')

class FDivider(FWidget):
    def __init__(self, orientation: Literal['h', 'v']='h', width: str = '1px', *, id_=None, clas=None, prop=None, style=None):
        if style is None: style = []
        if orientation=='v': style.append(f'width:{width}; height:100%;')
        else: style.append(f'width:100%; height:{width};')
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='div')
