# CrewAI Database Query & Forecasting System

A sophisticated multi-agent system built with CrewAI that intelligently routes natural language queries to specialized agents for SQL database analysis or time series forecasting. Supports both SQLite and PostgreSQL databases with a clean, modular architecture.

[![Python 3.8+](https://img.shields.io/badgehttps://www.python.org/downloadshttps://img.shields.io/badgehttps://opensource.org/licenseshttps://img.shields.io/badgehttps://github.com/crewAI 🚀 Features

- **Intelligent Query Routing**: Automatically determines if queries need SQL analysis or forecasting
- **Multi-Database Support**: Works with both SQLite and PostgreSQL databases
- **Modular Architecture**: Clean base classes for agents, tasks, tools, and knowledge sources
- **Type-Safe Configuration**: Enum-based database type validation
- **Environment-Based Config**: Secure configuration management with `.env` files
- **Schema-Aware SQL Generation**: Automatically loads and utilizes database schemas
- **Error Handling**: Comprehensive error handling and validation throughout
- **Extensible Design**: Easy to add new database types or agent capabilities

## 📋 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Support](#support)
- [Roadmap](#roadmap)

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Database (SQLite file or PostgreSQL instance)

### Install Dependencies

1. Clone the repository:
```bash
git clone https://github.com/dhirajkiran007/crewai-text2sql.git
cd crewai-text2sql
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## ⚙️ Configuration

Create a `.env` file in the project root:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
DB_TYPE=sqlite  # Options: sqlite | postgres (defined in DBTypeEnum)

# SQLite Configuration (only needed when DB_TYPE=sqlite)
SQLITE_DB_PATH=C:\database\baseball_1.sqlite

# PostgreSQL Configuration (only needed when DB_TYPE=postgres)
POSTGRES_HOST=localhost          # Database host
POSTGRES_PORT=5432              # Database port (default: 5432)
POSTGRES_DB=your_database_name   # Database name
POSTGRES_USER=your_username      # Database username
POSTGRES_PASSWORD=your_password  # Database password
```

### Database Type Configuration

The system uses a type-safe enum for database configuration:

```python
from src.config import DBTypeEnum

# Available options:
DBTypeEnum.SQLITE    # 'sqlite'
DBTypeEnum.POSTGRES  # 'postgres'
```

## 🏃‍♂️ Usage

### Basic Usage

```python
from main import CrewAIQuerySystem
from src.config import Config

# Initialize system
system = CrewAIQuerySystem()

# Setup database (automatically configured from .env)
db_config = Config.get_db_config()
system.setup_database(**db_config)
system.initialize_agents_and_tasks()
system.create_crews()

# Process a query
query = "Which park had the most attendances in 2008?"
result = system.process_query(query, **db_config)
print(result)
```

### Command Line Usage

```bash
python main.py
```

### Example Queries

**SQL Queries:**
- "Which park had the most attendances in 2008?"
- "Show me the top 5 teams by wins last season"
- "What's the average salary by position?"

**Forecasting Queries:**
- "Predict next quarter's sales"
- "Forecast visitor trends for next month"
- "What will be the expected growth rate?"

## 📁 Project Structure

```
crewai-text2sql/
├── src/
│   ├── __init__.py
│   ├── base_agent.py              # Base class for all agents
│   ├── base_task.py               # Base class for all tasks
│   ├── base_tool.py               # Base class for all tools
│   ├── base_knowledge_source.py   # Base class for knowledge sources
│   ├── agents.py                  # Agent definitions
│   ├── tasks.py                   # Task definitions
│   ├── tools.py                   # Custom tools (SQL executor, etc.)
│   ├── knowledge_sources.py       # Database schema fetchers
│   └── config.py                  # Configuration management
├── tests/
│   └── test_tools.py              # Unit tests
├── .env                           # Environment variables
├── .gitignore                     # Git ignore file
├── README.md                      # This file
├── requirements.txt               # Dependencies
├── main.py                        # Entry point
└── LICENSE                        # MIT License
```

## 🏗️ Architecture

### Agent Workflow

1. **Router Agent**: Analyzes query intent and routes to appropriate crew
2. **SQL Crew**: 
   - **Table Fetcher**: Identifies relevant database tables
   - **Column Fetcher**: Retrieves relevant columns
   - **SQL Generator**: Creates SQL queries from natural language
   - **SQL Validator**: Validates and executes SQL queries
3. **Forecasting Crew**: Handles time series analysis and predictions

### Base Classes

All components inherit from custom base classes for consistency:

- `BaseAgent`: Common agent functionality and error handling
- `BaseTask`: Standardized task structure and validation
- `BaseCustomTool`: Shared tool methods and error management
- `BaseCustomKnowledgeSource`: Common knowledge source patterns

## 📊 Examples

### SQLite Example

```python
# Configure for SQLite
os.environ["DB_TYPE"] = "sqlite"
os.environ["SQLITE_DB_PATH"] = "database/baseball.sqlite"

system = CrewAIQuerySystem()
result = system.process_query("Show teams with most wins")
```

### PostgreSQL Example

```python
# Configure for PostgreSQL
os.environ["DB_TYPE"] = "postgres"
os.environ["POSTGRES_HOST"] = "localhost"
os.environ["POSTGRES_DB"] = "sports_analytics"

system = CrewAIQuerySystem()
result = system.process_query("Analyze player performance trends")
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Add tests for new functionality
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Running Tests

```bash
python -m pytest tests/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

* **[CrewAI](https://github.com/crewAIInc/crewAI)** - Multi-agent framework
* **[LangChain](https://github.com/hwchase17/langchain)** - LLM application framework
* **[OpenAI](https://openai.com/)** - Language model APIs
* **[Model Context Protocol](https://modelcontextprotocol.io/)** - Tool integration standard (planned for future development)

## 📞 Support

* **Documentation**: Check the inline code documentation
* **Issues**: [GitHub Issues](https://github.com/dhirajkiran007/crewai-text2sql/issues)
* **Discussions**: [GitHub Discussions](https://github.com/dhirajkiran007/crewai-text2sql/discussions)

## 🗺️ Roadmap

* [ ] **Web Dashboard** - React-based GUI for easier interaction
* [ ] **Forecasting Model** - Integration for future predictions
* [ ] **More AI Models** - Support for Anthropic Claude, Google Gemini, Ollama (local)
* [ ] **Advanced Analytics** - Performance metrics and agent success rates
* [ ] **Plugin Ecosystem** - Custom tool development framework
* [ ] **Multi-Cloud Deployment** - AWS, Azure, GCP deployment templates
* [ ] **Batch Processing** - Handle multiple queries simultaneously
* [ ] **Agent Templates** - Pre-built agent configurations for common use cases
* [ ] **Real-time Collaboration** - Multi-user agent sharing and collaboration

***

**Made with ❤️ using CrewAI, Langchain, and Python**  
*Transform natural language queries into powerful database insights and forecasts with CrewAI's flexible multi-agent architecture*

***

⭐ If you find this project useful, please consider giving it a star on GitHub!

[1](https://docs.crewai.com)
[2](https://docs.crewai.com/tools/database-data/overview)
[3](https://docs.crewai.com/introduction)
[4](https://composio.dev/blog/crewai-examples)
[5](https://docs.crewai.com/concepts/knowledge)
[6](https://docs.crewai.com/tools/overview)