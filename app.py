from net.client import Client
from db.db import MongoDB
from dotenv import load_dotenv
from dateutil import parser

from flask import Flask, redirect, request, render_template, url_for, flash

import os
import json



baseUrl = 'https://api.twitter.com/2/'
app = Flask(__name__, template_folder='template')
app.config.from_file('config.json', load=json.load)
app.secret_key = os.getenv('FLASK_SECRET')

ENTRIES_TO_FETCH=20
AUTO_HANDLE_LIST= [
    'elonmusk',
    'i_am_fabs',
    'cnnbrk',
    'billgates',
    'nasa',
    'twitter',
    'cnn',
    'nytimes'
]


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
        if tuser[0] == '@':
            tuser = tuser[1:]

        t = c.load_latest_tweets(tuser, ENTRIES_TO_FETCH)
        if t != None:
            bson = m.attach_oids(t)

            m.print_bson(bson)
            m.insert_tweets(bson)
        else:
            flash("Username not found", 'danger')

    return redirect(url_for('root'))

@app.route("/auto", methods=['GET'])
def auto():
    for user in AUTO_HANDLE_LIST:
        t = c.load_latest_tweets(user, ENTRIES_TO_FETCH)
        if t != None:
            bson = m.attach_oids(t)

            m.print_bson(bson)
            m.insert_tweets(bson)
        else:
            flash("Username not found", 'danger')

    return redirect(url_for('root'))



@app.template_filter('fmtdatetime')
def format_datetime(value, format="%d.%m.%Y - %H:%M:%S"):
    """Format a date time"""
    if value is None:
        return ""
    datetime = parser.parse(value)
    return datetime.strftime(format)