import zipfile
import os

def add_folder_to_zip(zipf, folder, prefix=""):
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.join(prefix, os.path.relpath(file_path, folder))
            zipf.write(file_path, arcname)

with zipfile.ZipFile("lambda.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
    # dependencias
    add_folder_to_zip(zipf, "package", "")
    
    # codigo backend
    backend_files = ["main.py", "database.py", "models.py", "auth.py", "schemas.py"]
    for file in backend_files:
        zipf.write(f"backend/{file}", file)
    
    # routers
    add_folder_to_zip(zipf, "backend/routers", "routers")

print("lambda.zip created successfully")