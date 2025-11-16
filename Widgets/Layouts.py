from Widgets.Widget import FValueWidget, FWidget
from typing import List, Literal, Union

class FRow(FWidget):
    def __init__(self, *, id_=None, clas: List[str] | None = None, prop: List[str] | None = None, style: List[str] | None = None, 
                content: List | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='row', content=content)

class FCol(FWidget):
    def __init__(self, *, id_=None, clas: List[str] | None = None, prop: List[str] | None = None, style: List[str] | None = None, 
                content: List | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='col', content=content)

class FGrid(FWidget):
    def __init__(self, *, id_=None, clas: List[str] | None = None, prop: List[str] | None = None, style: List[str] | None = None, 
                content: List | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='grid', content=content)

class FCard(FWidget):
    def __init__(self, *, id_=None, clas: List[str] | None = None, prop: List[str] | None = None, style: List[str] | None = None, 
                content: List | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='card', content=content)

class FHeader(FWidget):
    def __init__(self, *, id_=None, clas=None, prop=None, style=None, content=None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='header', content=content)

class FFooter(FWidget):
    def __init__(self, *, id_=None, clas=None, prop=None, style=None, content=None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='footer', content=content)

class FNav(FWidget):
    def __init__(self, *, id_=None, clas=None, prop=None, style=None, content=None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='nav', content=content)

class FSpacer(FWidget):
    def __init__(self, *, id_=None, width=None, height=None):
        style = []
        if width: style.append(f'width:{width}px')
        if height: style.append(f'height:{height}px')
        super().__init__(id_=id_, style=style, tag='div')

class FDivider(FWidget):
    def __init__(self, *, id_=None, clas=None, prop=None, style=None, orientation: Literal['horizontal', 'vertical']='horizontal'):
        if style is None: style = []
        if orientation=='vertical': style.append('width:1px; height:100%;')
        else: style.append('width:100%; height:1px;')
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='div')
