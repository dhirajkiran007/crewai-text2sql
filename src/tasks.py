from src.base_task import BaseTask

def create_tasks(agents):
    router_task = BaseTask(
        description="""Analyze the {query} to understand its intent. Determine if the query requires SQL analysis or forecasting and route it to the appropriate agent.""",
        expected_output="""Output must be either 'sql' or 'forecast' or None based on the query type in dictionary format. For example: {{"response":"sql"}} or {{"response":"forecast"}} or {{"response":None}}""",
        agent=agents['router']
    )

    fetch_tables_task = BaseTask(
        description="""Retrieve all relevant tables from the database needed for {query}.""",
        expected_output="""Output must be a dictionary containing only the relevant tables. For example: {{"relevant_tables": ['table1', 'table2', ...]}}""",
        agent=agents['fetch_table']
    )

    fetch_columns_task = BaseTask(
        description="""Retrieve all relevant columns from the tables identified for {query}.""",
        expected_output="""Output must be a dictionary containing tables and their relevant columns. For example: {{'table1': ['column1', ...], 'table2': ['column1', ...]}}""",
        agent=agents['fetch_column']
    )

    generate_sql_task = BaseTask(
        description="""Generate an SQL query based on the available tables and columns for {query}.""",
        expected_output="""Output must be a dictionary containing the generated SQL query. For example: {{"sql": "SELECT ..."}}""",
        agent=agents['sql_generator']
    )

    validate_sql_task = BaseTask(
        description="""Validate the generated SQL query for correctness, ensure it follows syntax and logical rules, and execute the query against the database. The query should be executed and the result or any error should be returned.""",
        expected_output="""Output must be in dictionary format with 'status', 'message', and optional 'data'. For example: {{'status': 'success', 'message': 'Query executed successfully', 'data': [...]}} or {{'status': 'error', 'message': 'SQL syntax error', 'data': None}}""",
        agent=agents['sql_validator']
    )

    forecasting_task = BaseTask(
        description="""Analyze time series data and generate forecasts using Prophet for the {query}.""",
        expected_output="""Output MUST be in dict format. For example: {{"predicted": value}}""",
        agent=agents['forecasting']
    )

    return {
        'router': router_task,
        'fetch_tables': fetch_tables_task,
        'fetch_columns': fetch_columns_task,
        'generate_sql': generate_sql_task,
        'validate_sql': validate_sql_task,
        'forecasting': forecasting_task
    }
