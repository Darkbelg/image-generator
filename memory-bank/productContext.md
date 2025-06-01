# Product Context: Gradio Image Generation and Editing App

## 1. Why This Project Exists

This project aims to provide a simple, accessible, and self-contained tool for individuals to experiment with OpenAI's image generation and editing capabilities. Many users may find direct API interaction or complex software installations daunting. This Gradio application will offer a user-friendly graphical interface, lowering the barrier to entry for exploring AI-powered image creation.

The containerized Docker environment ensures that the application can be easily set up and run across different systems without complex dependency management, making it ideal for quick experimentation, learning, or small-scale personal projects.

## 2. Problems It Solves

*   **Accessibility:** Provides an easy-to-use GUI for OpenAI image models, removing the need for users to write code or use command-line interfaces directly.
*   **Simplified Workflow:** Streamlines the process of generating an image from a text prompt and performing basic edits on existing images.
*   **Reproducibility & Portability:** Dockerization allows the application to run consistently in various environments, simplifying setup and sharing.
*   **Focused Functionality:** Offers core image generation and editing features without the complexity of larger, multi-purpose image editing suites.
*   **Local Image Management:** Saves all generated/edited images to a local `output` folder, giving users direct access and control over their creations.

## 3. How It Should Work (User's Perspective)

The user will interact with a web-based Gradio interface.

*   **Main Interface:**
    *   The application will present two main sections, likely as tabs: "Generate Image" and "Edit Image".

*   **"Generate Image" Section:**
    1.  The user sees a text input field labeled "Enter your prompt:".
    2.  The user types a description of the image they want to create (e.g., "A futuristic cityscape at sunset").
    3.  (Optional) The user might have simple controls for image size or quality if implemented.
    4.  The user clicks a "Generate" button.
    5.  The application displays a loading indicator while the image is being generated.
    6.  Once complete, the generated image is displayed directly in the interface.
    7.  A message confirms that the image has also been saved to the `output/` folder (e.g., "Image saved as output/image_timestamp.png").

*   **"Edit Image" Section:**
    1.  The user sees an image upload component (e.g., "Upload your image:").
    2.  The user uploads an image from their local system. The uploaded image is displayed.
    3.  The user sees a text input field labeled "Describe your edits:" (e.g., "Make the sky blue" or "Add a cat to the scene").
    4.  (Optional, for inpainting) If inpainting is implemented, the user might see an option to upload a mask image or draw a mask directly on the uploaded image.
    5.  The user clicks an "Edit Image" button.
    6.  The application displays a loading indicator.
    7.  Once complete, the edited image is displayed.
    8.  A message confirms that the edited image has also been saved to the `output/` folder.

*   **Image Saving:**
    *   All images (generated or edited) are automatically saved to a local `output` directory within the project structure. Filenames could be timestamp-based or derived from prompts to ensure uniqueness.

*   **Docker Usage (Developer/Advanced User):**
    1.  The user clones the project repository.
    2.  The user builds the Docker image using the provided `Dockerfile` (e.g., `docker build -t image-app .`).
    3.  The user runs the Docker container, mapping necessary ports (e.g., `docker run -p 7860:7860 image-app`).
    4.  The user accesses the Gradio app via their web browser (e.g., `http://localhost:7860`).
    5.  The `output` folder within the container should ideally be mapped to a local directory on the host machine for persistent storage of images if the container is removed.

## 4. User Experience (UX) Goals

*   **Simplicity:** The interface should be clean, intuitive, and require minimal learning.
*   **Clarity:** Clear separation between image generation and editing functionalities.
*   **Responsiveness:** The application should provide feedback during long operations (e.g., loading indicators).
*   **Directness:** Users should be able to achieve their primary goals (generate/edit images) with a few clicks and minimal configuration.
*   **Reliability:** The application should handle API interactions gracefully and provide informative error messages if something goes wrong.
*   **Self-Contained:** Users should feel they have everything they need within the app for basic image tasks, with easy access to their output.
