import os

from flask import Flask
from flask.ext.mako import MakoTemplates, render_template

from markdown2 import Markdown

app = Flask(__name__)
app.template_folder = "templates"
mako = MakoTemplates(app)
base_dir = os.path.split(__file__)[0] + '/'

markdownGen = Markdown()

static_pages = {}
@app.route('/')
def index_page():
    """
    Render our index page
    """
    with open(base_dir + "index.md", "r") as indexMD:
        static_pages["index"] = indexMD.read()

    return markdownGen.convert(static_pages["index"])
