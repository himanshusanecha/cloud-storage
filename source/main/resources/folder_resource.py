from fastapi import APIRouter

class FolderResource:
    
    def __init__(self):
        self.router = APIRouter(prefix="/folder")
        self.router.add_api_route("/create", self.create_folder)
        
    def create_folder(self, user_id: str, folder_name: str):
        print("create folder")

    def delete_folder(self, user_id: str, folder_name: str):
        print("delete_folder")
    
    def list_files(self, user_id: str, folder_id: str):
        print("list_files")
        
    def get_details(self, user_id: str, folder_id: str):
        print("get_details")
        
        