import os
import requests
import json
from typing import Dict, Any, Optional

class LinkedinAPIClient:
    def __init__(self):
        self.access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
        if not self.access_token:
            raise ValueError("Linkedin access token not provided")
        self.person_id = os.environ.get("LINKEDIN_PERSON_ID")
        if not self.person_id:
            raise ValueError("Linkedin person id not provided")

        self.base_url = "https://api.linkedin.com/v2"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }

    def create_text_post(self, content, visibility):
        try:
            post_data = {
                "author": f"urn:li:person:{self.person_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": content
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": visibility
                }
            }
            
            response = requests.post(
                f"{self.base_url}/ugcPosts",
                headers=self.headers,
                json=post_data
            )
            
            if response.status_code in [200, 201]:
                return {
                    "success": True,
                    "post_id": response.json().get("id", "unknown"),
                    "status_code": response.status_code
                }
            else:
                return {
                    "success": False,
                    "error": response.text,
                    "status_code": response.status_code
                }
                
        except Exception as e:
            print(f"Error creating LinkedIn post: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }

    def get_post_status(self, post_id):
        try:
            response = requests.get(
                f"{self.base_url}/ugcPosts/{post_id}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "status_code": response.status_code
                }
            else:
                return {
                    "success": False,
                    "error": response.text,
                    "status_code": response.status_code
                }
                
        except Exception as e:
            print(f"Error getting LinkedIn post status: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }