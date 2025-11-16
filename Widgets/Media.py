from Widgets.Widget import FValueWidget, FWidget
from typing import List, Literal, Union

class FVideo(FWidget):
    def __init__(self, *, id_=None, clas: List[str] | None = None, prop: List[str] | None = None, style: List[str] | None = None, src="", controls=True):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='video')
        self.src = src
        self.controls = controls
        self.prop.append(f'src="{self.src}"')
        self.prop.append(f'{"controls"*self.controls}')

class FAudio(FWidget):
    def __init__(self, *, id_=None, clas: List[str] | None = None, prop: List[str] | None = None, style: List[str] | None = None, src="", controls=True):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='audio')
        self.src = src
        self.controls = controls
        self.prop.append(f'src="{self.src}"')
        self.prop.append(f'{"controls"*self.controls}')

class FImage(FWidget):
    def __init__(self, *, id_=None, clas: List[str] | None = None, prop: List[str] | None = None, style: List[str] | None = None, src=""):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='img')
        self.src = src
        self.prop.append(f'src="{self.src}"')

class FCanvas(FWidget):
    def __init__(self, *, id_=None, clas=None, prop=None, style=None, width=300, height=150):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='canvas')
        self.prop.append(f'width="{width}"')
        self.prop.append(f'height="{height}"')

class FIFrame(FWidget):
    def __init__(self, *, id_=None, clas=None, prop=None, style=None, src="", width="100%", height="300"):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='iframe')
        self.src = src
        self.prop.append(f'src="{self.src}"')
        self.prop.append(f'width="{width}"')
        self.prop.append(f'height="{height}"')
