import os

def check_eof(file_path):
    with open(file_path, 'rb') as f:
        f.seek(-20, os.SEEK_END)  # Seek to the last 20 bytes
        return b'%EOF' in f.read()

def check_and_remove_pdfs(folder_path):
    corrupted_pdfs = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                file_path = os.path.join(root, file)
                if not check_eof(file_path):
                    corrupted_pdfs.append(file_path)
                    os.remove(file_path)  # Remove the corrupted PDF
    return corrupted_pdfs

folder_path = './data/guidelines'
corrupted_pdfs = check_and_remove_pdfs(folder_path)

if corrupted_pdfs:
    print("Removed corrupted PDFs without EOF tag:")
    for pdf in corrupted_pdfs:
        print(pdf)
else:
    print("All PDFs have the EOF tag.")

