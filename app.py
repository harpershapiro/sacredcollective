import os
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/artist/sacredhumanbeings')
def artistPage():
    examplePortfolio = { "a":"1.JPG", "b":"2.jpg", "c":"3.jpg"}
    return render_template("artistPage.html",artist="Sacred Human Beings", portfolio=examplePortfolio)

#this method forces proper front-end updates
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == "__main__":
    app.run(debug=True)
