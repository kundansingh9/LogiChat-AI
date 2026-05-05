import os
import uuid
from dotenv import load_dotenv
import litellm
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()

# Set the API key in environment for LiteLLM (used by CrewAI)
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
MODEL_NAME = "groq/llama-3.3-70b-versatile"

@tool("DuckDuckGoSearch")
def search_tool(query: str):
    """Useful for searching the web for latest logistics and supply chain information."""
    return DuckDuckGoSearchRun().run(query)

class LogisticsResearcher:
    def __init__(self):
        # Create knowledge repo directory in the backend folder
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.repo_dir = os.path.join(base_dir, "knowledge_repo")
        os.makedirs(self.repo_dir, exist_ok=True)

    def research(self, query: str) -> dict:
        # Generate a unique file name for the output
        output_filename = f"{self.repo_dir}/research_{uuid.uuid4().hex[:8]}.txt"
        
        # Define the Agent
        researcher_agent = Agent(
            role='Logistics Research Specialist',
            goal=f'Conduct comprehensive research on the following query: {query}',
            backstory='You are an expert logistics researcher, capable of navigating the web '
                      'to find the most accurate, up-to-date, and relevant information regarding '
                      'supply chain and logistics. You synthesize complex information into clear summaries.',
            verbose=True,
            allow_delegation=False,
            tools=[search_tool],
            llm=MODEL_NAME
        )

        # Define the Task
        research_task = Task(
            description=f'Search the web for information related to: "{query}". '
                        f'Analyze the findings from multiple sources, summarize the key points, '
                        f'and format it into a comprehensive report.',
            expected_output='A detailed markdown report containing a comprehensive summary of the research findings.',
            agent=researcher_agent,
            output_file=output_filename
        )

        # Define the Crew
        crew = Crew(
            agents=[researcher_agent],
            tasks=[research_task],
            process=Process.sequential,
            verbose=True
        )

        # Execute the process
        result = crew.kickoff()
        
        return {
            "result": str(result),
            "file_path": output_filename
        }
