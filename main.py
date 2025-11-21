from flask import render_template_string
from app import App, FPage, Flask
from Widgets import (
    FButton, FInput, FSelect, FTextArea,
    FVideo, FAudio, FImage, FCanvas, FIFrame, FIcon,
    FRow, FCol, FGrid, FCard, FHeader, FFooter, FNav, FSpacer, FDivider,
    FLabel, FCode, FMarkdown, FPre, FBlockquote, FLink,
)
import globalVars
from Widgets import globalVars as gv
app = Flask(__name__)
tc = app.test_client()
m = App(app, tc)
globalVars.app = gv.app = app
globalVars.m = gv.m = m

page = FPage("/", "Markdown Renderer")
@app.route(page.route or '/')
def render():
    return render_template_string(page.toHtml())

with tc:
    globalVars.tc = gv.tc = tc

    # Header
    header = FHeader(
        [FLabel("Markdown Renderer", "h4", clas=["w-fit", "h-fit"])],
        clas=["flex", "flex-row", "justify-center"]
    )
    page << header # type: ignore
    row = FRow(clas=["w-full", "h-fit", "justify-between"])
    page << row # type: ignore

    source = FInput(
        "# Try this example!", 
        clas=["w-full", "h-fit", "justify-between"]
    )
    row << source # type: ignore

    previewer = FLabel(source.value)
    row << previewer # type: ignore

    # Define the function after previewer is created
    def renderMarkDown(src: str):
        print("Called")
        previewer.content = [src]
        print(previewer.toHtml())
        # Only reload if we're in a request context
        try:
            previewer.reload()
        except Exception as e:
            print("Warning: reload() called outside of request context. Skipping.")

    # Set the onchange handler after the function is defined
    source.onchange = renderMarkDown

app.run(port=8080, debug=True)
