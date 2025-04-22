import os
import json
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from typing import Dict, Any, Optional

class AzureBlobStorage:
    def __init__(self, blob_name):
        self.connection_string = os.environ["AZURE_BLOB_CONNECTION_STRING"]
        self.blob_storage_name = os.environ["AZURE_BLOB_NAME"]
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.blob_name = blob_name
        
        self.ensure_container_exists()

    def ensure_container_exists(self):
        try:
            self.container_client = self.blob_service_client.get_container_client(self.blob_storage_name)
            self.container_client.get_container_properties()  
        except Exception:
            self.container_client = self.blob_service_client.create_container(self.blob_storage_name)

    def save_content(self, content):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            post_data = {
                "content": content,
                "created_at": timestamp,
                "status": "successful"
            }
            json_data = json.dumps(post_data, indent=2)
            
            blob_client = self.container_client.get_blob_client(self.blob_name)
            
            blob_client.upload_blob(
                json_data,
                overwrite=True
            )
            
            return self.blob_name  

        except Exception as e:
            print(f"Error saving content to Azure Blob Storage: {str(e)}")
            raise

    def get_content(self):
        try:
            blob_client = self.container_client.get_blob_client(self.blob_name)
            
            download_stream = blob_client.download_blob()
            post_data = json.loads(download_stream.readall())
            
            return post_data
            
        except Exception as e:
            print(f"Error retrieving content from Azure Blob Storage: {str(e)}")
            raise

