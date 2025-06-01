import os
import base64
import gradio as gr
from datetime import datetime
from openai import OpenAI
from PIL import Image
import io

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# Initialize OpenAI client
def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)

client = get_openai_client()

# Helper function to save base64 image
def save_image_from_b64(b64_string, filename_prefix="generated"):
    img_data = base64.b64decode(b64_string)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join("output", f"{filename_prefix}_{timestamp}.png")
    with open(filepath, "wb") as f:
        f.write(img_data)
    return filepath

# Image generation function
def generate_image(prompt):
    if not prompt or prompt.strip() == "":
        return None, "Please enter a prompt."
    
    try:
        # Call OpenAI API
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            n=1,
            size="1024x1024",
            response_format="b64_json"
        )
        
        # Get base64 image data
        image_b64 = response.data[0].b64_json
        
        # Convert base64 to PIL Image
        img_data = base64.b64decode(image_b64)
        pil_image = Image.open(io.BytesIO(img_data))
        
        # Save image to output folder
        filepath = save_image_from_b64(image_b64, "generated")
        
        return pil_image, f"✅ Image generated successfully! Saved to: {filepath}"
        
    except Exception as e:
        error_msg = f"❌ Error generating image: {str(e)}"
        return None, error_msg

# Create Gradio interface
with gr.Blocks(title="AI Image Generator") as app:
    gr.Markdown("# 🎨 AI Image Generator")
    gr.Markdown("Generate images from text prompts using OpenAI's DALL-E 3 model.")
    
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
                gen_output_image = gr.Image(label="Generated Image", type="pil", interactive=False)
                gen_status = gr.Textbox(label="Status", interactive=False)
        
        gen_button.click(
            fn=generate_image,
            inputs=[gen_prompt],
            outputs=[gen_output_image, gen_status],
            show_api=False 
        )

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
