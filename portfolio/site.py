import os

from flask import Flask
from flask.ext.mako import MakoTemplates, render_template

from markdown2 import Markdown

app = Flask(__name__)
app.template_folder = "templates"
mako = MakoTemplates(app)
base_dir = os.path.split(__file__)[0] + '/'

markdownGen = Markdown()

@app.route('/<page>')
@app.route('/', defaults=dict(page="home"))
@app.route('/projects/', defaults=dict(page="projects"))
def index_page(page):
    """
    Render our index page
    """
    page = None
    with open(base_dir + "index.md", "r") as indexMD:
        page = indexMD.read()

    return markdownGen.convert(page)

@app.route('/projects/<name>')
def project_page(name = "test"):
    """
    Render a page for a specific project
    If that project doesn't exist
    serve a 404 page instead
    """

    name = name.lower().replace(' ','_')

    try:
        with open(base_dir + "projects/" + name + ".md") as projectMD:
            page = projectMD.read()
    except:
        page = "#404"

    return markdownGen.convert(page)
