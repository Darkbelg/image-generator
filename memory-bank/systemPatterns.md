# System Patterns: Gradio Image Generation and Editing App

## 1. System Architecture Overview

The application will follow a simple client-server architecture, containerized by Docker.

*   **Client:** The user's web browser, interacting with the Gradio interface.
*   **Server:** A Python backend powered by Gradio. This backend will:
    *   Serve the Gradio UI components.
    *   Handle user inputs (prompts, image uploads).
    *   Communicate with the OpenAI API for image generation and editing.
    *   Process API responses.
    *   Save images to the local filesystem.
*   **OpenAI API:** External service providing the core image generation/editing intelligence.
*   **Docker Container:** Encapsulates the Python/Gradio server and all its dependencies, ensuring a consistent runtime environment.

```mermaid
graph TD
    User[User's Web Browser] -- HTTP/WebSocket --> GradioApp[Gradio Application (Python Backend)]
    GradioApp -- API Calls --> OpenAI[OpenAI API]
    GradioApp -- File I/O --> OutputFolder[output/ Folder on Disk]
    Docker[Docker Container] -->|Wraps| GradioApp
    Docker -->|Manages| OutputFolder
```

## 2. Key Technical Decisions

*   **UI Framework:** **Gradio**
    *   *Reasoning:* Chosen for its simplicity in creating web UIs for machine learning models with Python. It handles much of the frontend complexity, allowing focus on backend logic. The user specifically requested a Gradio app.
*   **Backend Language:** **Python**
    *   *Reasoning:* Gradio is Python-based, and the OpenAI API has a well-supported Python SDK. It's a natural fit for this type of application.
*   **OpenAI API Interaction:** **OpenAI Python SDK**
    *   *Reasoning:* Provides a convenient and official way to interact with the OpenAI API, simplifying requests and response handling.
*   **API Endpoint Choice (Initial):** **Image API** (specifically `images.generate` and `images.edit` endpoints)
    *   *Reasoning:* As per `projectbrief.md`, this is simpler for single-prompt generation/editing. The `gpt-image-1` model will be prioritized. The Responses API (for streaming/multi-turn) is a potential future enhancement.
*   **Image Storage:** **Local Filesystem (`output/` directory)**
    *   *Reasoning:* Simple, direct, and meets the user's requirement. No need for database or cloud storage complexity for this project's scope.
*   **Containerization:** **Docker**
    *   *Reasoning:* Ensures a reproducible and portable development and runtime environment, simplifying dependency management and deployment.
*   **Concurrency Model (Gradio):** Gradio handles concurrent users by default, typically using threads. For long-running tasks like API calls, ensure functions are defined appropriately so they don't block the main Gradio event loop if possible (Gradio often handles this well for I/O bound operations).

## 3. Design Patterns & Approaches

*   **Modular Functions:**
    *   Separate Python functions will be created for:
        *   `generate_image(prompt, api_key, ...)`
        *   `edit_image(input_image, prompt, mask_image, api_key, ...)`
        *   `save_image(image_data, base_filename)`
    *   These functions will be called by the Gradio interface handlers.
*   **Configuration Management:**
    *   The OpenAI API key should not be hardcoded. It will be managed via an environment variable (`OPENAI_API_KEY`) that is passed into the Docker container at runtime.
    *   Other configurations (e.g., default model, output directory) can be constants or configurable at the top of the main script.
*   **Error Handling:**
    *   API calls will be wrapped in `try-except` blocks to catch potential network issues, API errors (e.g., rate limits, invalid prompts), or issues with image processing.
    *   User-friendly error messages will be displayed in the Gradio interface.
*   **State Management (Gradio):**
    *   Gradio components can hold state. For example, an `gr.Image` component will display the uploaded or generated image.
    *   For more complex state across interactions, Gradio's `gr.State` can be used if necessary, but the initial design aims for stateless operations per tab as much as possible.
*   **Input Validation:**
    *   Basic checks for empty prompts.
    *   Gradio's upload components handle file type validation to some extent.
*   **File Naming Convention:**
    *   Generated/edited images saved to the `output/` folder will use a consistent naming scheme, e.g., `generated_YYYYMMDD_HHMMSS.png` or `edited_YYYYMMDD_HHMMSS.png` to ensure uniqueness and provide some temporal context.

## 4. Component Relationships

*   **`app.py` (Main Application File):**
    *   Initializes the OpenAI client.
    *   Defines the core logic functions (generate, edit, save).
    *   Constructs the Gradio interface (`gr.Blocks` or `gr.Interface`).
        *   **Generation Tab:** `gr.Textbox` for prompt, `gr.Button` to trigger generation, `gr.Image` to display output.
        *   **Editing Tab:** `gr.Image` for upload, `gr.Textbox` for edit prompt, (optional `gr.Image` for mask), `gr.Button` to trigger edit, `gr.Image` to display output.
    *   Launches the Gradio app.
*   **`Dockerfile`:**
    *   Specifies the base Python image.
    *   Copies application code (`app.py`, `requirements.txt`).
    *   Installs dependencies from `requirements.txt`.
    *   Sets the `OPENAI_API_KEY` environment variable (to be provided at `docker run`).
    *   Defines the command to run the Gradio application.
*   **`requirements.txt`:**
    *   Lists Python dependencies (e.g., `gradio`, `openai`, `Pillow` for image handling if needed beyond base64).
*   **`output/` directory:**
    *   Created by the application (or Dockerfile) to store output images.

## 5. Critical Implementation Paths

1.  **Setting up the Basic Gradio App:** Create a minimal Gradio app with two tabs.
2.  **OpenAI API Key Management:** Securely pass and use the API key.
3.  **Image Generation Functionality:**
    *   Implement `generate_image` function.
    *   Connect to Gradio input (prompt) and output (image display).
    *   Implement image saving.
4.  **Image Editing Functionality:**
    *   Implement `edit_image` function (handling image upload, prompt, optional mask).
    *   Connect to Gradio inputs and outputs.
    *   Implement image saving.
5.  **Dockerization:**
    *   Create `Dockerfile`.
    *   Create `requirements.txt`.
    *   Ensure the app runs correctly within a Docker container.
    *   Address volume mapping for the `output/` folder for persistence.
6.  **Error Handling and UX Refinements:** Implement robust error handling and user feedback mechanisms.
