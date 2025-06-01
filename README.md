# AI Image Generator & Editor

A Gradio-based web application for generating and editing images using OpenAI's image models. The app provides separate interfaces for image generation and editing, with all output images automatically saved to a local `output/` folder.

## Features

- **Image Generation**: Generate new images from text prompts using OpenAI's `gpt-image-1` model
- **Image Editing**: Edit existing images with text prompts and optional masks for inpainting
- **Local Storage**: All generated and edited images are automatically saved to the `output/` folder
- **Docker Support**: Fully containerized for easy deployment and portability
- **User-Friendly Interface**: Clean Gradio web interface with separate tabs for generation and editing

## Prerequisites

- Docker installed on your system
- OpenAI API key with access to image generation models

## Quick Start with Docker

1. **Clone or download this project**

2. **Build the Docker image:**
   ```bash
   docker build -t gradio-image-app .
   ```

3. **Run the container:**
   ```bash
   docker run -p 7860:7860 -e OPENAI_API_KEY="your-api-key-here" --rm -v "$(pwd)/output:/app/output" gradio-image-app
   ```

   Replace `your-api-key-here` with your actual OpenAI API key.

4. **Access the application:**
   Open your web browser and go to `http://localhost:7860`

## Docker Run Command Explanation

- `-p 7860:7860`: Maps port 7860 on your host to port 7860 in the container (Gradio's default port)
- `-e OPENAI_API_KEY="your-api-key-here"`: Passes your OpenAI API key as an environment variable
- `--rm`: Automatically removes the container when it exits
- `-v "$(pwd)/output:/app/output"`: Mounts your local `output` directory to the container's output directory for persistent image storage

## Local Development (without Docker)

If you prefer to run the application locally without Docker:

1. **Install Python 3.8+ and create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your OpenAI API key:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the application:**
   Open your web browser and go to `http://localhost:7860`

## Usage

### Image Generation
1. Navigate to the "Generate Image" tab
2. Enter a descriptive text prompt
3. Click "Generate Image"
4. The generated image will be displayed and automatically saved to the `output/` folder

### Image Editing
1. Navigate to the "Edit Image" tab
2. Upload an image you want to edit
3. Enter a text prompt describing the desired changes
4. (Optional) Upload a mask image for inpainting - white areas in the mask will be edited
5. Click "Edit Image"
6. The edited image will be displayed and automatically saved to the `output/` folder

## File Structure

```
.
├── app.py              # Main Gradio application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── README.md          # This file
├── memory-bank/       # Project documentation
└── output/           # Generated/edited images (created automatically)
```

## Technical Details

- **Framework**: Gradio for the web interface
- **AI Model**: OpenAI's `gpt-image-1` via the Image API
- **Image Format**: PNG (1024x1024 pixels)
- **Storage**: Local filesystem in the `output/` directory
- **Containerization**: Docker with Python 3.9 slim base image

## Troubleshooting

- **API Key Issues**: Ensure your OpenAI API key is valid and has sufficient credits
- **Port Conflicts**: If port 7860 is in use, change the port mapping: `-p 8080:7860`
- **Permission Issues**: Ensure the `output/` directory is writable
- **Memory Issues**: Image generation can be memory-intensive; ensure adequate system resources

## Memory Bank

This project uses a Memory Bank system for documentation. See the `memory-bank/` directory for detailed project documentation including:
- Project brief and requirements
- Technical architecture and patterns
- Development progress tracking
