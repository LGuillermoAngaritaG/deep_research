from fastapi import FastAPI
import gradio as gr
from app import demo

app = FastAPI(title="Deep Research API", version="1.0.0")

app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=False)