import os

from flask import Flask
from flask.ext.mako import MakoTemplates, render_template

from markdown2 import Markdown

app = Flask(__name__)
app.template_folder = "content/templates"
mako = MakoTemplates(app)
base_dir = os.path.split(__file__)[0] + '/content/'

markdownGen = Markdown(extras=['tables', 'core-friendly',
                               'fenced-code-blocks', 'metadata'])

@app.route('/<page>')
@app.route('/', defaults=dict(page="home"))
@app.route('/tutorials/', defaults=dict(page="tutorials"))
def index_page(page):
    """
    Render our index page
    """
    body = None
    with open(base_dir + "index.md", "r") as indexMD:
        body = indexMD.read()

    
    # Append tutorials in markdown

    for tutorial in tutorial_list():
        if 'tutorials' not in page:
	    tutorialURL = 'tutorials/' + tutorial
	else:
	    tutorialURL = tutorial
        body += '* [' + tutorial.replace('_', ' ') + '](' + tutorialURL + ')\n\n'

    return render_template('master.mak', body=markdownGen.convert(body), name="mako")

@app.route('/tutorials/<name>')
def tutorial_page(name = "test"):
    """
    Render a page for a specific tutorial
    If that tutorial doesn't exist
    serve a 404 page instead
    """

    name = name.lower().replace(' ','_')

    try:
        with open(base_dir + "tutorials/" + name + ".md") as tutorialMD:
            page = tutorialMD.read()
    except:
        page = "#404"

    return render_template('master.mak', body=markdownGen.convert(page), name="mako")

def tutorial_list():
    """
    Returns a list of tutorial names as strings
    """
    tutorial_list = []

    for dirpath, dirnames, files in os.walk(base_dir + "tutorials/"):
        for fname in files:
	    if fname.endswith('.md'):
	        tutorial_list.append(os.path.splitext(fname)[0])

    return tutorial_list
