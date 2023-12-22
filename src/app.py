from flask import Flask, jsonify, flash, request, redirect, render_template, url_for, Response, stream_with_context
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from retriever.semantic_retriever import *


app = Flask(__name__)
app.debug = True

cors = CORS(app)
chat_history = init_chat_history()

@app.route('/health', methods = ['GET'])
def health():
    return jsonify(
      application='AlphaBeam CBI API',
      version='1.0.0',
      message= "endpoint working"
    )

@app.route('/embedding', methods=['GET', 'POST'])
def process():    
    if request.method == 'POST':
        project_name = request.form['projectName']
        index_name = project_name.replace(' ', '_').lower() + '_embeddings'
        data_dir = './semantics/models/semantic_models/'
        embedding = generate_vector_embedding_chroma(index_name, data_dir)

        response = {
            'statusCode': 200,
            'status': 'Vector embeddings created and stored successfully!',
        }
        return response
    return render_template('index.html')



@app.route("/retrieval", methods=["GET","POST"])
@cross_origin()
def completions():
    project = request.json
    project_name = project['projectName']
    index_name = project_name.replace(' ', '_').lower() + '_embeddings'

    if project['reset_chat'] in [True,'True']:
        chat_history = init_chat_history()

    # def query_semantic_layer():
    query = project['query']
    question_exists = answer_query_stream(query, index_name, chat_history, semantic_prompt_style())
    if question_exists == 'No':
        return "The source data doesn't contain the requested information. Please rephrase your question or ask me another question."

    # def query_metric_layer():
    # def generate_metric_flow_query():
    
    metrif_flow_command = answer_query_stream(query, index_name, chat_history, query_gen_prompt_style())
    fetch_data = fetch_data(query, metrif_flow_command)
    return fetch_data






    






