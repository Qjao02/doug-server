import sys
import json
from subprocess import Popen, PIPE
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    params = request.args

    keywords = ['python','inverted_index.py']
    for key in params:
        keywords.append(key)

    # Abrindo um pipe para o módulo de captura dos parametros
    process = Popen(keywords, stdout=PIPE)
    (output, err) = process.communicate()
    process.wait()

    urls = output.decode('utf-8')

    return urls
