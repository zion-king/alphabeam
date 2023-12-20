from flask import Flask, jsonify, flash, request, redirect, render_template, url_for, Response, stream_with_context
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.debug = True

cors = CORS(app)

@app.route('/health', methods = ['GET'])
def health():
    return jsonify(
      application='AlphaBeam CBI API',
      version='1.0.0',
      message= "endpoint working"
    )