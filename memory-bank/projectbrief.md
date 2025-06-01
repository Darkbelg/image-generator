# Project Brief: Gradio Image Generation and Editing App

## 1. Project Overview

The goal is to develop a Gradio application that allows users to generate and edit images using the OpenAI API. The application should provide a user-friendly interface with distinct sections for image generation and image editing. All generated or edited images will be stored in a local `output` folder. The development environment will be containerized using Docker for portability and ease of setup.

## 2. Core Requirements

*   **Gradio Interface:**
    *   Separate pages/tabs for "Image Generation" and "Image Editing".
*   **Image Generation:**
    *   User inputs a text prompt.
    *   Application calls the OpenAI API to generate an image based on the prompt.
    *   The generated image is displayed to the user.
    *   The generated image is saved to an `output/` directory.
*   **Image Editing:**
    *   User uploads an existing image.
    *   User inputs a text prompt to describe the desired edits.
    *   (Optional) User can provide a mask for inpainting.
    *   Application calls the OpenAI API to edit the image.
    *   The edited image is displayed to the user.
    *   The edited image is saved to the `output/` directory.
*   **OpenAI API Integration:**
    *   Utilize appropriate OpenAI API endpoints for image generation and editing (e.g., `gpt-image-1` model via Image API or Responses API).
    *   Handle API responses and errors gracefully.
*   **Image Storage:**
    *   All generated and edited images must be saved locally in an `output/` folder within the project.
*   **Dockerization:**
    *   The application and its dependencies must be containerized using Docker.
    *   A `Dockerfile` must be provided to build the application image.
*   **Technology Stack (Initial Thoughts):**
    *   Python
    *   Gradio (for UI)
    *   OpenAI Python SDK
    *   Docker

## 3. Key Considerations & Decisions

*   **API Choice:**
    *   The user mentioned "streaming would be a plus but if it adds complexity leave it."
    *   The documentation indicates the **Image API** is suitable for single image generation/editing from one prompt, while the **Responses API** is better for conversational experiences and streaming.
    *   **Initial Decision:** Start with the **Image API** for simplicity, focusing on `gpt-image-1` model. Streaming can be considered a future enhancement if the Image API proves too limiting or if the user re-prioritizes it.
*   **Model Choice:** `gpt-image-1` is preferred due to its advanced capabilities.
*   **User Experience:** The interface should be intuitive, clearly separating the generation and editing functionalities.

## 4. Scope

*   **In Scope:**
    *   Basic image generation from text.
    *   Basic image editing from an uploaded image and text prompt.
    *   Saving images to a local folder.
    *   Docker setup for the development environment.
    *   Creation of Memory Bank files to document the project.
*   **Out of Scope (Initially, unless complexity is low):**
    *   Advanced multi-turn conversational editing (might require Responses API).
    *   Real-time streaming of image generation (might require Responses API).
    *   User authentication or accounts.
    *   Cloud storage for images.
    *   Image variations (DALL·E 2 specific feature).

## 5. Success Criteria

*   A functional Gradio application that meets all core requirements.
*   Users can successfully generate images from text prompts.
*   Users can successfully edit uploaded images using text prompts.
*   Generated/edited images are saved correctly.
*   The application can be built and run using Docker.
*   The Memory Bank is initialized and contains relevant project information.
