# Tech Context: Gradio Image Generation and Editing App

## 1. Technologies Used

*   **Programming Language:** Python (version 3.8+ recommended for broad compatibility with libraries)
*   **UI Framework:** Gradio
    *   *Purpose:* Rapidly create web-based UIs for machine learning models and Python scripts.
    *   *Key Features Utilized:* `gr.Blocks` for custom layouts, `gr.Tab` for separate pages, `gr.Textbox`, `gr.Image`, `gr.Button`, input/output binding.
*   **AI Service:** OpenAI API
    *   *Models:* Primarily `gpt-image-1`. DALL·E 2/3 via Image API are alternatives if `gpt-image-1` presents issues or for specific features like variations (DALL·E 2 only).
    *   *Endpoints (Initial Focus):*
        *   Image Generations: `POST /v1/images/generations`
        *   Image Edits: `POST /v1/images/edits` (handles both full edits and inpainting with a mask)
*   **Python Libraries:**
    *   `openai`: Official Python client library for the OpenAI API.
    *   `gradio`: For building the web interface.
    *   `Pillow` (Python Imaging Library): May be needed for more advanced image manipulation if Gradio's built-in handling or OpenAI's direct byte/base64 responses are insufficient (e.g., creating masks programmatically, format conversions not handled by Gradio/OpenAI).
    *   `python-dotenv` (optional, for local development): To load environment variables like `OPENAI_API_KEY` from a `.env` file outside of Docker.
*   **Containerization:** Docker with Docker Compose
    *   *Purpose:* Package the application and its dependencies into a portable container.
    *   *Components:* `Dockerfile` to define the image build process, `docker-compose.yml` for orchestration, `.env` for environment variables.
*   **Version Control:** Git (assumed, standard practice)

## 2. Development Setup

*   **Local Environment (Pre-Docker):**
    1.  Python 3.8+ installed.
    2.  Virtual environment (e.g., `venv`) created and activated.
    3.  Dependencies installed via `pip install -r requirements.txt`.
    4.  `OPENAI_API_KEY` set as an environment variable (e.g., in `.env` file loaded by `python-dotenv`, or exported in the shell).
    5.  Run the Gradio app: `python app.py`.
*   **Dockerized Environment (Docker Compose - Recommended):**
    1.  Docker Desktop (or Docker Engine on Linux) installed.
    2.  Project files (`app.py`, `Dockerfile`, `docker-compose.yml`, `.env`, `requirements.txt`) in a directory.
    3.  Set up environment variables in `.env` file with your OpenAI API key.
    4.  Run with Docker Compose: `docker-compose up --build`
    5.  Stop with: `docker-compose down`
*   **Alternative Dockerized Environment (Manual Docker):**
    1.  Build the Docker image: `docker build -t gradio-image-app .`
    2.  Run the Docker container: `docker run -p 7860:7860 --env-file .env --rm -v "$(pwd)/output:/app/output" gradio-image-app`
        *   `-p 7860:7860`: Maps port 7860 on the host to port 7860 in the container.
        *   `--env-file .env`: Loads environment variables from the .env file.
        *   `--rm`: Automatically removes the container when it exits.
        *   `-v "$(pwd)/output:/app/output"`: Mounts local output directory for persistent storage.

## 3. Technical Constraints & Considerations

*   **OpenAI API Key:**
    *   A valid OpenAI API key with sufficient credits is required.
    *   The key must be kept secure and not hardcoded into the source code. Environment variables are the standard approach.
*   **OpenAI API Rate Limits & Quotas:**
    *   The application should be mindful of API rate limits. While a simple app for single users is unlikely to hit them frequently, error handling should account for this.
    *   Cost: Image generation, especially with `gpt-image-1` and high quality/resolution, can incur costs. Users should be aware.
*   **Image Formats & Sizes:**
    *   OpenAI API has specific requirements for input image formats (e.g., PNG for masks) and sizes.
    *   Output images are typically returned as base64 encoded strings or URLs. The app will handle base64 and save as PNG/JPEG.
    *   Gradio's `gr.Image` component handles various input/output types.
