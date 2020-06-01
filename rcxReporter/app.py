from flask import Flask, make_response, request, render_template
from werkzeug.utils import secure_filename
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time



app = Flask(__name__, static_url_path='/home/rcxreporter/rcxreporter/static/')



@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/transform', methods=["POST"])
def transform_view():
    global num

    f = request.files['data_file']
    filename = secure_filename(f.filename)
    f.save(filename)

    df = pd.read_csv(filename, index_col='Date', parse_dates=True)

    OAT = pd.Series(df['OAT'])
    RAT = pd.Series(df['RAT'])
    MAT = pd.Series(df['MAT'])

    df_OATrat = (OAT - RAT)
    df_MATrat = (MAT - RAT)

    plt.scatter(df_OATrat,df_MATrat, color='grey', marker='+')
    plt.xlabel('OAT-RAT')
    plt.ylabel('MAT-RAT')
    plt.title('Economizer Diagnostics')
    plt.plot([0,-18],[0,-18], color='green', label='100% OSA during ideal conditions')
    plt.plot([0,20],[0,5], color='red', label='Minimum OSA in cooling mode')
    plt.plot([0,-38],[0,-9.5], color='blue', label='Minimum OSA in heating mode')
    plt.plot([0,0],[-20,10], color='black')
    plt.plot([-30,20],[0,0], color='black')
    #plt.legend()
    plt.text(-3, -28, time.ctime(), fontsize=9)


    plt.savefig('/home/rcxreporter/rcxreporter/static/plot.png')

    #plot = home/rcxreporter/rcxreporter/static/plot.png

    resp = add_header(make_response(render_template('table.html', tables=[df.to_html(classes='data')], titles=df.columns.values)))

    return resp



if __name__ == '__main__':
    app.run(debug=True)
