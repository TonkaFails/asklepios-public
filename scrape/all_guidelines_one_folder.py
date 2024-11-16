import os
import shutil

def find_and_copy_pdfs(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith('.pdf'):
                relative_path = os.path.relpath(root, source_folder)
                subfolder_parts = relative_path.split(os.sep)
                new_name = f"{'_'.join(subfolder_parts)}_{file}" if subfolder_parts else file
                source_file = os.path.join(root, file)
                destination_file = os.path.join(destination_folder, new_name)
                shutil.copy2(source_file, destination_file)

source_folder = './Leitlinien'
destination_folder = 'alle_Leitlinien'

find_and_copy_pdfs(source_folder, destination_folder)
