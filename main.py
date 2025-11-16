from app import FPage, App
from Widgets.Widget import FPage, FButton, FInput

app = App()
# FPage
pg = FPage()
label = FButton(content=["button"], onclick=lambda:print("This is clickable widget!"))
pg.add(label)
txt = FInput(
    onchange=lambda v: print("Text changed:", v)
)
pg.add(txt)

app.fuiAddPage(pg)
app.run(port=8080, debug=True)
