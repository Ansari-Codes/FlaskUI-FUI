from Widgets.Widget import FValueWidget, FWidget
from typing import List, Literal, Union
from .Text import FLabel

class FLink(FWidget):
    def __init__(self, content: List | None = None, href: str|None = None, target: str = '_blank', 
                *, 
                id_=None, clas: List[str] | None = None, 
                prop: List[str] | None = None, 
                style: List[str] | None = None):
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='a', content=content)
        self.target = target
        self.href = href or '#'
        self.prop.append(f'target="{self.target}"')
        self.prop.append(f'href="{self.href}"')
        self._build_html()

class FNav(FWidget):
    def __init__(self, 
                brand_name: str|dict = "",
                links: List[FLink|dict]|None = None,
                *, 
                id_=None, clas: List[str] | None = None,
                prop: List[str] | None = None, 
                style: List[str] | None = None):
        links = links or []
        content = [
            brand_name 
            if isinstance(brand_name, FLabel) 
            else (
                FLabel(**brand_name) 
                if isinstance(brand_name, dict) 
                else 
                FLabel(content=[brand_name])
            )] + [(c if isinstance(c, FLink) else FLink(**c)) for c in links]
        super().__init__(id_=id_, clas=clas, prop=prop, style=style, tag='nav', content=content)
