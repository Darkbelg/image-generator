import os
import gradio as gr

# Ensure output directory exists - good practice even if not used by MVP
os.makedirs("output", exist_ok=True)

# Create a minimal Gradio interface
with gr.Blocks(title="MVP Gradio App") as app:
    gr.Markdown("# 👋 MVP Gradio App")
    gr.Markdown("This is a minimal Gradio application to test the launch.")
    gr.Markdown("If you see this, the basic Gradio server is working!")

if __name__ == "__main__":
    # Read configuration from environment variables
    port = int(os.environ.get("APP_PORT", 7860))
    debug = os.environ.get("APP_DEBUG", "False").lower() == "true"
    
    app.launch(
        server_name="0.0.0.0",  # Listen on all interfaces
        server_port=port,
        share=False,
        debug=debug
    )
