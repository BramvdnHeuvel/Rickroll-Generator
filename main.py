from flask import Flask, render_template, redirect, url_for, send_from_directory, request
import src.database as db
import src.parser as parse
import sys

app = Flask(__name__)
DOMAIN_NAME = 'https://rr.noordstar.me' # Change this to where people can access your rickroll website.

@app.route('/')
def index():
    """
        Main homepage. Here, users are allowed to create their own rickroll links!
    """
    return render_template('index.html')

@app.route('/<string:link>')
def get_rickrolled(link):
    """
        Gain the page that shows the fake rich preview.
    """
    if link == 'favicon.ico':
        abort(404)
        
    shortcut = db.find_link(link)

    if shortcut is None:
        return redirect(url_for('index'))
    else:
        return render_template('roll.html', 
            title=shortcut[2], 
            description=shortcut[3], 
            image=shortcut[4],
            link=link,
            domain=DOMAIN_NAME
        )

@app.route('/source/<string:link>')
def notice_rickrolled_victim(link):
    """
        Get redirected to the Rickroll - but add the score real quick.
    """
    # GET RICKROLLED
    db.visit_link(link)

    return redirect("https://youtu.be/dQw4w9WgXcQ")

@app.route('/data/<string:link>')
def view_rickroll_success(link):
    """
        Get a page that shows how many people fell for your rickroll.
    """
    shortcut = db.find_link(link)

    if shortcut is None:
        return redirect(url_for('index'))
    else:
        return render_template('success.html', 
            amount=shortcut[1],
            link=link,
            domain=DOMAIN_NAME
        )

@app.route('/create', methods=['POST'])
def create_roll():
    """
        This page is visited when a user has submitted their information.
    """
    try:
        info = parse.new_link()
    except Exception:
        return redirect(url_for('index'))
    else:
        code = db.add_link(**info)
        title = parse.title(info['title'], code)

        return render_template('new-rolls.html', code=code, title=title, domain=DOMAIN_NAME)

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, request.path[1:])

if __name__ == '__main__':
    if len(sys.argv) == 1:
        app.run(debug=True)
    elif len(sys.argv) == 2:
        app.run(port=sys.argv[1])
    else:
        app.run(host=sys.argv[1], port=sys.argv[2])