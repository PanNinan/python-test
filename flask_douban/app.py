import datetime
import sqlite3

import jieba
import numpy as np
from PIL import Image
from flask import Flask, render_template

# from matplotlib import pyplot as plt
# from wordcloud import WordCloud


app = Flask(__name__)


@app.route('/')
def index():
    time = datetime.date.today()
    return render_template("index.html", time=time)


@app.route('/movie')
def movie():
    data_list = []
    conn = sqlite3.connect("movie_250")
    cur = conn.cursor()
    sql = "select * from movie_250"
    data = cur.execute(sql)
    for item in data:
        data_list.append(item)
    cur.close()
    conn.close()
    return render_template("movie.html", data_list=data_list)


@app.route('/score')
def score():
    score = []
    num = []
    conn = sqlite3.connect("movie_250")
    cur = conn.cursor()
    sql = "select score,count(score) from movie_250 group by score"
    data = cur.execute(sql)
    for item in data:
        score.append(str(item[0]))
        num.append(str(item[1]))
    cur.close()
    conn.close()
    return render_template("score.html", score=score, num=num)


@app.route('/word', methods=['POST', 'GET'])
def word():
    conn = sqlite3.connect("movie_250")
    cur = conn.cursor()
    sql = "select instroduction from movie_250"
    data = cur.execute(sql)
    text = ""
    for item in data:
        text += item[0]
    cur.close()
    conn.close()
    cut = jieba.cut(text)
    string = ' '.join(cut)
    img = Image.open(r'./static/images/back.jpg')
    img_array = np.array(img)
    # wc = WordCloud(
    #     background_color='white',
    #     mask=img_array,
    #     font_path="微软雅黑.ttf"
    # )
    # wc.generate_from_text(string)
    return render_template("word.html", string=string)


@app.route('/team')
def team():
    return render_template("team.html")


if __name__ == '__main__':
    app.run()
