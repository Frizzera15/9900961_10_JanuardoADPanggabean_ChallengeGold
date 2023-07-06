from flask import Flask, jsonify
from flasgger import Swagger, swag_from

app = Flask(__name__)
title = 'API Documentation for Data Processing dan Modelling'
version = '1.0.0'
description = 'Dokumentasi API untuk Data Processing dan Modelling'

swagger_template = {'info' : {'title': title,
                              'version' : version,
                              'description' : description
                              },
                    'host' : 'localhost'
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

@swag_from('docs/hello_world.yml', methods=['GET'])
@app.route('/', methods=['GET'])
def hello_world():
    json_response = {
        'status code': 200,
        'description': 'Hello World',
        'data': 'Menyapa Dunia Hari Ini'
    }

    response_data = jsonify(json_response)
    return response_data


@app.route('/test', methods=['GET'])
def halo_dunia():
    json_response = {
        'situation': 'Good',
        'analyzing': 'in progress',
        'results': 'pending'
    }

    response_data = jsonify(json_response)
    return response_data


if __name__ == "__main__":
    app.run()
