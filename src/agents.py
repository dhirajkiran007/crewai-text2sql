from src.base_agent import BaseAgent

def create_agents(llm, schema_info, execute_sql_query_tool):
    router_agent = BaseAgent(
        role='Router',
        goal='Route queries to appropriate specialized agents',
        backstory="""You are an intelligent router that analyzes user queries and determines whether they need SQL analysis or forecasting analysis.""",
        llm=llm
    )

    fetch_table_agent = BaseAgent(
        role='Table Fetcher',
        goal='Fetch and understand available database tables',
        backstory="""You are specialized in retrieving database table information and understanding table relationships.""",
        knowledge_sources=[schema_info],
        llm=llm
    )

    fetch_column_agent = BaseAgent(
        role='Column Fetcher',
        goal='Fetch and understand table columns',
        backstory="""You are specialized in retrieving and understanding table columns and their data types.""",
        knowledge_sources=[schema_info],
        llm=llm
    )

    sql_generator_agent = BaseAgent(
        role='SQL Generator',
        goal='Generate accurate SQL queries',
        backstory="""You are an expert in generating SQL queries based on natural language requests and database structure.""",
        llm=llm
    )

    sql_validator_agent = BaseAgent(
        role='SQL Validator',
        goal='Validate SQL queries for correctness and execute them on the database',
        backstory="""You are specialized in validating SQL queries for syntax and logical correctness, and executing them on the connected database.""",
        llm=llm,
        tools=[execute_sql_query_tool]
    )

    forecasting_agent = BaseAgent(
        role='Forecasting Analyst',
        goal='Generate accurate time series forecasts',
        backstory="""You are an expert in time series analysis and forecasting, specialized in using Prophet for predictions.""",
        llm=llm
    )

    return {
        'router': router_agent,
        'fetch_table': fetch_table_agent,
        'fetch_column': fetch_column_agent,
        'sql_generator': sql_generator_agent,
        'sql_validator': sql_validator_agent,
        'forecasting': forecasting_agent
    }
