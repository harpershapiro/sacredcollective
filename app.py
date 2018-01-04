import os
from flask import Flask, request, render_template

id_Counter = 0

app = Flask(__name__)

class Post:
    def __init__(self, cont, content_link, b_txt):
        # bandcamp player or other content
        self.content    = cont
        # following text
        self.body_text  = b_txt
        self.content_url = content_link
        self.id = id_Counter
        global id_Counter 
        id_Counter += 1 

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/artist/sacredhumanbeings')
def shb_artistPage():
    # examplePortfolio = ["sosacred/1.JPG", "sosacred/2.jpg", "sosacred/3.jpg"]
    posts = []
    posts.append(Post( 
            "https://bandcamp.com/EmbeddedPlayer/album=3809564303/size=large/bgcol=ffffff/linkcol=0687f5/tracklist=false/transparent=true/",
            "http://sacredhumanbeings.bandcamp.com/album/holy-places",
            "some text about this project",

            ))
    return render_template("artistPage.html", artist="Sacred Human Beings", portfolio=posts)

@app.route('/artist/bennetbadactor')
def bba_artistPage():
    examplePortfolio = ["brocolli/1.JPG", "brocolli/2.jpg", "brocolli/3.jpg", "brocolli/4.jpg"]
    return render_template("artistPage.html",
        artist="Bennet Bad Actor", 
        portfolio=examplePortfolio)

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
