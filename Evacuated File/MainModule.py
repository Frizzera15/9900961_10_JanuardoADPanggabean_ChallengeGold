@swag_from("docs/text_process.yml", methods=['GET','POST'])
@app.route('/text_process', methods=['GET', 'POST'])
def process():
    input_text = request.form['text']  # Get the input text from the form

    # Process the input text using the processing_word function
    processed_text = processing_word(input_text)
    response = {
        'input_text': input_text,
        'processed_text': processed_text
    }

    return jsonify(response)

def insert_to_table(value_1, value_2):
    value_1 = value_1.encode('utf-8')
    value_2 = value_2.encode('utf-8')
    query = f"INSERT INTO tweet_cleaning (id, cleaned_new_tweet) VALUES (?, ?);"
    cursors = conn.execute(query, (value_1, value_2))
    conn.commit()