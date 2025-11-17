from Widgets.Widget import FValueWidget, FWidget
from typing import List, Literal, Union

class FVideo(FWidget):
    def __init__(self, src="", controls=True, *, id_=None, clas: List[str] | None = None, prop: List[str] | None = None, style: List[str] | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='video')
        self.src = src
        self.controls = controls
        self.prop.append(f'src="{self.src}"')
        self.prop.append(f'{"controls"*self.controls}')

class FAudio(FWidget):
    def __init__(self, src="", controls=True, *, id_=None, clas: List[str] | None = None, prop: List[str] | None = None, style: List[str] | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='audio')
        self.src = src
        self.controls = controls
        self.prop.append(f'src="{self.src}"')
        self.prop.append(f'{"controls"*self.controls}')

class FImage(FWidget):
    def __init__(self, src="", *, id_=None, clas: List[str] | None = None, prop: List[str] | None = None, style: List[str] | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='img')
        self.src = src
        self.prop.append(f'src="{self.src}"')

class FCanvas(FWidget):
    def __init__(self, width=300, height=150, *, id_=None, clas=None, prop=None, style=None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='canvas')
        self.prop.append(f'width="{width}"')
        self.prop.append(f'height="{height}"')

class FIFrame(FWidget):
    def __init__(self, src="", width="100%", height="300", *, id_=None, clas=None, prop=None, style=None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='iframe')
        self.src = src
        self.prop.append(f'src="{self.src}"')
        self.prop.append(f'width="{width}"')
        self.prop.append(f'height="{height}"')

class FIcon(FWidget):
    def __init__(
        self,
        icon: str|None = None,
        provider: Literal["fa4", "mi", "b3"] = "mi",
        *,
        id_=None,
        clas: List[str] | None = None,
        prop: List[str] | None = None,
        style: List[str] | None = None,
    ):
        clas = clas or []
        if provider == 'fa4':
            clas.append(f"fa fa-{icon}")
        elif provider == 'b3':
            clas.append(f"glyphicon glyphicon-{icon}")
        elif provider == 'mi':
            clas.append(f"material-icons")
        content = [icon] if provider == 'mi' else []
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='i', content=content)
