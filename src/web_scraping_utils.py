import os
from web.base import ReadabilityWebPageReader

def web_loader(urls:list, dir_to_save:str):
    loader = ReadabilityWebPageReader()
    print("Collecting pages...")
    web_documents = [i for url in urls for i in loader.load_data(url)]
    
    for webpage in web_documents:
        print("Writing webpage to text...")
        page_name = webpage.get_doc_id() + '.txt'
        with open(os.path.join(dir_to_save, page_name), 'w', encoding='utf-8') as file:
            file.write(webpage.get_text())

    return {
            'statusCode': 200,
            'status': 'Web pages scraped succesully',
        }

# load MetricFlow documentation
webpages = [
    "https://docs.getdbt.com/docs/build/metricflow-commands#metricflow",
    "https://docs.getdbt.com/docs/build/metricflow-commands#metricflow-commands",
    "https://docs.getdbt.com/docs/build/metricflow-commands#query",
    "https://docs.getdbt.com/docs/build/metricflow-commands#query-examples",
    "https://docs.getdbt.com/docs/build/metricflow-commands#time-granularity",
    "https://docs.getdbt.com/docs/build/metricflow-commands#faqs",

]

# load from github, cleaner output
webpages = [
    "https://github.com/dbt-labs/docs.getdbt.com/blob/current/website/docs/docs/build/metricflow-commands.md"
    ]

web_loader(webpages, "./retrieval/metric_flow_docs/")

