from pydantic_ai import Agent
from pydantic_ai import RunContext
from models.planner import PlanOutput, GetHumanInTheLoopInput, GetHumanInTheLoopOutput, GetPlanInput, GetPlanOutput
from config.config import Settings
from config.logs import logger
from utils.prompt_manager import PromptManager
from utils.update_progress import update_progress

class Planner:
    def __init__(self):
        self.settings = Settings()
        self.logger = logger

    async def make_plan(self, question: str, user_input_callback=None, progress_callback=None):
        await update_progress(progress_callback, "🧠 Creating research plan...")
        logger.info(f"Making plan with model: {self.settings.MODEL_NAME}")

        # Setup planning agent
        planning_agent = Agent(
            model=self.settings.MODEL_NAME,
            system_prompt=PromptManager.get_prompt("planner"),
            output_type=PlanOutput
        )
        # Tools for planning agent
        @planning_agent.tool
        async def get_plan(_: RunContext[GetPlanInput], instructions_for_plan: str) -> GetPlanOutput:
            outline_agent = Agent(self.settings.MODEL_NAME,
                        instructions="You are an experienced planner for a research project, you will be given a query from the user and you need to make an outline of the report to give the user about it, and what to search for in the web in order to create the report",
                        output_type=GetPlanOutput)
            logger.info("Creating plan...")
            result = await outline_agent.run(instructions_for_plan)
            return GetPlanOutput(plan=result.output.plan)
        
        @planning_agent.tool
        async def get_human_in_the_loop(_: RunContext[GetHumanInTheLoopInput], question: str) -> GetHumanInTheLoopOutput:
            await update_progress(progress_callback, "❓ Need your input...")
            logger.info("Asking User for input...")
            if user_input_callback:
                input_str = await user_input_callback(f"Please provide your input for the question > '{question}': ")
            else:
                # Fallback to console input if no callback provided
                input_str = input(f"Please provide your input for the question > '{question}': ")
            logger.info("User input received...")
            return GetHumanInTheLoopOutput(answer=input_str)
        
        result = await planning_agent.run(question)
        return result.output.outline