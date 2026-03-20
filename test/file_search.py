import os

def suche_dateien(root_path, suchbegriffe):
    for current_path, dirs, files in os.walk(root_path):
        for file in files:
            if any(such in file for such in suchbegriffe):
                print(os.path.abspath(os.path.join(current_path, file)))
                break


root = r"Y:"
suchbegriffe = ["IMG_1532.HEIC"]
suche_dateien(root, suchbegriffe)
