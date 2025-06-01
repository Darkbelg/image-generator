import os
import base64
import gradio as gr
from datetime import datetime
from openai import OpenAI
from PIL import Image
import io

# Ensure output and input directories exist
os.makedirs("output", exist_ok=True)
os.makedirs("input", exist_ok=True)

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
def generate_image(prompt, background_style, quality, size):
    if not prompt or prompt.strip() == "":
        return None, "Please enter a prompt."
    
    try:
        # Build API parameters
        api_params = {
            "model": "gpt-image-1",
            "prompt": prompt,
            "n": 1,
            "moderation": "low",
        }
        
        # Add optional parameters if not "auto"
        if size != "auto":
            api_params["size"] = size
        if quality != "auto":
            api_params["quality"] = quality
        if background_style != "auto":
            api_params["background"] = background_style
        
        # Call OpenAI API
        response = client.images.generate(**api_params)
        
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

# Image editing function
def edit_image(uploaded_files, prompt, n_images, background_style, quality, size):
    if not uploaded_files or len(uploaded_files) == 0:
        return None, "Please upload at least one image."
    
    if not prompt or prompt.strip() == "":
        return None, "Please enter an edit prompt."
    
    # Check if we have too many files (API limit is 16)
    if len(uploaded_files) > 16:
        return None, "❌ Too many files uploaded. Maximum is 16 images."
    
    image_files_for_api = []
    
    try:
        # Prepare images for API
        for file_obj in uploaded_files:
            image_files_for_api.append(open(file_obj.name, "rb"))
        
        # Build API parameters
        api_params = {
            "model": "gpt-image-1",
            "image": image_files_for_api,
            "prompt": prompt,
            "n": n_images,
        }
        
        # Add optional parameters if not "auto"
        if size != "auto":
            api_params["size"] = size
        if quality != "auto":
            api_params["quality"] = quality
        if background_style != "auto":
            api_params["background"] = background_style
        
        # Call OpenAI API
        response = client.images.edit(**api_params)
        
        # Process response - handle multiple images
        pil_images_list = []
        saved_filepaths_list = []
        
        for i, image_data in enumerate(response.data):
            # Get base64 image data
            image_b64 = image_data.b64_json
            
            # Convert base64 to PIL Image
            img_data = base64.b64decode(image_b64)
            pil_image = Image.open(io.BytesIO(img_data))
            pil_images_list.append(pil_image)
            
            # Save image to output folder
            filepath = save_image_from_b64(image_b64, f"edited_{i+1}")
            saved_filepaths_list.append(filepath)
        
        # Create success message
        if len(saved_filepaths_list) == 1:
            status_msg = f"✅ Image edited successfully! Saved to: {saved_filepaths_list[0]}"
        else:
            status_msg = f"✅ {len(saved_filepaths_list)} images edited successfully! Saved to: {', '.join(saved_filepaths_list)}"
        
        return pil_images_list, status_msg
        
    except Exception as e:
        error_msg = f"❌ Error editing image: {str(e)}"
        return None, error_msg
    
    finally:
        # Close all opened files
        for file_obj in image_files_for_api:
            try:
                file_obj.close()
            except:
                pass

# Create Gradio interface
with gr.Blocks(title="AI Image Generator & Editor") as app:
    gr.Markdown("# 🎨 AI Image Generator & Editor")
    gr.Markdown("Generate and edit images using OpenAI's gpt-image-1 model.")
    
    with gr.Tab("🖼️ Generate Image"):
        gr.Markdown("### Generate a new image from a text description")
        
        with gr.Row():
            with gr.Column():
                gen_prompt = gr.Textbox(
                    label="Enter your prompt",
                    placeholder="Describe the image you want to generate...",
                    lines=3
                )
                
                # New input options for gpt-image-1
                gen_background_input = gr.Radio(
                    label="Background Style",
                    choices=["auto", "transparent", "opaque"],
                    value="auto",
                    info="Choose background handling for the generated image"
                )
                
                gen_quality_input = gr.Radio(
                    label="Image Quality",
                    choices=["auto", "high", "medium", "low"],
                    value="auto",
                    info="Select the quality level for image generation"
                )
                
                gen_size_input = gr.Radio(
                    label="Image Size",
                    choices=["auto", "1024x1024", "1536x1024", "1024x1536"],
                    value="auto",
                    info="Choose image dimensions (auto, square, landscape, portrait)"
                )
                
                gen_button = gr.Button("Generate Image", variant="primary")
            
            with gr.Column():
                gen_output_image = gr.Image(label="Generated Image", type="pil", interactive=False)
                gen_status = gr.Textbox(label="Status", interactive=False)
        
        gen_button.click(
            fn=generate_image,
            inputs=[gen_prompt, gen_background_input, gen_quality_input, gen_size_input],
            outputs=[gen_output_image, gen_status],
            show_api=False 
        )
    
    with gr.Tab("🎨 Edit Image"):
        gr.Markdown("### Edit existing images using a text prompt")
        
        with gr.Row():
            with gr.Column():
                edit_image_input = gr.File(
                    label="Upload Image(s) (PNG, JPG, WEBP - up to 16 files, <50MB each)",
                    file_count="multiple",
                    file_types=["image"]
                )
                
                edit_prompt_input = gr.Textbox(
                    label="Enter your edit prompt",
                    placeholder="Describe the changes you want to make...",
                    lines=3
                )
                
                edit_n_input = gr.Slider(
                    label="Number of Images to Generate",
                    minimum=1,
                    maximum=10,
                    step=1,
                    value=1,
                    info="Number of edited images to generate from the input"
                )
                
                edit_background_input = gr.Radio(
                    label="Background Style",
                    choices=["auto", "transparent", "opaque"],
                    value="auto",
                    info="Choose background handling for the edited image(s)"
                )
                
                edit_quality_input = gr.Radio(
                    label="Image Quality",
                    choices=["auto", "high", "medium", "low"],
                    value="auto",
                    info="Select the quality level for image editing"
                )
                
                edit_size_input = gr.Radio(
                    label="Image Size",
                    choices=["auto", "1024x1024", "1536x1024", "1024x1536"],
                    value="auto",
                    info="Choose image dimensions for edited image(s)"
                )
                
                edit_button = gr.Button("Edit Images", variant="primary")
            
            with gr.Column():
                edit_output_gallery = gr.Gallery(
                    label="Edited Images",
                    show_label=True,
                    elem_id="edit_gallery"
                )
                edit_status_output = gr.Textbox(label="Status", interactive=False)
        
        edit_button.click(
            fn=edit_image,
            inputs=[
                edit_image_input,
                edit_prompt_input,
                edit_n_input,
                edit_background_input,
                edit_quality_input,
                edit_size_input
            ],
            outputs=[edit_output_gallery, edit_status_output],
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
