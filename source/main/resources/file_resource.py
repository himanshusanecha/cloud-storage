from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from services.file_service import FileService
import uuid

class FileResource:
    
    def __init__(self):
        self.router = APIRouter(prefix="/file")
        self.router.add_api_route("/upload_chunks", self.upload_chunks, methods=["POST"])
        self.router.add_api_route("/upload", self.file_upload, methods=["POST"])
        self.file_service = FileService()

    def file_upload(self):
        # generate uuid
        id = uuid.uuid4()
        return {"id": id}
    
    async def upload_chunks(
        self, 
        id: str = Form(...),
        chunk_num: int = Form(...),
        filename: str = Form(...), 
        path: str = Form(...), 
        parent_folder: str = Form(...), 
        chunk_data: UploadFile = File(...)  # Accepting UploadFile
    ):
        """
        Endpoint to handle file chunks upload.
        """
        try:
            # Read the chunk data as bytes
            chunk_content = await chunk_data.read()
            # Ensure the data is in bytes format
            if not isinstance(chunk_content, bytes):
                raise ValueError("Chunk data must be in bytes format.")

            # Pass the bytes to the service function
            self.file_service.produce_message(id, chunk_num, chunk_content, filename, path, parent_folder)
            return {"status": True}

        except Exception as e:
            print(f"Error processing upload chunk: {e}")
            raise HTTPException(status_code=500, detail=str(e))