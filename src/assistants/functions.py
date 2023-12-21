import subprocess
from typing import Any, List Dict, Optional, Tuple


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


def llm_run_query(llm_query_input: str):
    output = subprocess.run(["mf", llm_query_input], 
                    capture_output=True)
    print(output)
    return output



# examples
metric = "revenue_total"
action = ""