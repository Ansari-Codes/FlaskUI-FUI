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

