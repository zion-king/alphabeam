from flask import Flask, jsonify, flash, request, redirect, render_template, url_for, Response, stream_with_context
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from retrieval.semantic_retrieval import *
import warnings
warnings.filterwarnings("ignore")


app = Flask(__name__)
app.debug = True

cors = CORS(app)
app.chat_history = init_chat_history()

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
        
        for i in ["marts","metrics","semantic_models"]:
            data_dir = f'./semantics/models/{i}/'
            generate_vector_embedding_chroma(index_name, data_dir)
        
        # add metricflow documentation to semantic embeddings
        generate_vector_embedding_chroma(index_name, "./retrieval/metric_flow_docs/")

        response = {
            'statusCode': 200,
            'status': 'Vector embeddings created and stored successfully!',
        }
        return response
    return render_template('index.html')



@app.route("/retrieval", methods=["GET","POST"])
@cross_origin()
def answer_gen():
    project = request.json
    project_name = project['projectName']
    index_name = project_name.replace(' ', '_').lower() + '_embeddings'

    if project['reset_chat'] in [True,'True','Yes']:
        app.chat_history = init_chat_history()

    # query semantic layer to check whether information exists
    query = project['query']
    answer_exists = answer_query_stream(query, index_name, semantic_prompt_style())

    if answer_exists != 'Yes':
        return "The source data doesn't contain the requested information. Please rephrase your question or ask me another question."
    
    # use semantic and metric layers to assist Gemini to generate MetricFlow command to retrieve the data
    metrif_flow_command = answer_query_stream(query, index_name, query_gen_prompt_style())
    print("Got command >>>", metrif_flow_command)

    # run generated MetricFlow command against database
    output = fetch_data(query, metrif_flow_command, app.chat_history)
    return output


if __name__ == "__main__":
    print("Starting AlphBeam App...")
    app.debug = True
    app.run()