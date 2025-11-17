from app import App, FPage
from Widgets import (
    FButton, FInput, FSelect, FTextArea,
    FVideo, FAudio, FImage, FCanvas, FIFrame, FIcon,
    FRow, FCol, FGrid, FCard, FHeader, FFooter, FNav, FSpacer, FDivider,
    FLabel, FCode, FMarkdown, FPre, FBlockquote, FLink,
)

app = App()

# Page
page = FPage("/", "Markdown Renderer")
page.addStyle("""
<style>
/* === Layout === */
.col {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.row {
    display: flex;
    flex-direction: row;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.grid {
    display: grid;
    gap: 1rem;
}

/* === Headers & Text === */
header, h1, h2, h3, h4, h5, h6, p, blockquote, code, pre {
    margin: 0.5rem 0;
    font-family: 'Segoe UI', Roboto, sans-serif;
}

h1 { font-size: 30px; font-weight: 700; }
h2 { font-size: 26px; font-weight: 600; }
h3 { font-size: 22px; font-weight: 600; }
h4 { font-size: 18px; font-weight: 500; }
h5 { font-size: 14px; font-weight: 500; }
h6 { font-size: 10px; font-weight: 500; }

p {
    font-size: 12px;
    line-height: 1.5;
}

pre, code {
    margin: 0;         /* remove default margins */
    padding: 0.25rem 0.5rem;
    font-family: 'Courier New', monospace;
    background-color: #f5f5f5;
    border-radius: 4px;
    overflow-x: auto;
}

/* === Card / Containers === */
.card {
    background-color: #fff;
    border-radius: 0.5rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    padding: 1rem;
    transition: all 0.2s ease;
}

.card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* === Buttons === */
button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 0.375rem;
    background-color: #3b82f6;
    color: #fff;
    cursor: pointer;
    font-weight: 500;
    transition: background-color 0.2s ease, transform 0.1s ease;
}

button:hover {
    background-color: #2563eb;
    transform: translateY(-1px);
}

button:active {
    transform: translateY(0);
}

/* === Inputs & Selects === */
input, select, textarea, option {
    font-size: 1rem;
    padding: 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    outline: none;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

input:focus, select:focus, textarea:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

/* === Media === */
video, audio, img, canvas, iframe {
    max-width: 100%;
    height: auto;
    border-radius: 0.375rem;
}

/* === Links & Icons === */
a {
    color: #3b82f6;
    text-decoration: none;
    transition: color 0.2s ease;
}

a:hover {
    color: #2563eb;
    text-decoration: underline;
}

i {
    font-style: normal; /* optional: use font icons instead */
}

/* === Navigation === */
nav {
    display: flex;
    gap: 1rem;
    padding: 0.5rem 1rem;
    background-color: #f3f4f6;
    border-radius: 0.375rem;
}

/* === Footer === */
footer {
    padding: 1rem;
    background-color: #f3f4f6;
    text-align: center;
    font-size: 0.875rem;
    color: #6b7280;
}

/* === Utility / Reset === */
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: 'Segoe UI', Roboto, sans-serif;
    background-color: #f9fafb;
    color: #111827;
}
</style>
""")

def renderMarkDown(src: str):
    previewer.content = [src]
    previewer.reload()

# Header
header = FHeader(
    [
    FLabel("Markdown Renderer", "h4", clas=["w-fit", "h-fit"]),
    ],
    clas=["flex", "flex-row", "justify-center"]
)
page << header #type:ignore

row = FRow(clas=["w-full", "h-fit", "justify-between"])
page << row #type:ignore

source = FInput(
    "# Try this example!", 
    onchange=renderMarkDown, 
    clas=["w-full", "h-fit", "justify-between"]
    )
row << source #type:ignore

previewer = FMarkdown(source.value)
row << previewer #type:ignore

app.fuiAddPage(page)

app.run(debug=False, port=8080)




