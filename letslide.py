import os, os.path, tempfile
from flask import Flask, request, render_template, redirect, url_for, make_response, send_from_directory
from landslide.generator import Generator

app = Flask(__name__)
app.debug = True
app.secret_key = os.environ.get('LETSLIDE_SECRET_KEY')

STORAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

SAMPLE_SOURCE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample.md')

def render_presentation(filename):
    gen = Generator(filename, embed=True)
    return gen.render()

def store_presentation(source, filename=None):
    if filename is None:
        fd, filename = tempfile.mkstemp(prefix='', dir=STORAGE_PATH, suffix='.md')
        os.close(fd)

    slug, filename = sanitize_filename(filename)
    with open(filename, 'wb') as f:
        f.write(source)

    return slug

def sanitize_filename(filename):
    return os.path.basename(filename), os.path.join(STORAGE_PATH, os.path.basename(filename))

@app.route('/edit/', methods=['GET', 'POST',])
@app.route('/edit/<slug>', methods=['GET', 'POST',])
def edit(slug=None):
    if request.method == 'POST':
        captcha_field = request.form['name']
        if captcha_field != 'let-me-pass':
            return make_response('Bad request', 400)

        slug = store_presentation(request.form['source'], slug)

        return redirect(url_for('edit', slug=slug))

    source = u''
    slides_url = None
    if slug is not None:
        slug, filename = sanitize_filename(slug)
        with open(filename, 'rb') as f:
            source = f.read()

        slides_url = '%s%s' % (request.url_root[:-1], url_for('slides', slug=slug))

    return render_template('edit.html', source=source, slug=slug, slides_url=slides_url)

@app.route('/', methods=['GET',])
def index():
    with open(SAMPLE_SOURCE_FILE, 'rb') as f:
        source = f.read()

    return render_template('index.html', source=source)

@app.route('/slides/<slug>', methods=['GET', 'POST',])
def slides(slug):
    slug, filename = sanitize_filename(slug)
    resp = make_response(render_presentation(filename), 200)

    return resp

@app.route('/about', methods=['GET',])
def about():
    return render_template('about.html')

@app.route('/legal', methods=['GET',])
def legal():
    return render_template('legal.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run()
