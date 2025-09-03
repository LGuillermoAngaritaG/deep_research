import gradio as gr
import asyncio
from core.logic import DeepResearchLogic
import queue
import threading

# Initialize the deep research logic
deep_research = DeepResearchLogic()

class InteractiveResearchSession:
    def __init__(self):
        self.question_queue = queue.Queue()
        self.answer_queue = queue.Queue()
        self.progress_queue = queue.Queue()
        self.is_waiting_for_answer = False
        self.current_question = None
        self.session_active = False
        
    async def ask_user(self, question):
        """Callback function to ask user for input through the UI"""
        self.current_question = question
        self.is_waiting_for_answer = True
        
        # Put the question in the queue for the UI to pick up
        self.question_queue.put(question)
        
        # Wait for the answer from the UI
        while self.is_waiting_for_answer:
            try:
                answer = self.answer_queue.get(timeout=1)
                self.is_waiting_for_answer = False
                self.current_question = None
                return answer
            except queue.Empty:
                await asyncio.sleep(0.1)
                continue
    
    def provide_answer(self, answer):
        """Provide answer from the UI"""
        if self.is_waiting_for_answer:
            self.answer_queue.put(answer)
    
    async def report_progress(self, message):
        """Report progress updates to the UI"""
        self.progress_queue.put(("PROGRESS", message))

# Global session instance
research_session = InteractiveResearchSession()

async def process_research_async(question):
    """Async function to process research"""
    research_session.session_active = True
    try:
        result = await deep_research.execute(
            question, 
            research_session.ask_user,
            research_session.report_progress
        )
        return result
    except Exception as e:
        return f"Error processing your question: {str(e)}"
    finally:
        research_session.session_active = False

def start_research(question, history):
    """Start the research process"""
    if not question.strip():
        return history + [{"role": "assistant", "content": "Please enter a question to research."}], ""
    
    # Add the initial question to history
    history = history + [
        {"role": "user", "content": question},
        {"role": "assistant", "content": "🔍 Starting research... This may take a few moments."}
    ]
    
    # Start research in a separate thread
    def run_research():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(process_research_async(question))
            research_session.answer_queue.put(("FINAL_RESULT", result))
        except Exception as e:
            research_session.answer_queue.put(("ERROR", str(e)))
        finally:
            loop.close()
    
    thread = threading.Thread(target=run_research)
    thread.daemon = True
    thread.start()
    
    return history, ""

def check_for_updates(history):
    """Check for agent questions, progress updates, or final results"""
    try:
        # Process ALL progress updates first to ensure they're displayed before questions
        progress_updates = []
        while not research_session.progress_queue.empty():
            try:
                item = research_session.progress_queue.get_nowait()
                if isinstance(item, tuple) and item[0] == "PROGRESS":
                    progress_updates.append(item[1])
            except queue.Empty:
                break
        
        # Add all progress updates to history
        if progress_updates:
            for update in progress_updates:
                history = history + [{"role": "assistant", "content": update}]
            return history, gr.update(), gr.update()
        
        # Check for agent questions (only after all progress is processed)
        if not research_session.question_queue.empty():
            question = research_session.question_queue.get_nowait()
            history = history + [{"role": "assistant", "content": f"🤖 Agent Question: {question}"}]
            # Update the main input field to answer mode
            return history, gr.update(placeholder="Enter your answer here...", label="Answer to Agent Question"), gr.update(value="Submit Answer")
        
        # Check for results
        if not research_session.answer_queue.empty():
            item = research_session.answer_queue.get_nowait()
            if isinstance(item, tuple) and item[0] == "FINAL_RESULT":
                history = history + [{"role": "assistant", "content": f"✅ Research Complete:\n\n{item[1]}"}]
                # Reset input field to question mode
                return history, gr.update(placeholder="Enter your research question...", label=""), gr.update(value="Send")
            elif isinstance(item, tuple) and item[0] == "ERROR":
                history = history + [{"role": "assistant", "content": f"❌ Error: {item[1]}"}]
                # Reset input field to question mode
                return history, gr.update(placeholder="Enter your research question...", label=""), gr.update(value="Send")
    except queue.Empty:
        pass
    
    return history, gr.update(), gr.update()

