from pydantic_ai import Agent
from models.writer import reportOutput
from config.config import Settings
from config.logs import logger
from utils.prompt_manager import PromptManager
from models.researcher import Section
from utils.update_progress import update_progress

class Writer:
    def __init__(self):
        self.settings = Settings()
        self.logger = logger

    async def make_report(self, information: list[Section], plan: str, progress_callback=None):
        await update_progress(progress_callback, "📝 Analyzing research data...")
        logger.info(f"Making report with model: {self.settings.MODEL_NAME}")

        # Setup writer agent
        writer_agent = Agent(
            self.settings.MODEL_NAME,
            instructions=PromptManager.get_prompt("writer"),
            output_type=reportOutput
        )
        
        await update_progress(progress_callback, "✍️ Generating comprehensive report...")
        logger.info("Generating report...")

        result = await writer_agent.run(f"""Write a report about the following outline: {plan}
        A Researcher has found the following information for each section: {information}
        Please use this to create a comprehesive report""")
        
        await update_progress(progress_callback, "✅ Report completed successfully!")
        return result.output.report