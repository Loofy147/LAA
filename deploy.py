
import os
import sys
from huggingface_hub import HfApi, login, whoami

# --- Configuration ---
REPO_NAME = "laa-algorithms-demo"
FILES_TO_UPLOAD = [
    "app.py",
    "requirements.txt",
    "laa_core/src/lib.rs",
    "laa_core/Cargo.toml",
    "laa_core/Cargo.lock",
    "README.md"
]

def get_hf_token():
    """Gets the Hugging Face token from an environment variable."""
    token = os.getenv("HF_TOKEN")
    if not token:
        print("Error: HF_TOKEN environment variable not set.")
        print("Please set the HF_TOKEN environment variable with your Hugging Face API token.")
        sys.exit(1)
    return token

def deploy_to_hf_spaces(token):
    """Logs in to Hugging Face, creates a new Space, and uploads the application files."""
    print("--- Logging in to Hugging Face Hub ---")
    login(token=token)

    try:
        user_info = whoami()
        hf_username = user_info['name']
    except Exception as e:
        print(f"Could not determine Hugging Face username: {e}")
        return

    api = HfApi()

    repo_id = f"{hf_username}/{REPO_NAME}"
    print(f"--- Creating new Space: {repo_id} ---")
    api.create_repo(
        repo_id=repo_id,
        repo_type="space",
        space_sdk="gradio",
        exist_ok=True,
    )

    print("--- Uploading files to the Space ---")
    for file_path in FILES_TO_UPLOAD:
        if os.path.exists(file_path):
            print(f"Uploading {file_path}...")
            api.upload_file(
                path_or_fileobj=file_path,
                path_in_repo=file_path,
                repo_id=repo_id,
                repo_type="space",
            )
        else:
            print(f"Warning: {file_path} not found, skipping.")

    print("\n--- Deployment script finished ---")
    print(f"Check the status of your Space here: https://huggingface.co/spaces/{hf_username}/{REPO_NAME}")

if __name__ == "__main__":
    hf_token = get_hf_token()
    deploy_to_hf_spaces(hf_token)
