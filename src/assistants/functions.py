import sys
import io
import os
import re
import json
import subprocess
import google.auth
from metricflow import MetricFlowClient
from dbt.adapters.bigquery import Plugin
from metricflow.protocols.sql_client import SqlClient
from google.cloud.bigquery.client import Client

from typing import Any, List, Dict, Optional, Tuple

# sys.setdefaultencoding("utf-8")
# os.environ("PYTHONIOENCODING") = "utf-8"

class AttrDict(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value


class RecursiveAttrDict(dict):
    def __init__(self, data):
        super().__init__(data)
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = RecursiveAttrDict(value)  # Recursively apply to nested dicts
            elif isinstance(value, list):
                self[key] = [
                    RecursiveAttrDict(item) if isinstance(item, dict) else item
                    for item in value
                ]  # Apply to items in lists of dicts

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"No attribute '{key}' found")

    def __setattr__(self, key, value):
        if isinstance(value, dict):
            self[key] = RecursiveAttrDict(value)  # Ensure nested dicts are also AttrDicts
        else:
            self[key] = value


def run_query(metrics: List[str],
    tables: List[str],
    # tables_and_dims: List[str],
    group_by: List[str] = None,
    condition: List[str]  = None,
    order_by: List[str] = None,
    limit: int = None
):

    metrics = ', '.join(metrics)
    tables = ', '.join(tables)
    tables_and_dims = ', '.join(tables_and_dims)
    group_by = f"--group-by {', '.join(group_by)}" if group_by else ""
    limit = f"--limit {str(limit)}" if limit else ""
    order_by = f"--order -{', '.join(order_by)}" if order_by else ""
    condition = f"--where '{'condition'}'" if condition else ""

    # Example: f"query --metrics revenue_total --group-by sales_key__order_date"
    bash = f'''query --metrics {metrics} {group_by} {limit} {order_by} {condition}'''
    output = subprocess.run(["mf", bash], 
                    capture_output=True)
    print(output)
    return output


def llm_run_query_cmd(llm_query_input: str):
    # output = subprocess.run("mf query --metrics revenue_total --group-by metric_time --start-time '2017-08-01' --end-time '2017-08-31' ", 
    #                         cwd="./semantics/",
    #                         shell=True,
    #                         text=True,
    #                         capture_output=True,)

    try:
        output = subprocess.run(llm_query_input, 
                            cwd="./semantics/",
                            text=True, 
                            shell=True, 
                            encoding="utf-16",
                            capture_output=True,
                            )
        return output.stdout

    # output = subprocess.getstatusoutput("mf query --metrics revenue_total --group-by metric_time --start-time '2017-08-01' --end-time '2017-08-31' ", 
    #                             # cwd="./semantics/",
    #                             )
                                
    except Exception as e:
        print("Lots of encoding errors!!!")
        return "Couldn't fetch data"

    # command = llm_query_input +  "> ./retrieval/data/output.txt"
    # exit_status = os.system(command)

    # Check if the command was successful (exit status 0)
    # if exit_status == 0:
    #     with open("output.txt", "r", encoding="utf-8") as output_file:
    #         output = output_file.read()
    #     return output
        # with io.open(sys.stdout.fileno(), "w", encoding="utf-8") as stdout:
        #     exit_status = os.system(command)

        # return {
        #     'statusCode': 200,
        #     'status': 'Data retrieved successfully',
        # }
    
    # else:
    #     return {
    #         'statusCode': 500,
    #         'status': f"Error executing the command. Exit status: {exit_status}",
    #     }

    # return output.stdout


def llm_run_query_func(llm_query_input: str):
    mf_params = decompose_metricflow_command(llm_query_input)
    print(mf_params)

    credentials, project_id = google.auth.default()

    sql_client = Client(
        project="alphabeam",
        credentials=credentials,
        )

    semantic_manifest = json.load(open("./semantics/target/semantic_manifest.json"))

    semantic_manifest = RecursiveAttrDict(semantic_manifest)
    mfc = MetricFlowClient(sql_client, semantic_manifest)

    mf_query_function = mfc.query(
        mf_params['metrics'],
        dimensions = mf_params['dimensions'] if 'dimensions' in mf_params else [],
        where = mf_params['where'] if 'where' in mf_params else None,
        order = mf_params['order'] if 'order' in mf_params else None,
        limit = mf_params['limit'] if 'limit' in mf_params else None,
        start_time = mf_params['start_time'] if 'start_time' in mf_params else None,
        end_time = mf_params['end_time'] if 'end_time' in mf_params else None,
    )

    return mf_query_function


def decompose_metricflow_command(command_string):
   """Decomposes a MetricFlow command string into input parameters for a query function.

   Args:
       command_string: The MetricFlow command string to parse.

   Returns:
       A dictionary containing the extracted parameters:
           metrics: A list of metrics.
           dimensions: A list of dimensions.
           limit: An integer for the limit (if present).
           start_time: The start time (if present).
           end_time: The end time (if present).
           where: The WHERE clause (if present).
           order: The ORDER clause (if present).
   """

   params = {}

   # Extract metrics
   metrics_match = re.search(r"--metrics (\S+)", command_string)
   if metrics_match:
       params["metrics"] = metrics_match.group(1).split(",")

   # Extract dimensions
   dimensions_match = re.search(r"--group-by (\S+)", command_string)
   if dimensions_match:
       params["dimensions"] = dimensions_match.group(1).split(",")

   # Extract limit
   limit_match = re.search(r"--limit (\d+)", command_string)
   if limit_match:
       params["limit"] = int(limit_match.group(1))

   # Extract start_time
   start_time_match = re.search(r"--start-time '(\S+)'", command_string)
   if start_time_match:
       params["start_time"] = start_time_match.group(1)

   # Extract end_time
   end_time_match = re.search(r"--end-time '(\S+)'", command_string)
   if end_time_match:
       params["end_time"] = end_time_match.group(1)

   # Extract where clause
   where_match = re.search(r"--where '(.+)'", command_string)
   if where_match:
       params["where"] = where_match.group(1)

   # Extract order clause
   order_match = re.search(r"--order (\S+)", command_string)
   if order_match:
       params["order"] = order_match.group(1)

   return params




# examples
metric = "revenue_total"
action = ""