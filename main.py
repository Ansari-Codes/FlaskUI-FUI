from app import App, FPage
from Widgets import (
    FButton, FInput, FSelect, FTextArea,
    FVideo, FAudio, FImage, FCanvas, FIFrame, FIcon,
    FRow, FCol, FGrid, FCard, FHeader, FFooter, FNav, FSpacer, FDivider,
    FLabel, FCode, FMarkdown, FPre, FBlockquote, FLink,
)

app = App()

pg = FPage(title="FUI Widget Showcase")

# Header / Nav
hdr = FHeader(content=[FLabel(tag='h2', content=["Flask UI — Widget Showcase"])])
pg.add(hdr)

nav = FNav(brand_name="FUI", links=[{"content":["Docs"], "href":"#"}, {"content":["Repo"], "href":"#"}])
pg.add(nav)

# Layout: two columns
left = FCol(content=[])
right = FCol(content=[])

# Left: form widgets and interactivity
inp = FInput(value="Type here")
left.add(FCard(content=[FLabel(content=["Text Input"]), inp]))

sel = FSelect(options=[{"value":"1", "content":["One"]}, {"value":"2", "content":["Two"]}], value="1")
left.add(FCard(content=[FLabel(content=["Select"]), sel]))

ta = FTextArea(value="Some longer text")
left.add(FCard(content=[FLabel(content=["TextArea"]), ta]))

def server_update():
    # Example server-side change: set input and mark it for reload
    inp.setValue("Updated on server click")
    inp.reload()

btn = FButton(content=["Update Input (server-side)"], onclick=server_update)
left.add(FCard(content=[btn]))

# Right: media and text widgets
img = FImage(src="https://via.placeholder.com/150")
right.add(FCard(content=[FLabel(content=["Image"]), img]))

vid = FVideo(src="", controls=False)
right.add(FCard(content=[FLabel(content=["Video (placeholder)"]), vid]))

iframe = FIFrame(src="https://example.com", width="100%", height="200")
right.add(FCard(content=[FLabel(content=["IFrame"]), iframe]))

code = FCode(text="print('Hello from FCode')")
md = FMarkdown(text="# Markdown title\nSome *markdown* here")
right.add(FCard(content=[FLabel(content=["Code"]), code, FDivider(), md]))

# Put columns in a row and add to page
row = FRow(content=[left, right])
pg.add(row)

# Footer
pg.add(FFooter(content=[FLabel(content=["Footer — FUI Showcase"]) ]))

app.fuiAddPage(pg)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
