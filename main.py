from app import App, FPage
from Widgets import FButton, FInput

app = App()

pg = FPage(title="FUI Reload Demo")

inp = FInput(value="Old value")
pg.add(inp)

def change():
    inp.setValue("New value from server")
    inp.reload()

btn = FButton(content=["Update input (server-side)"], onclick=change)
pg.add(btn)

app.fuiAddPage(pg)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
