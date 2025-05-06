# LinkedIn Auto-Poster

An automated system that generates and posts high-quality content to LinkedIn on a scheduled basis using Airflow, Azure Blob Storage, and the LinkedIn API.

## Overview

This project creates an end-to-end pipeline for LinkedIn content creation and posting:

1. **Content Generation**: Uses AI agents (via AutoGen and GPT-4) to generate engaging LinkedIn posts
2. **Content Storage**: Saves posts to Azure Blob Storage for archiving and retrieval 
3. **Content Publishing**: Posts directly to LinkedIn through their API
4. **Workflow Orchestration**: Manages the entire process using Apache Airflow

## Architecture

![Architecture Diagram](https://via.placeholder.com/800x400?text=LinkedIn+Auto-Poster+Architecture)

## Components

### LinkedIn Content Generation
- Uses the AutoGen framework to create a system of AI agents
- Includes specialized agents for content creation and editing
- Generates professional content optimized for LinkedIn's algorithm

### Azure Blob Storage
- Stores generated content with timestamps
- Provides persistent storage for post history and analytics
- Manages state between generation and posting steps

### LinkedIn API Integration
- Posts content directly to LinkedIn
- Supports visibility controls (public/connections)
- Can retrieve post status for monitoring

### Airflow Orchestration
- Schedules content generation and posting
- Manages the workflow between components
- Provides error handling and retries

## Setup

### Prerequisites
- Python 3.8+
- Apache Airflow 2.0+
- Azure Storage Account
- LinkedIn Developer Account with API access

### Environment Variables
```
# Azure Storage
AZURE_BLOB_CONNECTION_STRING=your_connection_string
AZURE_BLOB_NAME=your_container_name

# LinkedIn API
LINKEDIN_ACCESS_TOKEN=your_access_token
LINKEDIN_PERSON_ID=your_person_id
```

### Installation

1. Clone this repository
```bash
git clone https://github.com/yourusername/linkedin-auto-poster.git
cd linkedin-auto-poster
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
```bash
export AZURE_BLOB_CONNECTION_STRING="your_connection_string"
export AZURE_BLOB_NAME="your_container_name"
export LINKEDIN_ACCESS_TOKEN="your_access_token"
export LINKEDIN_PERSON_ID="your_person_id"
```

4. Add the DAG to your Airflow installation

## Usage

### Running with Airflow

The DAG is scheduled to run daily. It will:
1. Generate LinkedIn content
2. Save it to Azure Blob Storage
3. Post it to LinkedIn

### Manual Execution

You can also run components independently:

```python
# Generate content
from linkedin_generator import LinkedInAgentSystem
agent_system = LinkedInAgentSystem()
content = agent_system.generate_content()

# Save to Azure
from azure_storage import AzureBlobStorage
azure_blob = AzureBlobStorage("my_post.json")
azure_blob.save_content(content)

# Post to LinkedIn
from linkedin_api import LinkedinAPIClient
linkedin_client = LinkedinAPIClient()
linkedin_client.create_text_post(content, visibility="PUBLIC")
```

## Configuration

### Content Generation
To customize the content generation prompts, modify the system messages in `LinkedInAgentSystem`:

```python
self.content_creator = AssistantAgent(
    name="LinkedIn_Content_Creator",
    llm_config=llm_config,
    system_message="""Your custom prompt here"""
)
```

### Posting Schedule
To change the posting frequency, modify the DAG's `schedule_interval`:

```python
with DAG(
    'linkedin_posting_dag',
    ...
    schedule_interval=timedelta(days=2),  # Change to post every 2 days
    ...
) as dag:
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [AutoGen](https://github.com/microsoft/autogen) for the agent framework
- [Azure Blob Storage SDK](https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/storage/azure-storage-blob) for cloud storage
- [LinkedIn API](https://docs.microsoft.com/en-us/linkedin/marketing/getting-started) for post publishing
