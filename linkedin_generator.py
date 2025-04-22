import os
import json
import autogen
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from typing import Dict, Any, List, Optional

llm_config = {
    "model": "gpt 4",
    "temperature": 0.4,
}

class LinkedInAgentSystem:    
    def __init__(self):
        self._initialize_agents()

    def _initialize_agents(self):
        """Create the agent ecosystem"""
        self.content_creator = AssistantAgent(
            name="LinkedIn_Content_Creator",
            llm_config=llm_config,
            system_message="""You are a LinkedIn content specialist who creates engaging, professional posts.
            Create content that is insightful, concise, and optimized for LinkedIn's algorithm.
            Focus on delivering value with actionable insights and avoid generic advice.
            Use formatting effectively with line breaks, emojis, and bullet points when appropriate.
            Each post should be between 150-300 words and include relevant hashtags."""
        )
        
        self.editor = AssistantAgent(
            name="LinkedIn_Editor",
            llm_config=llm_config,
            system_message="""You are an expert LinkedIn post editor who refines content for maximum engagement.
            Your job is to:
            1. Improve clarity and conciseness while maintaining the original message
            2. Enhance the hook (first 2-3 lines) to capture attention
            3. Optimize for readability with appropriate spacing and formatting
            4. Ensure content is professional and error-free
            5. Refine hashtags to include 3-5 relevant ones that will maximize reach
            6. Mark the end of your final edited content with 'FINAL_CONTENT:' followed by the post"""
        )
        
        self.user_proxy = UserProxyAgent(
            name="User_Proxy",
            llm_config=llm_config,
            human_input_mode="NEVER", 
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: "FINAL_CONTENT:" in x.get("content", ""),
            code_execution_config=False 
        )
    
    def generate_content(self): 
        prompt = f"""

        """
        self.user_proxy.initiate_chat(
            self.content_creator, 
            message=prompt
        )
        
        creator_messages = self.user_proxy.chat_messages[self.content_creator]
        draft_content = creator_messages[-1]["content"]
        
        edit_prompt = f"Please edit and optimize this LinkedIn post draft:\n\n{draft_content}"
        self.user_proxy.initiate_chat(
            self.editor,
            message=edit_prompt
        )
        
        editor_messages = self.user_proxy.chat_messages[self.editor]
        final_message = editor_messages[-1]["content"]
        
        if "FINAL_CONTENT:" in final_message:
            parts = final_message.split("FINAL_CONTENT:")
            final_content = parts[1].strip()
        else:
            final_content = final_message
        
        return final_content

