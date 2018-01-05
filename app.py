import os
from flask import Flask, request, render_template

id_Counter = 0

app = Flask(__name__)

class Post:
    def __init__(self, cont, b_txt):
        # bandcamp player or other content
        self._content    = cont
        # following text
        self._body_text  = b_txt
        # self.content_url = content_link
        self._id = id_Counter
        global id_Counter 
        id_Counter += 1

    # def render_content(self):
    #     return self.content

    def render_body_text(self):
        return self._body_text


class AlbumPost(Post):
    def __init__(self, iframe_str, bcmp_link_str, b_txt):
        self._iframe_str = iframe_str
        self._bcmp_link_str = bcmp_link_str
        self._body_text = b_txt
        self._content = ""
        self._id = id_Counter
        global id_Counter 
        id_Counter += 1

    def render_content(self):
        # 0: content
        # 1: id
        # 2: album url on bandcamp
        self._content = """<iframe style="border: 0; width: 600px; height: 600px;" 
            src={0} seamless onload="document.getElementById({1}).style.display = 'block'">
            <a href={2} >holy places by Sacred Human Beings</a>
            </iframe>""".format(self._iframe_str, self._id, self._bcmp_link_str)
        
        return self._content

class ArtPost(Post):
    def __init__(self, img_src, b_text):
        self._img_src = img_src
        self._body_text = b_text

    def render_content(self):
        self._content = "<img src=\"{0}\">".format(self._img_src)
        return self._content

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/artist/sacredhumanbeings')
def shb_artistPage():
    # examplePortfolio = ["sosacred/1.JPG", "sosacred/2.jpg", "sosacred/3.jpg"]
    posts = []    

    posts.append(AlbumPost( 
           "https://bandcamp.com/EmbeddedPlayer/album=3809564303/size=large/bgcol=ffffff/linkcol=0687f5/tracklist=false/transparent=true/",
           "http://sacredhumanbeings.bandcamp.com/album/holy-places",
           "Some text about this project. "
           ))

    posts.append(ArtPost("../static/images/sosacred/1.JPG", "img 001"))
    posts.append(ArtPost("../static/images/sosacred/2.JPG", "img 002"))
    posts.append(ArtPost("../static/images/sosacred/3.JPG", "img 003"))

    return render_template("artistPage.html", artist="Sacred Human Beings", portfolio=posts)

@app.route('/artist/bennetbadactor')
def bba_artistPage():
    examplePortfolio = ["brocolli/1.JPG", "brocolli/2.jpg", "brocolli/3.jpg", "brocolli/4.jpg"]
    posts = [ArtPost("../static/images/" + x, " img :) ") for x in examplePortfolio]
    return render_template("artistPage.html",
        artist="Bennet Bad Actor", 
        portfolio=posts)

@app.route('/artist/thickbrick')
def tb_artistPage():
    examplePortfolio = ["brocolli/1.JPG", "brocolli/2.jpg", "brocolli/3.jpg", "brocolli/4.jpg"]
    return render_template("artistPage.html",
        artist="Thick Brick", 
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
