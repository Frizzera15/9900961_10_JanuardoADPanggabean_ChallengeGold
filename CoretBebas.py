from flask import Flask, jsonify
from FlaskModuleOut import create_json_response
import regex as re

from flask import request, json
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

app = Flask(__name__)
app.json_encoder = LazyJSONEncoder

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
    "specs": [{"endpoint": "docs", "route": '/docs.json'}],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app,
                  template=swagger_template,
                  config=swagger_config
                  )


@swag_from('docs/hello_world.yml', methods=['GET'])
@app.route('/', methods=['GET'])
def hello():
    json_response = create_json_response(description="Menyapa Hello World",
                                         data="Hello World")
    response_data = jsonify(json_response)
    return response_data


##############################################################################
@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():
    text = request.form.get('text')
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
    json_response = create_json_response(description="Teks yang sudah diproses",
                                         data=text)
    response_data = jsonify(json_response)
    return response_data


###############################################################################

@app.route('/text', methods=['GET'])
def text():
    json_response = create_json_response(description="Original Teks",
                                         data="Halo, apa kabar semua?")
    response_data = jsonify(json_response)
    return response_data


@app.route('/text-clean', methods=['GET'])
def text_clean():
    cleaned_text = re.sub(r'[^a-zA-Z0-9]', ' ', 'Halo, apa kabar semua?')
    json_response = create_json_response(description="Original Teks",
                                         data=cleaned_text)

    response_data = jsonify(json_response)
    return response_data


if __name__ == '__main__':
    app.run()(debug=True)
