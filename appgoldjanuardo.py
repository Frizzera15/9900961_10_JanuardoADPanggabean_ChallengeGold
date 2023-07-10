import re
import pandas as pd
import sqlite3

from flask import Flask, jsonify, request, render_template, redirect, url_for
from BinarGoldChallengeWorkJanuardo import processing_text, processing_word
from data_reading_and_writing import create_table, insert_to_table, read_table

from flasgger import Swagger
from flasgger import swag_from

app = Flask(__name__, template_folder='Templates')
title = 'API Documentation for Data Processing dan Modelling'
version = '1.0.0'
description = 'Dokumentasi API untuk Data Processing dan Modelling'

swagger_template = {'info': {'title': title,
                             'version': version,
                             'description': description
                             },
                    'host': 'localhost'
                    }

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "docs",
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)


@app.route('/', methods=['GET', "POST"])
def hello_world():
    if request.method == 'POST':
        go_to_page = request.form['inputText']
        if go_to_page == "1":
            return redirect(url_for("input_text_processing"))
        elif go_to_page == "2":
            return redirect(url_for("input_file_processing"))
        elif go_to_page == "3":
            return redirect(url_for("read_database"))
    else:
        return render_template("indexcontoh.html")


@app.route('/text-processing', methods=['GET', 'POST'])
def input_text_processing():
    if request.method == 'POST':
        previous_text = request.form['inputText']
        cleaned_text = processing_text(previous_text)
        fixed_text = processing_word(cleaned_text)
        json_response = {'previous_text': previous_text,
                         'cleaned_text': fixed_text
                         }
        json_response = jsonify(json_response)
        return json_response
    else:
        return render_template("input_processing.html")


@app.route('/file-processing', methods=['GET', 'POST'])
def input_file_processing():
    if request.method == 'POST':
        input_file = request.files['inputFile']
        df = pd.read_csv(input_file, encoding='latin1')
        if ("Tweet" in df.columns):
            list_of_tweets = df['Tweet']  # yang dari CSV
            list_of_cleaned_tweet = df['Tweet'].apply(lambda x: processing_text(x))  # ini yang hasil cleaning-an
            list_of_fixed_tweet = list_of_cleaned_tweet.apply(lambda x: processing_word(x))

            create_table(table_name='tweet_cleansing_ardo')
            for previous_text, cleaned_text in zip(list_of_tweets, list_of_fixed_tweet):  # disini di-looping barengan
                insert_to_table(value_1=previous_text, value_2=cleaned_text)

            json_response = {'list_of_tweets': list_of_tweets[0],
                             'list_of_fixed_tweet': list_of_fixed_tweet[0]
                             }
            json_response = jsonify(json_response)
            return json_response
        else:
            json_response = {'ERROR_WARNING': "NO COLUMNS 'Tweet' APPEAR ON THE UPLOADED FILE"}
            json_response = jsonify(json_response)
            return json_response
        return json_response
    else:
        return render_template("file_processing.html")


@app.route('/read-database', methods=['GET', 'POST'])
def read_database():
    if request.method == "POST":
        showed_index = request.form['inputIndex']
        showed_keywords = request.form['inputKeywords']
        if len(showed_index) > 0:
            print("AAAAAAAAAA")
            result_from_reading_index = read_table(target_index=showed_index)
            previous_text = result_from_reading_index[1].decode('latin1')
            cleaned_text = result_from_reading_index[2].decode('latin1')
            json_response = {'Index': showed_index,
                             'Previous_text': previous_text,
                             'Cleaned_text': cleaned_text
                             }
            json_response = jsonify(json_response)
            return json_response
        elif len(showed_keywords) > 0:
            print("BBBBBBBBB")
            result_from_reading_keyword = read_table(target_keywords=showed_keywords)
            json_response = {'showed_keywords': showed_keywords,
                             'previous_text': result_from_reading_keyword[0][1].decode('latin1'),
                             'cleaned_text': result_from_reading_keyword[0][2].decode('latin1')
                             }
            json_response = jsonify(json_response)
            return json_response
        else:
            print("CCCCCCCC")
            json_response = {'ERROR_WARNING': "INDEX OR KEYWORDS IS NONE"}
            json_response = jsonify(json_response)
            return json_response
    else:
        return render_template("read_database.html")


if __name__ == '__main__':
    app.run(debug=True)
