from multiprocessing import Value
import random
import time
import sys

from flask import Flask, render_template, redirect, url_for, send_from_directory, request, abort, jsonify

import src.database as db
import src.parser as parse

app = Flask(__name__)
DOMAIN_NAME = 'https://youtu.be/' # Change this to where people can access your rickroll website.
ALLOW_ADS = False    # Only change this to True if you want ads on your website - so pretty much never.

counter = Value('i', db.count_rickrolls())
last_updated_count = Value('i', int(time.time()))

@app.route('/')
def index():
    """
        Main homepage. Here, users are allowed to create their own rickroll links!
    """
    return render_template('index.html', allow_ads=ALLOW_ADS)

@app.route('/total')
def total():
    """
        Get the total of how many people have been rickrolled
    """
    now = int(time.time())

    # Do a recount to get the actual (higher) value
    # Don't do it too often, though
    if abs(last_updated_count.value - now) > 10 and random.randint(1, 4) == 1:
        last_updated_count.value = now
        counter.value            = db.count_rickrolls()
    
    return jsonify({
        'total': counter.value
    })

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
    counter.value += 1
    amount = counter.value

    if amount % 25 == 0:
        print(f"Rickrolled {amount} people!")

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
        print("Created new rickroll: " + info['title'])
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
