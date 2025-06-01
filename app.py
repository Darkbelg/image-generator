import os
import gradio as gr

# Ensure output directory exists - good practice even if not used by MVP
os.makedirs("output", exist_ok=True)

# Create Gradio interface with image generation tab
with gr.Blocks(title="AI Image Generator") as app:
    gr.Markdown("# 🎨 AI Image Generator")
    gr.Markdown("Generate images from text prompts using OpenAI's gpt-image-1 model.")
    
    with gr.Tabs():
        # Image Generation Tab
        with gr.Tab("🖼️ Generate Image"):
            gr.Markdown("### Generate a new image from a text description")
            
            with gr.Row():
                with gr.Column():
                    gen_prompt = gr.Textbox(
                        label="Enter your prompt",
                        placeholder="Describe the image you want to generate...",
                        lines=3
                    )
                    gen_button = gr.Button("Generate Image", variant="primary")
                
                with gr.Column():
                    gen_output_image = gr.Image(label="Generated Image", type="pil")
                    gen_status = gr.Textbox(label="Status", interactive=False)
            
            # For now, connect to a simple test function
            def test_button_click(prompt):
                if not prompt or prompt.strip() == "":
                    return None, "Please enter a prompt."
                return None, f"Button clicked! Prompt: {prompt[:50]}..."

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
