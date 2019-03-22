import pandas as pd
import numpy as np
from splinter import Browser
from flask import Flask,render_template,url_for, request
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')



@app.route('/result',methods = ['POST'])

def rec():
    if request.method == 'POST':
        searche = request.form['search']
        r_cols=['user_id','movie_id','rating']
        ratings=pd.read_csv('ml-100k/u.data',sep='\t',names=r_cols,usecols=range(3))
        m_cols=['movie_id','title']
        movies=pd.read_csv('ml-100k/u.item',sep='|',names=m_cols,usecols=range(2),encoding = "ISO-8859-1")
        final=pd.merge(ratings,movies)
        movierating=final.pivot_table(index=['user_id'],columns=['title'],values=['rating'])
        desired=movierating['rating'][searche]
        moviestats=final.groupby('title').agg({'rating':[np.size,np.mean]})
        pop_movies=moviestats['rating']['size']>=100
        moviestats[pop_movies].sort_values([('rating','mean')],ascending=False)[:15]
        similar=movierating.corrwith(desired)
        similar=similar.dropna()
        df=moviestats[pop_movies].join(pd.DataFrame(similar,columns=['similarity']))
        m=df.sort_values(['similarity'],ascending=False)[:6]
        arr=[]
        for i in range(1,6):
            k=m.index.values[i][1]
            arr.append(k)



        
    
    
    return render_template('result.html',res=arr)





