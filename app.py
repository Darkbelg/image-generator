import os
import base64
import gradio as gr
from openai import OpenAI
from datetime import datetime
from PIL import Image
import io

# Initialize OpenAI client
def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# Initialize OpenAI client
try:
    client = get_openai_client()
except ValueError as e:
    print(f"Error: {e}")
    client = None

def save_image_from_b64(b64_string, filename_prefix="generated"):
    """Save base64 encoded image to output directory"""
    try:
        img_data = base64.b64decode(b64_string)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join("output", f"{filename_prefix}_{timestamp}.png")
        
        with open(filepath, "wb") as f:
            f.write(img_data)
        
        return filepath
    except Exception as e:
        raise Exception(f"Failed to save image: {str(e)}")

def generate_image(prompt):
    """Generate an image from a text prompt"""
    if not client:
        return None, "Error: OpenAI client not initialized. Please check your API key."
    
    if not prompt or prompt.strip() == "":
        return None, "Error: Please enter a prompt."
    
    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt.strip(),
            n=1,
            size="1024x1024",
            response_format="b64_json"
        )
        
        image_b64 = response.data[0].b64_json
        
        # Save the image
        filepath = save_image_from_b64(image_b64, "generated")
        
        # Convert base64 to PIL Image for display
        img_data = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(img_data))
        
        success_message = f"✅ Image generated successfully!\nSaved to: {filepath}"
        return image, success_message
        
    except Exception as e:
        error_message = f"❌ Error generating image: {str(e)}"
        return None, error_message

def edit_image(input_image, prompt, mask_image=None):
    """Edit an image using a text prompt and optional mask"""
    if not client:
        return None, "Error: OpenAI client not initialized. Please check your API key."
    
    if input_image is None:
        return None, "Error: Please upload an image to edit."
    
    if not prompt or prompt.strip() == "":
        return None, "Error: Please enter an edit prompt."
    
    try:
        # Convert PIL Image to bytes
        img_byte_arr = io.BytesIO()
        input_image.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()
        
        # Prepare mask if provided
        mask_bytes = None
        if mask_image is not None:
            # Convert mask to RGBA if needed
            if mask_image.mode != 'RGBA':
                # Convert to grayscale first, then to RGBA
                mask_gray = mask_image.convert('L')
                mask_rgba = mask_gray.convert('RGBA')
                # Use the grayscale values as alpha channel
                mask_rgba.putalpha(mask_gray)
            else:
                mask_rgba = mask_image
            
            mask_byte_arr = io.BytesIO()
            mask_rgba.save(mask_byte_arr, format='PNG')
            mask_bytes = mask_byte_arr.getvalue()
        
        # Call OpenAI API
        response = client.images.edit(
            model="gpt-image-1",
            image=img_bytes,
            mask=mask_bytes,
            prompt=prompt.strip(),
            n=1,
            size="1024x1024",
            response_format="b64_json"
        )
        
        image_b64 = response.data[0].b64_json
        
        # Save the edited image
        filepath = save_image_from_b64(image_b64, "edited")
        
        # Convert base64 to PIL Image for display
        img_data = base64.b64decode(image_b64)
        edited_image = Image.open(io.BytesIO(img_data))
        
        success_message = f"✅ Image edited successfully!\nSaved to: {filepath}"
        return edited_image, success_message
        
    except Exception as e:
        error_message = f"❌ Error editing image: {str(e)}"
        return None, error_message

# Create Gradio interface
with gr.Blocks(title="AI Image Generator & Editor") as app:
    gr.Markdown("# 🎨 AI Image Generator & Editor")
    gr.Markdown("Generate new images from text prompts or edit existing images using OpenAI's image models.")
    
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
            
            gen_button.click(
                fn=generate_image,
                inputs=[gen_prompt],
                outputs=[gen_output_image, gen_status]
            )
        
        # Image Editing Tab
        with gr.Tab("✏️ Edit Image"):
            gr.Markdown("### Edit an existing image with a text prompt")
            
            with gr.Row():
                with gr.Column():
                    edit_input_image = gr.Image(
                        label="Upload image to edit",
                        type="pil"
                    )
                    edit_prompt = gr.Textbox(
                        label="Describe your edits",
                        placeholder="Describe how you want to modify the image...",
                        lines=3
                    )
                    edit_mask = gr.Image(
                        label="Upload mask (optional)",
                        type="pil"
                    )
                    gr.Markdown("💡 **Mask tip:** Upload a black & white image where white areas will be edited.")
                    edit_button = gr.Button("Edit Image", variant="primary")
                
                with gr.Column():
                    edit_output_image = gr.Image(label="Edited Image", type="pil")
                    edit_status = gr.Textbox(label="Status", interactive=False)
            
            edit_button.click(
                fn=edit_image,
                inputs=[edit_input_image, edit_prompt, edit_mask],
                outputs=[edit_output_image, edit_status]
            )
    
    gr.Markdown("---")
    gr.Markdown("💾 All generated and edited images are automatically saved to the `output/` folder.")

if __name__ == "__main__":
    # Read configuration from environment variables
    port = int(os.environ.get("APP_PORT", 7860))
    debug = os.environ.get("APP_DEBUG", "False").lower() == "true"
    
    app.launch(
        server_name="0.0.0.0",  # Listen on all interfaces
        server_port=port,
        share=False,  # Set to True if you want a public link
        debug=debug
    )
