import os
import shutil
import datetime
from transformers import pipeline

# Load transformer model for zero-shot classification
classifier = pipeline("zero-shot-classification")

# Candidate file system actions
LABELS = ["move files", "delete files", "sort by date", "rename files", "copy files"]

# Get user command
user_input = input("What do you want to do with your files?\n> ")

# Classify intent
result = classifier(user_input, LABELS)
top_action = result['labels'][0]
print(f"\n🧠 Detected Action: {top_action}\n")

# Base folder (you can modify this)
BASE_PATH = os.path.expanduser("~/Downloads")

# Logic based on action
def move_files(extension, target_folder):
    os.makedirs(target_folder, exist_ok=True)
    for file in os.listdir(BASE_PATH):
        if file.endswith(extension):
            shutil.move(os.path.join(BASE_PATH, file), os.path.join(target_folder, file))
            print(f"Moved: {file}")

def delete_temp_files():
    for file in os.listdir(BASE_PATH):
        if file.endswith((".tmp", ".temp", ".log")):
            os.remove(os.path.join(BASE_PATH, file))
            print(f"Deleted: {file}")

def sort_by_date():
    for file in os.listdir(BASE_PATH):
        path = os.path.join(BASE_PATH, file)
        if os.path.isfile(path):
            ctime = os.path.getctime(path)
            date_folder = datetime.datetime.fromtimestamp(ctime).strftime('%Y-%m-%d')
            target = os.path.join(BASE_PATH, date_folder)
            os.makedirs(target, exist_ok=True)
            shutil.move(path, os.path.join(target, file))
            print(f"Moved {file} to {date_folder}/")

# Run based on detected action
if "move" in top_action:
    if "pdf" in user_input:
        move_files(".pdf", os.path.join(BASE_PATH, "Documents"))
    elif "images" in user_input:
        move_files(".jpg", os.path.join(BASE_PATH, "Images"))
    else:
        print("❓Please specify file type to move (e.g., PDFs, images).")

elif "delete" in top_action:
    delete_temp_files()

elif "sort" in top_action:
    sort_by_date()

else:
    print("⚠️ Sorry, this action is not yet supported.")

