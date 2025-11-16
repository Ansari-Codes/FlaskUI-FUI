from app import App, FPage
from Widgets import FButton, FInput, FSelect, FTextArea
from Widgets import FVideo, FAudio, FImage, FCanvas, FIFrame, FIcon
from Widgets import FRow, FCol, FGrid, FCard, FHeader, FFooter, FNav, FSpacer, FDivider
from Widgets import FLabel, FCode, FMarkdown, FPre, FBlockquote, FLink

# Create App
app = App()

# Create a new page
pg = FPage(title="FUI Widget Showcase")

# --- Layouts ---
header = FHeader(content=[FLabel(content=["Header"])])
footer = FFooter(content=[FLabel(content=["Footer"])])
nav = FNav(links=[
    {"content": ["Home"], "href": "#"},
    {"content": ["About"], "href": "#"}
])
pg.add(header)
pg.add(nav)
pg.add(FSpacer(height=10))

# --- Buttons ---
btn = FButton(content=["Click Me"], onclick=lambda: print("Button clicked!"))
pg.add(btn)

# --- Inputs ---
txt_input = FInput(onchange=lambda v: print("Input changed:", v))
pg.add(txt_input)

txt_area = FTextArea(onchange=lambda v: print("Textarea changed:", v))
pg.add(txt_area)

# --- Select ---
select = FSelect(options=[
    {"value": "Option1", "content": ["Option 1"]},
    {"value": "Option2", "content": ["Option 2"]},
    {"value": "Option3", "content": ["Option 3"]}
], onchange=lambda v: print("Selected:", v))
pg.add(select)

# --- Text Widgets ---
pg.add(FLabel(content=["This is a label"]))
pg.add(FCode(text="print('Hello World')"))
pg.add(FMarkdown(text="**Bold Markdown Text**"))
pg.add(FPre(content=["Preformatted text"]))
pg.add(FBlockquote(content=["This is a blockquote"]))

# --- Media Widgets ---
pg.add(FVideo(src="sample.mp4", controls=True))
pg.add(FAudio(src="sample.mp3", controls=True))
pg.add(FImage(src="sample.png"))
pg.add(FCanvas(width=200, height=100))
pg.add(FIFrame(src="https://example.com", width="300", height="150"))

# --- Icons ---
pg.add(FIcon(icon="home", provider="mi"))
pg.add(FIcon(icon="star", provider="fa4"))
pg.add(FIcon(icon="user", provider="b3"))

# --- Layout Widgets ---
row = FRow(content=[
    FCol(content=[FLabel(content=["Column 1"])]),
    FCol(content=[FLabel(content=["Column 2"])])
])
pg.add(row)

grid = FGrid(content=[
    FCard(content=[FLabel(content=["Card 1"])]),
    FCard(content=[FLabel(content=["Card 2"])])
])
pg.add(grid)

pg.add(FDivider(orientation="horizontal"))
pg.add(FSpacer(height=20))
pg.add(footer)

# Add page to app
app.fuiAddPage(pg)

# Run app
app.run(port=8080, debug=True)