*   **Masks for Inpainting:**
    *   Masks must be RGBA PNG files where the transparent area indicates the region to edit.
    *   The documentation provides Python code using Pillow to convert B&W masks to the required RGBA format. This logic might need to be integrated if users are expected to upload simple B&W masks.
*   **Streaming:**
    *   The user expressed interest but deprioritized it due to potential complexity.
    *   The Image API (chosen for initial simplicity) does not support streaming.
    *   The Responses API supports streaming but is more complex to integrate and currently only supports `gpt-image-1` for image generation (not edits directly in the same way as the Image API's edit endpoint). If streaming becomes a priority, a shift to the Responses API would be necessary, potentially impacting the editing workflow.
*   **Latency:**
    *   Image generation can take time (up to 2 minutes for complex prompts with `gpt-image-1` as per docs).
    *   The Gradio UI should provide clear feedback (e.g., loading indicators) during these operations.
*   **Dependencies:**
    *   Keep the `requirements.txt` file updated with all necessary Python packages and their versions.
*   **Docker Image Size:**
    *   Aim for a reasonably sized Docker image by using an appropriate base image (e.g., `python:3.9-slim`) and efficient Dockerfile layering.

## 4. Dependencies (`requirements.txt`)

```
openai>=1.0.0
gradio>=4.0.0
Pillow>=9.0.0
python-dotenv>=0.19.0
```

## 5. Environment Configuration (`.env`)

```
OPENAI_API_KEY=your_openai_api_key_here
APP_PORT=7860
APP_DEBUG=False
```

## 6. Docker Compose Configuration (`docker-compose.yml`)

```yaml
version: '3.8'
services:
  gradio-image-app:
    build: .
    container_name: gradio-image-app
    ports:
      - "${APP_PORT}:${APP_PORT}"
    env_file:
      - .env
    volumes:
      - ./output:/app/output
    restart: unless-stopped
    environment:
      - GRADIO_SERVER_NAME=0.0.0.0
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - APP_PORT=${APP_PORT}
      - APP_DEBUG=${APP_DEBUG}
```

**Key Features:**
- Dynamic port mapping using `${APP_PORT}` from .env file
- Explicit environment variable declaration for clarity
- Environment variables are loaded from .env file and explicitly passed to container
- All configuration values are externalized and configurable

## 7. Tool Usage Patterns

*   **OpenAI Client Initialization:**
    ```python
    from openai import OpenAI
    import os

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    ```
*   **Image Generation (Image API):**
    ```python
    response = client.images.generate(
        model="gpt-image-1", # or "dall-e-3"
        prompt="A cute cat playing with a ball of yarn",
        n=1,
        size="1024x1024", # or other supported sizes
        response_format="b64_json" # To get base64 encoded image data
    )
    image_b64 = response.data[0].b64_json
    # Decode base64 and save/display
    ```
*   **Image Editing (Image API):**
    ```python
    # Assuming 'image_bytes' is the original image file read as bytes
    # Assuming 'mask_bytes' (optional) is the mask file read as bytes
    response = client.images.edit(
        model="gpt-image-1",
        image=image_bytes, # e.g., open("input.png", "rb")
        mask=mask_bytes,   # e.g., open("mask.png", "rb"), optional
        prompt="Add a party hat to the subject",
        n=1,
        size="1024x1024",
        response_format="b64_json"
    )
    edited_image_b64 = response.data[0].b64_json
    # Decode base64 and save/display
    ```
*   **Saving Base64 Image:**
    ```python
    import base64
    from datetime import datetime

    def save_image_from_b64(b64_string, filename_prefix="generated"):
        img_data = base64.b64decode(b64_string)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Ensure output directory exists
        os.makedirs("output", exist_ok=True)
        filepath = os.path.join("output", f"{filename_prefix}_{timestamp}.png")
        with open(filepath, "wb") as f:
            f.write(img_data)
        return filepath
