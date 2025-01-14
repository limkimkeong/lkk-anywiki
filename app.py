from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)
PAGES_DIR = 'pages'
UPLOAD_FOLDER = 'uploads'
TAGS_FILE = 'tags.json'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'wav', 'ogg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load tags from file
if os.path.exists(TAGS_FILE):
    with open(TAGS_FILE, 'r') as file:
        tags_data = json.load(file)
else:
    tags_data = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    pages = os.listdir(PAGES_DIR)
    pages = [page.replace('.md', '') for page in pages]
    return render_template('index.html', pages=pages, tags_data=tags_data)

@app.route('/<page>')
def view_page(page):
    page_path = os.path.join(PAGES_DIR, f'{page}.md')
    if os.path.exists(page_path):
        with open(page_path, 'r') as file:
            content = file.read()
        page_tags = tags_data.get(page, [])
        return render_template('page.html', page=page, content=content, tags=page_tags)
    else:
        return render_template('edit.html', page=page, content='', tags=[])

@app.route('/edit/<page>', methods=['GET', 'POST'])
def edit_page(page):
    page_path = os.path.join(PAGES_DIR, f'{page}.md')
    if request.method == 'POST':
        content = request.form['content']
        tags = request.form['tags'].split(',')

        with open(page_path, 'w') as file:
            file.write(content)

        tags_data[page] = [tag.strip() for tag in tags if tag.strip()]
        with open(TAGS_FILE, 'w') as file:
            json.dump(tags_data, file)

        return redirect(url_for('view_page', page=page))
    else:
        if os.path.exists(page_path):
            with open(page_path, 'r') as file:
                content = file.read()
        else:
            content = ''
        page_tags = tags_data.get(page, [])
        return render_template('edit.html', page=page, content=content, tags=page_tags)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/tags/<tag>')
def view_tag(tag):
    matching_pages = [page for page, page_tags in tags_data.items() if tag in page_tags]
    return render_template('tag.html', tag=tag, pages=matching_pages)

if __name__ == '__main__':
    if not os.path.exists(PAGES_DIR):
        os.makedirs(PAGES_DIR)
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)