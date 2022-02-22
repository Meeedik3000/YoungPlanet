# MAIN PAGES

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, request, make_response
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# DB Classes
class chanel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    pic = db.Column(db.String(100))
    about = db.Column(db.String(500))
    videos = db.relationship('video', backref = 'chanel')
    articles = db.relationship('article', backref = 'chanel')

class video(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    pic = db.Column(db.String(100))
    about = db.Column(db.String(500))
    src = db.Column(db.String(100))
    quest = date = db.Column(db.String(100))
    date = db.Column(db.String(20))
    chanel_id = db.Column(db.Integer, db.ForeignKey('chanel.id'))

class article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    pic = db.Column(db.String(100))
    text = db.Column(db.String(2000))
    quest = date = db.Column(db.String(100))
    date = db.Column(db.String(20))
    chanel_id = db.Column(db.Integer, db.ForeignKey('chanel.id'))


# Main page  +
@app.route('/', methods=['GET'])
def MainPage():
    vidName = video.query.all().name
    vidPic = video.query.all().pic
    vidId = video.query.all().id
    artName = article.query.all().name
    artPic = article.query.all().pic
    artId = article.query.all().id
    lastVid = video.query.filter_by(id = vidId[-1]).first()
    #lastArt = video.query.filter_by(id = artId[-1])
    return render_template('mainPage.html', photoes=vidPic, names=vidName, src=vidId, firstSrc=lastVid.id, firstPhotoes=lastVid.pic, firstName=lastVid.name, namesArt=artName, srcArt=artId, picArt=artPic)


# Videos page
@app.route('/videos', methods=['GET'])
def VideosPage():
    vidName = video.query.all().name
    vidPic = video.query.all().pic
    vidId = video.query.all().id
    return render_template('videos.html', photoes=vidPic, names=vidName, src=vidId)


# About page
@app.route('/about', methods=['GET'])
def AboutPage():
    return render_template('about.html')


# Chanels page
@app.route('/chanels', methods=['GET'])
def ChanelsPage():
    chnName = chanel.query.all().name
    chnPic = chanel.query.all().pic
    chnId = chanel.query.all().id
    return render_template('chanels.html', names=chnName, src=chnId, pic=chnPic)


# Watch video  +
@app.route('/videos/<VideoLink>', methods=['GET'])
def WatchVideo(VideoLink):
    vid = video.query.filter_by(id = VideoLink).first()
    chn = chanel.query.filte_by(id = vid.chanel_id).first()
    return render_template('watchVideo.html', src=vid.id, name=vid.name, type=chn.id, chanel=chn.name, chanelPic=chn.pic, quest=vid.quest, about=vid.about, date=vid.date)


# Watch article  +
@app.route('/articles/<ArticleLink>', methods=['GET'])
def WatchArticle(ArticleLink):
    art = video.query.filter_by(id = ArticleLink).first()
    chn = chanel.query.filte_by(id = art.chanel_id).first()
    return render_template('watchVideo.html', src=art.id, name=art.name, type=chn.id, chanel=chn.name, chanelPic=chn.pic, quest=art.quest, text=art.article, date=art.date)


# Open chanel  +
@app.route('/chanels/<ChaneLink>', methods=['GET'])
def WatchChanel(ChaneLink):
    chn = chanel.query.filter_by(id = ChaneLink).first()
    vidIds = chn.videos.id
    vidNames = chn.videos.name
    vidPic = chn.videos.pic
    return render_template('watchChanel.html', photoes=vidPic, names=vidNames, src=vidIds, name=chn.name, pic=chn.pic)


# Checking password before enter to the admin panel
@app.route('/admin', methods=['POST'])
def adminCheck():
    name = request.form['name']
    password = request.form['password']
    if name == 'admin' and password == 'admin':
        cok = make_response(redirect(url_for('videoApp.adminVideos')))
        cok.set_cookie('admin', 'True', max_age=60*60*24*1*1)
        return cok
    else: # if password or name invaled, redirecting user to the same page to try more
        return render_template('adminEnter.html', eror=True)


# Add video
@app.route('/admin/videos/add', methods=['POST', 'GET'])
def ad_video():
    if request.cookies.get('admin') == 'True':
        if request.method == 'GET':
            return render_template('addVideo.html')
        elif request.method == 'POST':

            name = request.form['name']
            pic = request.form['pic']
            about = request.form['about']
            src = request.form['src']
            quest = request.form['quest']
            date = request.form['date']
            chn = request.form['chanel']
            
            if name.replace(' ', '') != '' and src.replace(' ', '') != '' and pic.replace(' ', '') != '' and chn.replace(' ', '') != '':
                chanel_to_add = chanel.query.filter_by(name=chn).first()
                if chanel_to_add == None: chanel_to_add = chanel(name = chn, pic = '', about = '')
                db.session.add(video(name = name, pic = pic, about = about, src = src, quest = quest, date = date, chanel_id = chanel_to_add.id))
                db.session.commit()
                return redirect(url_for('videoApp.adminVideos'))
            else:
                return render_template('addVideo.html', eror=True, name=name, pic=pic, src=src, chanel=chn, quest=quest, about=about, date=date)
    else:
        return render_template('adminEnter.html')


# Edit video
@app.route('/admin/videos/<VideoLink>/edit', methods=['POST', 'GET'])
def edit_video(VideoLink):
    if request.cookies.get('admin') == 'True':
        if request.method == 'GET':
            vid = video.query.filter_by(name=VideoLink)
            return render_template('editVideo.html', name=vid.name, link=vid.id, src=vid.src, pic=vid.pic, chanel=vid.chanel, about=vid.about)
        elif request.method == 'POST':

            name = request.form['name']
            pic = request.form['pic']
            about = request.form['about']
            src = request.form['src']
            quest = request.form['quest']
            date = request.form['date']
            chn = request.form['chanel']
            
            if name.replace(' ', '') != '' and src.replace(' ', '') != '' and pic.replace(' ', '') != '' and chn.replace(' ', '') != '':
                chanel_to_add = chanel.query.filter_by(name=chn).first()
                if chanel_to_add == None: chanel_to_add = chanel(name = chn, pic = '', about = '')
                new_vid = video.query.filter_by(name=VideoLink).first()
                new_vid.name = name
                new_vid.pic = pic
                new_vid.about = about
                new_vid.src = src
                new_vid.quest = quest
                new_vid.date = date
                new_vid.chanel = chn
                db.session.add(new_vid)
                db.session.commit()
                return redirect(url_for('videoApp.adminVideos'))
            else:
                return render_template('addVideo.html', eror=True, name=name, pic=pic, src=src, chanel=chn, quest=quest, about=about, date=date)
    else:
        return render_template('adminEnter.html')


# Delete video
@app.route('/admin/videos/<VideoLink>/delete', methods=['GET'])
def delete_video(VideoLink):
    if request.cookies.get('admin') == 'True':
        vid = video.query.filter_by(name = VideoLink).first()
        db.session.delete(vid)
        db.session.commit()
        return redirect(url_for('adminVideos'))
    else:
        return render_template('adminEnter.html')


# Admin page
@app.route('/admin/videos', methods=['GET'])
def admin_video():
    if request.cookies.get('admin') == 'True':
        names = video.query.all().name
        src = video.query.all().id
        return render_template('adminPanel.html', names=names, src=src, open='videos', videos=True)
    else:
        return render_template('adminEnter.html')


# Edit chanel
@app.route('/admin/chanels/<ChanelLink>/edit', methods=['POST', 'GET'])
def edit_chanel_end(ChanelLink):
    if request.cookies.get('admin') == 'True':
        if request.method == 'GET':
            chn = chanel.query.filter_by(name = ChanelLink).first()
            return render_template('editChanel.html', name=chn.name, pic=chn.pic, link=chn.id, about=chn.about)
        elif request.method == 'POST':
            name = request.form['name']
            pic = request.form['pic']
            about = request.form['about']
            if name.replace(' ', '') != '':
                new_chanel = chanel.query.filter_by(name = ChanelLink).first()

                new_chanel.name = name
                new_chanel.pic = pic
                new_chanel.about = about

                return redirect(url_for('videoApp.adminVideos'))
            else:
                return render_template('editChanel.html', eror=True, name=name, pic=pic, link=ChanelLink, about=about)
    else:
        return render_template('adminEnter.html')


# admin page (chanels)
@app.route('/admin/chanels', methods=['GET'])
def adminChanels():
    if request.cookies.get('admin') == 'True':
        names = chanel.query.all().name
        src = chanel.qury.all().id
        return render_template('adminPanel.html', names=names, src=src, open='chanels')
    else:
        return render_template('adminEnter.html')


# Add article
@app.route('/admin/articles/add', methods=['POST', 'GET'])
def ad_article():
    if request.cookies.get('admin') == 'True':
        if request.method == 'GET':
            return render_template('addArticle.html')
        elif request.method == 'POST':
            
            name = request.form['name']
            pic = request.form['pic']
            art = request.form['article']
            chn = request.form['chanel']
            quest = request.form['quest']
            date = request.form['date']
            
            if name.replace(' ', '') != '' and art.replace(' ', '') != '' and pic.replace(' ', '') != '' and chn.replace(' ', '') != '':
                chanel_to_add = chanel.query.filter_by(name=chn).first()
                if chanel_to_add == None: chanel_to_add = chanel(name = chn, pic = '', about = '')
                db.session.add(article(name = name, pic = pic, article = art, quest = quest, date = date, chanel_id = chanel_to_add.id))
                db.session.commit()
                return redirect(url_for('videoApp.adminVideos'))
            else:
                return render_template('addArticle.html', eror=True, name=name, pic=pic, chn=chn, quest=quest, article=article, date=date)
    else:
        return render_template('adminEnter.html')


# Edit article
@app.route('/admin/articles/<ArticleLink>/edit', methods=['POST', 'GET'])
def edit_article(ArticleLink):
    if request.cookies.get('admin') == 'True':
        if request.method == 'GET':
            art = article.query.filter_by(name=ArticleLink)
            return render_template('editArticle.html', name=article.name, pic=article.pic, chanel=article.chanel, quest=article.quest, article=article.article, link=article.id)
        elif request.method == 'POST':

            name = request.form['name']
            pic = request.form['pic']
            chn = request.form['chanel']
            quest = request.form['quest']
            art = request.form['article']
            date = request.form['date']

            if name.replace(' ', '') != '' and art.replace(' ', '') != '' and pic.replace(' ', '') != '' and chn.replace(' ', '') != '':
                chanel_to_add = chanel.query.filter_by(name=chn).first()
                if chanel_to_add == None: chanel_to_add = chanel(name = chn, pic = '', about = '')
                new_art = article.query.filter_by(name=ArticleLink).first()
                new_art.name = name
                new_art.pic = pic
                new_art.article = art
                new_art.quest = quest
                new_art.date = date
                new_art.chanel = chn
                db.session.add(new_art)
                db.session.commit()
                return redirect(url_for('videoApp.adminVideos'))
            else:
                return render_template('editArticle.html', eror=True, name=name, pic=pic, chanel=chanel, quest=quest, article=article)
    else:
        return render_template('adminEnter.html')


# Delete article
@app.route('/admin/articles/<ArticleLink>/delete', methods=['GET'])
def delete_article(ArticleLink):
    if request.cookies.get('admin') == 'True':
        art = article.query.filter_by(name = ArticleLink).first()
        db.session.delete(art)
        db.session.commit()
        return redirect(url_for('adminVideos'))
    else:
        return render_template('adminEnter.html')


# Admin page
@app.route('/admin/articles', methods=['GET'])
def admin_article():
    if request.cookies.get('admin') == 'True':
        names = article.query.all().name
        src = article.query.all().id
        return render_template('adminPanel.html', names=names, src=src, open='videos', videos=True)
    else:
        return render_template('adminEnter.html')


if __name__ == "__main__":
    app.run(debug=True)