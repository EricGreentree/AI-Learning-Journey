import os
import shutil

FOLDER = "."  # current folder
LOG_FILE = "organizer_log.txt"

def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")
    print(message)

def is_image(filename):
    return filename.lower().endswith((".jpg", ".jpeg", ".png"))

def main():
    files = os.listdir(FOLDER)

    for filename in files:
                # Skip folders and this script
        if os.path.isdir(filename):
            continue

        if filename in ("organizer.py", LOG_FILE):
            continue

                # Create target directories
        image_dir = "images"
        other_dir = "other_files"

        # Create folders if they don't exist
        os.makedirs(image_dir, exist_ok=True)
        os.makedirs(other_dir, exist_ok=True)
        if is_image(filename):
            target = os.path.join(image_dir, filename)
            source = os.path.join(FOLDER, filename)
            shutil.move(source, target)
            log(f"Moved image: {filename} → images/")
        else:
            target = os.path.join(other_dir, filename)
            source = os.path.join(FOLDER, filename)
            shutil.move(source, target)
            log(f"Moved file: {filename} → other_files/")


        if filename in ("organizer.py", LOG_FILE):
            continue
            
        # We will fill in the logic here
        pass

if __name__ == "__main__":
    main()
