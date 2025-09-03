async def update_progress(progress_callback, message):
    """
    Helper function to send progress updates to the UI
    
    Args:
        progress_callback: Optional callback function to send progress to
        message: The progress message to send
    """
    if progress_callback:
        await progress_callback(message)