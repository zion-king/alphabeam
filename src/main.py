from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.retrieval.semantic_retrieval import *
import gunicorn
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class LLMRequest(BaseModel):
    projectName: str
    query: str
    reset_chat: str

app = FastAPI()


@app.on_event("startup")
async def startup():
    print("Alphabeam::Started")

origins = [
    "*",
]

# add middleware to allow CORS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/health')
async def health():
    return {
      'application':'AlphaBeam CBI API',
      'version':'1.0.0',
      'message': "endpoint working"
    }

# @app.post('/embedding')
# async async def process():    
#     if request.method == 'POST':
#         project_name = request.form['projectName']
#         index_name = project_name.replace(' ', '_').lower() + '_embeddings'
        
#         for i in ["marts","metrics","semantic_models"]:
#             data_dir = f'./semantics/models/{i}/'
#             await generate_vector_embedding_chroma(index_name, data_dir)
        
#         # add metricflow documentation to semantic embeddings
#         await generate_vector_embedding_chroma(index_name, "./retrieval/metric_flow_docs/")

#         response = {
#             'statusCode': 200,
#             'status': 'Vector embeddings created and stored successfully!',
#         }
#         return response
#     return render_template('index.html')


@app.post("/retrieval")
async def answer_gen(data:LLMRequest):
    project_name = data.projectName
    index_name = project_name.replace(' ', '_').lower() + '_embeddings'

    if data.reset_chat in [True,'True','Yes']:
        app.chat_history = await init_chat_history()

    query = data.query

    # query semantic layer to check whether information exists
    # we will revist this layer... more prompt tuning required
    # answer_exists = answer_query_stream(query, index_name, semantic_prompt_style())

    # if answer_exists != 'Yes':
    #     return "The source data doesn't contain the requested information. Please rephrase your question or ask me another question."
    
    # use semantic and metric layers to assist Gemini to generate MetricFlow command to retrieve the data
    metrif_flow_command = await answer_query_stream(query, index_name, query_gen_prompt_style())
    print("Got command >>>", metrif_flow_command)

    # run generated MetricFlow command against database
    output = await fetch_data(query, metrif_flow_command, app.chat_history)
    if output is not None:
        return JSONResponse({
                "statusCode": 200,
                "result": output
            },status_code=200)
    else:
        return JSONResponse({
                "statusCode": 400,
                "result": str(output) + "malformed"
            },status_code=400)

if __name__ == "__main__":
    gunicorn.run(app,host='0.0.0.0',port=7000)