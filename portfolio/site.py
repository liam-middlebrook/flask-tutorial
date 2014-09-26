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
    body = None
    with open(base_dir + "index.md", "r") as indexMD:
        body = indexMD.read()

    body += "\n\n##Project List\n\n"
    
    for project in project_list():
        if 'projects' not in page:
	    projectURL = 'projects/' + project
	else:
	    projectURL = project
        body += '* [' + project.replace('_', ' ') + '](' + projectURL + ')\n\n'

    return render_template('master.mak', body=markdownGen.convert(body), name="mako")

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

    return render_template('master.mak', body=markdownGen.convert(page), name="mako")

def project_list():
    """
    Returns a list of project names as strings
    """
    project_list = []

    for dirpath, dirnames, files in os.walk(base_dir + "projects/"):
        for fname in files:
	    if fname.endswith('.md'):
	        project_list.append(fname.rstrip('.md'))

    return project_list
