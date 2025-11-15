from app import FPage, App, FButton

app = App()

# FPage
pg = FPage()
label = FButton(content=["button"], onclick=lambda:print("This is clickable widget!"))
pg.add(label)

app.fuiAddPage(pg)
app.run(port=8080, debug=True)
