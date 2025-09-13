import os
from crewai import Crew, Process
from src.knowledge_sources import DatabaseKnowledgeSource
from src.tools import execute_sql_query_tool
from src.agents import create_agents
from src.tasks import create_tasks

class CrewAIQuerySystem:
    """Main class orchestrating the CrewAI database query and forecasting system."""
    
    def __init__(self, llm: str = "gpt-4o-mini"):
        self.llm = llm
        self.agents = None
        self.tasks = None
        self.crews = {}
        
    def setup_database(self, db_type: str, db_path: str = None, conn_string: str = None):
        """Setup database knowledge source and load schema."""
        self.db_source = DatabaseKnowledgeSource(
            db_path=db_path,
            db_type=db_type,
            conn_string=conn_string
        )
        self.schema_info = self.db_source.load_content()
        
    def initialize_agents_and_tasks(self):
        """Initialize all agents and tasks."""
        self.agents = create_agents(self.llm, self.schema_info, execute_sql_query_tool)
        self.tasks = create_tasks(self.agents)
        
    def create_crews(self):
        """Create specialized crews for different types of queries."""
        self.crews['sql'] = Crew(
            agents=[
                self.agents['fetch_table'],
                self.agents['fetch_column'],
                self.agents['sql_generator'],
                self.agents['sql_validator']
            ],
            tasks=[
                self.tasks['fetch_tables'],
                self.tasks['fetch_columns'],
                self.tasks['generate_sql'],
                self.tasks['validate_sql']
            ],
            process=Process.sequential
        )
        
        self.crews['forecasting'] = Crew(
            agents=[self.agents['forecasting']],
            tasks=[self.tasks['forecasting']],
            process=Process.sequential
        )
        
        self.crews['router'] = Crew(
            agents=[self.agents['router']],
            tasks=[self.tasks['router']],
            process=Process.sequential
        )
        
    def process_query(self, query: str, db_path: str = None, db_type: str = 'sqlite', conn_string: str = None):
        """Process user query through appropriate crew."""
        result = self.crews['router'].kickoff(inputs={'query': query})
        print(f"Router result: {result}")
        
        response = result.get('response')
        if response == "sql":
            return self.crews['sql'].kickoff(inputs={
                'query': query,
                'db_path': db_path,
                'db_type': db_type,
                'conn_string': conn_string
            })
        elif response == "forecast":
            return self.crews['forecasting'].kickoff(inputs={'query': query})
        else:
            return {"error": "Query type not recognized", "result": result}

from src.config import Config, DBTypeEnum

def main():
    """Main function to run the system."""
    try:
        # Validate configuration first
        Config.validate()
        
        os.environ["OPENAI_API_KEY"] = Config.OPENAI_API_KEY
        
        system = CrewAIQuerySystem()
        db_config = Config.get_db_config()
        
        print(f"Using database type: {Config.get_db_type_enum().value}")
        
        system.setup_database(**db_config)
        system.initialize_agents_and_tasks()
        system.create_crews()
        
        query = "Which park had most attendances in 2008?"
        result = system.process_query(query, **db_config)
        print(f"Final result: {result}")
        
    except Exception as e:
        print(f"Configuration Error: {str(e)}")

