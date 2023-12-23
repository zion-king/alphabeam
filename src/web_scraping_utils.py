import os
from web.base import ReadabilityWebPageReader

def web_loader(urls:list, dir_to_save:str):
    loader = ReadabilityWebPageReader()
    web_documents = [i for url in urls for i in loader.load_data(url)]
    
    for webpage in web_documents:
        page_name = webpage.get_doc_id() + '.txt'
        with open(os.path.join(dir_to_save, page_name), 'w', encoding='utf-8') as file:
            file.write(webpage.get_text())

    return {
            'statusCode': 200,
            'status': 'Web pages scraped succesully',
        }

# load MetricFlow documentation
web_loader(["https://docs.getdbt.com/docs/build/metricflow-commands"], "./retrieval/metric_flow_docs/")

