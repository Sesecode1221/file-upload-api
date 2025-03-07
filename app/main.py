from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
import os
from io import BytesIO
from tempfile import NamedTemporaryFile

app = FastAPI(title="Simple File Upload API")

# Define a directory to store uploaded files
UPLOAD_DIR = "/tmp/uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>File Upload</title>
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
      <div class="container mt-5">
        <h2 class="mb-4">Upload a File</h2>
        <form action="/upload" method="post" enctype="multipart/form-data">
          <div class="form-group">
            <input type="file" name="file" class="form-control-file" required>
          </div>
          <button type="submit" class="btn btn-primary">Upload</button>
        </form>
      </div>
    </body>
    </html>
    """
    return html_content

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        # Temporarily store file content in memory
        with NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            file_location = temp_file.name
        
        return {"message": f"File '{file.filename}' uploaded successfully!", "file_path": file_location}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error saving file") from e
