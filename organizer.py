import os
import shutil
import sys
import argparse

LOG_FILE = "organizer_log.txt"

def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")
    print(message)

def is_image(filename):
    return filename.lower().endswith((".jpg", ".jpeg", ".png"))

def main(folder, dry_run=False):
    files = os.listdir(folder)

    for filename in files:
        full_path = os.path.join(folder, filename)

        # Skip directories
        if os.path.isdir(full_path):
            continue

        # Skip this script and log file
        if filename in ("organizer.py", LOG_FILE):
            continue

        # Target directories inside the same folder
        image_dir = os.path.join(folder, "images")
        other_dir = os.path.join(folder, "other_files")

        os.makedirs(image_dir, exist_ok=True)
        os.makedirs(other_dir, exist_ok=True)

        if is_image(filename):
            source = full_path
            target = os.path.join(image_dir, filename)
            if dry_run:
                log(f"[DRY RUN] Would move image: {filename} → images/")
            else:
                shutil.move(source, target)
                log(f"Moved image: {filename} → images/")
        else:
            source = full_path
            target = os.path.join(other_dir, filename)
            if dry_run:
                log(f"[DRY RUN] Would move file: {filename} → other_files/")
            else:
                shutil.move(source, target)
                log(f"Moved file: {filename} → other_files/")

if __name__ == "__main__":
    # Use argparse for robust CLI parsing
    parser = argparse.ArgumentParser(description="Organize files in a folder into images/ and other_files/.")
    parser.add_argument(
        "folder",
        nargs="?",
        default=".",
        help="Folder to organize (default: current directory).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without moving any files.",
    )

    args = parser.parse_args()

    # Expand ~ to full path (e.g., ~/Desktop → /Users/you/Desktop)
    folder = os.path.expanduser(args.folder)
    dry_run = args.dry_run

    if not os.path.isdir(folder):
        print(f"Error: {folder} is not a valid directory.")
        sys.exit(1)

    log(f"Starting organizer on folder: {folder} (dry_run={dry_run})")
    main(folder, dry_run=dry_run)
    log("Organizer finished.")
