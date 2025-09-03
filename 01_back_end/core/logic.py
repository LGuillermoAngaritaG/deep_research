import asyncio
from modules.planner import Planner
from modules.researcher import Researcher
from modules.writer import Writer
from utils.update_progress import update_progress

from config.logs import logger

class DeepResearchLogic:
    def __init__(self):
        self.planner = Planner()
        self.researcher = Researcher()
        self.writer = Writer()
        self.logger = logger

    async def execute(self, question: str, user_input_callback=None, progress_callback=None):
        try:
            # Step 1: Create the plan
            logger.info("Creating research plan...")
            await update_progress(progress_callback, "🤔 Planning your research...")
            plan = await self.planner.make_plan(question, user_input_callback, progress_callback)

            logger.info("Plan created successfully. Starting research...")
            # Show the plan to user
            await update_progress(progress_callback, f"📋 **Research Plan Created:**\n\n{plan}")
            
            # Small delay to ensure the plan gets displayed before proceeding
            await asyncio.sleep(0.5)
            
            # Step 2: Research
            information = await self.researcher.make_research(plan, progress_callback)
            logger.info("Research completed successfully. Starting report...")
            
            # Step 3: Write report
            report = await self.writer.make_report(information, plan, progress_callback)
            logger.info("Report completed successfully!")
            
        except Exception as e:
            logger.error(f"Error executing research: {e}")
            raise e

        return report