def handle_input(input_text, history):
    """Handle both initial questions and follow-up answers"""
    if not input_text.strip():
        return history, input_text, gr.update(), gr.update()
    
    # If waiting for answer, submit as answer
    if research_session.is_waiting_for_answer:
        history = history + [{"role": "user", "content": input_text}]
        research_session.provide_answer(input_text.strip())
        # Reset input field to question mode
        return history, "", gr.update(placeholder="Enter your research question...", label=""), gr.update(value="Send")
    else:
        # Start new research - extend start_research return to match expected outputs
        updated_history, cleared_input = start_research(input_text, history)
        return updated_history, cleared_input, gr.update(), gr.update()

def clear_chat():
    """Clear the conversation history and reset the session"""
    # Clear all queues
    while not research_session.question_queue.empty():
        try:
            research_session.question_queue.get_nowait()
        except queue.Empty:
            break
    
    while not research_session.answer_queue.empty():
        try:
            research_session.answer_queue.get_nowait()
        except queue.Empty:
            break
            
    while not research_session.progress_queue.empty():
        try:
            research_session.progress_queue.get_nowait()
        except queue.Empty:
            break
    
    # Reset session state
    research_session.is_waiting_for_answer = False
    research_session.current_question = None
    research_session.session_active = False
    
    # Reset UI to question mode
    return [], "", gr.update(placeholder="Enter your research question...", label=""), gr.update(value="Send")

css = """
/* Hide all elements that might be loading indicators */
[class*="loading"],
[class*="pending"],
[class*="generating"],
[class*="typing"],
[class*="progress"],
[class*="queue"] {
    display: none !important;
}

/* Improved scroll behavior for chatbot */
.chatbot {
    scroll-behavior: smooth !important;
}

"""
# Create the Gradio interface
with gr.Blocks(title="Deep Research Assistant", css=css) as demo:
    gr.Markdown("# Deep Research Assistant")
    gr.Markdown("Ask any question and get a comprehensive research report! The agent may ask follow-up questions during the research process.")
    
    with gr.Row():
        with gr.Column(scale=4):
            # Chat interface for the conversation
            chatbot = gr.Chatbot(
                label="Research Conversation",
                height=600,
                show_copy_button=True,
                type="messages",
                autoscroll=False, 
            )
            
            with gr.Row():
                question_input = gr.Textbox(
                    label="",
                    placeholder="Enter your research question...",
                    lines=2,
                    scale=4
                )
                with gr.Column(scale=1):
                    send_btn = gr.Button("Send", variant="primary")
                    clear_btn = gr.Button("Clear Chat", variant="secondary")
    
    # State to keep track of conversation history
    conversation_state = gr.State([])
    
    # Handle input (both questions and answers)
    send_btn.click(
        fn=handle_input,
        inputs=[question_input, conversation_state],
        outputs=[conversation_state, question_input, question_input, send_btn]
    ).then(
        fn=lambda x: x,
        inputs=[conversation_state],
        outputs=[chatbot]
    )
    
    question_input.submit(
        fn=handle_input,
        inputs=[question_input, conversation_state],
        outputs=[conversation_state, question_input, question_input, send_btn]
    ).then(
        fn=lambda x: x,
        inputs=[conversation_state],
        outputs=[chatbot]
    )
    
    # Clear chat functionality
    clear_btn.click(
        fn=clear_chat,
        inputs=[],
        outputs=[conversation_state, question_input, question_input, send_btn]
    ).then(
        fn=lambda x: x,
        inputs=[conversation_state],
        outputs=[chatbot]
    )
    
    # Timer for periodic updates
    timer = gr.Timer(0.5)
    
    timer.tick(
        fn=check_for_updates,
        inputs=[conversation_state],
        outputs=[conversation_state, question_input, send_btn]
    ).then(
        fn=lambda x: x,
        inputs=[conversation_state],
        outputs=[chatbot]
    )
