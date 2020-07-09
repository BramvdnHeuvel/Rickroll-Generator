from flask import Flask, render_template, redirect, url_for
import src.database as db
import src.parser as parse
import sys

app = Flask(__name__)
DOMAIN_NAME = 'http:/rr.noordstar.me' # Change this to where people can access your rickroll website.

@app.route('/')
def index():
    """
        Main homepage. Here, users are allowed to create their own rickroll links!
    """
    return render_template('index.html')

@app.route('/<string:link>')
def get_rickrolled(link):
    shortcut = db.find_link(link)

    if shortcut is None:
        return redirect(url_for('index'))
    else:
        # GET RICKROLLED
        db.visit_link(link)

        return render_template('roll.html', 
            title=shortcut[2], 
            description=shortcut[3], 
            image=shortcut[4]
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

if __name__ == '__main__':
    if len(sys.argv) == 1:
        app.run(debug=True)
    elif len(sys.argv) == 2:
        app.run(port=sys.argv[1])
    else:
        app.run(host=sys.argv[1], port=sys.argv[2])