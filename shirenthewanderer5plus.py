import os
import shutil
from datetime import datetime
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get environment variables from the .env file
steam_userid = os.getenv("STEAM_USERID", "")
shirenthewanderer5plus_save_data_folder = os.getenv("SHIRENTHEWANDERER5PLUS_SAVE_DATA_FOLDER", "")

# Construct the backup folder path
backup_base_path = f"C:/Program Files (x86)/Steam/userdata/{steam_userid}/{shirenthewanderer5plus_save_data_folder}/remote"
parent_dir = os.path.dirname(backup_base_path)  # Parent directory of "remote"

def list_zip_files():
    """List all ZIP files in the parent directory."""
    zip_files = [f for f in os.listdir(parent_dir) if f.endswith('.zip')]
    if not zip_files:
        print("No ZIP files found.")
        return

    print("ZIP files:")
    for idx, zip_file in enumerate(zip_files, start=1):
        print(f"{idx}. {zip_file}")

def backup_folder(comment=""):
    # Get the current date and time in the format YYYY-MM-DD-hh-mm
    current_time = datetime.now().strftime("%Y-%m-%d-%H-%M")

    # Add the comment to the filename if provided
    backup_filename = f"remote_{current_time}_{comment}.zip" if comment else f"remote_{current_time}.zip"

    # Set the path for the zip file (created in the same directory as "remote")
    zip_path = os.path.join(parent_dir, backup_filename)

    # Compress files and subdirectories inside the "remote" folder
    shutil.make_archive(zip_path.replace(".zip", ""), 'zip', backup_base_path)

    print(f"Backup completed: {zip_path}")

def restore_folder():
    # List ZIP files in the backup base path
    zip_files = [f for f in os.listdir(parent_dir) if f.endswith('.zip')]

    if not zip_files:
        print("No ZIP files found for restoration.")
        return

    print("Please select a ZIP file to restore:")

    # Display files with numbers
    for idx, zip_file in enumerate(zip_files, start=1):
        print(f"{idx}. {zip_file}")

    # Prompt the user to select a file
    choice = input("Enter the number: ").strip()

    # Exit the program if `q` is entered
    if choice.lower() == 'q':
        print("Exiting the program.")
        exit()

    # Check if the input is a valid number
    try:
        choice_idx = int(choice) - 1
        if choice_idx < 0 or choice_idx >= len(zip_files):
            raise ValueError("Invalid number entered.")
    except ValueError:
        print("Invalid input.")
        return

    # Get the path of the selected ZIP file
    selected_zip_file = zip_files[choice_idx]
    zip_path = os.path.join(parent_dir, selected_zip_file)

    # Check if the restore folder exists
    if os.path.exists(backup_base_path):
        # If the folder exists, confirm overwriting
        confirm = input(f"{backup_base_path} already exists. Do you want to overwrite it? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Restoration canceled.")
            return
        # Delete contents of the folder
        for root, dirs, files in os.walk(backup_base_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    # Extract the ZIP file to restore it to the original location
    shutil.unpack_archive(zip_path, backup_base_path)
    print(f"Restoration completed: {backup_base_path}")

def main():
    while True:
        # Prompt the user to select an action
        action = input("Select Backup (b), Restore (r), List ZIPs (l), or Quit (q): ").strip().lower()

        if action == 'q':
            print("Exiting the program.")
            break
        elif action == 'b':
            comment = input("Enter a comment for the backup: ").strip()
            backup_folder(comment)
        elif action == 'r':
            restore_folder()
        elif action == 'l':
            list_zip_files()
        else:
            print("Invalid choice. Please select 'b', 'r', 'l', or 'q'.")

# Execute
if __name__ == "__main__":
    main()