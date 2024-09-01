from fastapi import FastAPI
from resources.folder_resource import FolderResource
from resources.file_resource import FileResource
from fastapi.middleware.cors import CORSMiddleware

folder_resource = FolderResource()
file_resource = FileResource()

app = FastAPI()
app.include_router(folder_resource.router)
app.include_router(file_resource.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # Allows all origins
    allow_credentials=True,        # Allows cookies
    allow_methods=["*"],           # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],           # Allows all headers
)