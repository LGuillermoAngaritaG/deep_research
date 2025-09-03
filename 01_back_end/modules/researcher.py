from pydantic_ai import Agent
from models.researcher import documentationOutput
from config.config import Settings
from config.logs import logger
from utils.prompt_manager import PromptManager
from utils.update_progress import update_progress
from modules.mpcs.web_mcp import tavily_mcp


class Researcher:
    def __init__(self):
        self.settings = Settings()
        self.logger = logger

    async def make_research(self, plan: str, progress_callback=None):
        await update_progress(progress_callback, "🔍 Starting web research...")
        logger.info(f"Making research with model: {self.settings.MODEL_NAME}")
        
        tavily_server = tavily_mcp(self.settings.TAVILY_API_KEY)
        logger.info("Tavily server initialized...")

        # Setup research agent
        researcher_agent = Agent(
            self.settings.MODEL_NAME, 
            toolsets=[tavily_server], 
            instructions=PromptManager.get_prompt("researcher"),
            output_type=documentationOutput
        )

        await update_progress(progress_callback, "🌐 Searching the web for information...")
        logger.info("Searching the web for information...")
        # Do the research
        async with researcher_agent:
            result = await researcher_agent.run(f"The outline of the report is: {plan}")

        await update_progress(progress_callback, "📊 Research completed - organizing findings...")
        return result.output.sections