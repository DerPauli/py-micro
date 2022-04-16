from net.client import Client
from db.db import MongoDB
from dotenv import load_dotenv

from flask import Flask, redirect, request, render_template, url_for, flash

import json



baseUrl = 'https://api.twitter.com/2/'
app = Flask(__name__, template_folder='template')
app.config.from_file('config.json', load=json.load)
app.secret_key = "super secret key"

load_dotenv()

c = Client(baseUrl)
m = MongoDB()


@app.route("/")
def root():
    t = m.get_all_tweets()
    return render_template('home.html', tweets=t)

@app.route("/fetch", methods=['POST'])
def fetch():
    tuser = request.form.get('handle')
    if tuser != None and tuser != '':
        t = c.load_latest_tweets(tuser)
        if t != None:
            bson = m.attach_oids(t)

            m.print_bson(bson)
            m.insert_tweets(bson)
        else:
            flash("Username not found", 'danger')

    return redirect(url_for('root'))