# AWS Rekognition Vision Analyzer
=====================================

A cloud-based image analysis service using Amazon Rekognition and Streamlit for user interaction.

## Project Description
--------------------

This project utilizes Amazon Rekognition to detect objects and visual labels in images. Users can upload an image, and the application will analyze it using Rekognition, displaying the results in a user-friendly interface.

## Badges
--------

[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.9.0-orange.svg)](https://streamlit.io/)

## PROEJCT UI
[!Rekognition](./project%20demo%20images/rekognition01.png)
[!Rekognition](./project%20demo%20images/rekognition02.png)

## USER FLOW AT UI SIDE
[!Rekognition](./project%20demo%20images/prject%20flow%20for%20ui%20user.png)


## Overview and Key Features
---------------------------

* Detect objects and visual labels in images using Amazon Rekognition
* User-friendly interface for image upload and analysis
* Results displayed in a clear and concise manner

## Technology Stack
-----------------

* **Languages:** Python 3.9
* **Frameworks:** Streamlit 1.9.0
* **Libraries:**
	+ Boto3 (AWS SDK for Python)
	+ Pillow (Python Imaging Library)
	+ Python-dotenv (for loading environment variables)
* **Infrastructure:** AWS (Amazon Web Services), specifically Amazon Rekognition

## Architecture
-------------

```mermaid
graph LR
    User-->|Upload Image| Streamlit App
    Streamlit App-->|Process Image| Rekognition Service
    Rekognition Service-->|Detect Labels| Amazon Rekognition
    Amazon Rekognition-->|Return Results| Streamlit App
    Streamlit App-->|Display Results| User
```

## Project Structure
------------------

```markdown
aws-rekognition-vision-analyzer/
├── backend/
│   └── rekognition_service.py
├── configuration/
│   └── config.py
├── frontend/
│   └── streamlit_app_rekognition.py
├── demo/
│   ├── images/
│   └── labels.csv
└── requirements.txt
```

## Prerequisites
--------------

* Python 3.9 installed
* Boto3, Pillow, and Streamlit installed using pip
* AWS account with Amazon Rekognition enabled

## Installation and Setup
------------------------

1. Clone the repository
2. Install required libraries using pip: `pip install -r requirements.txt`
3. Set environment variables using `python -m python-dotenv`

## Environment Variables
----------------------

* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`
* `REKOGNITION_REGION`

## How to Run the Application
-----------------------------

1. Run the Streamlit application: `streamlit run frontend/streamlit_app_rekognition.py`

## API Endpoints and Usage Examples
---------------------------------

* The application uses the Amazon Rekognition API to detect labels in images
* Example usage:
```python
import boto3

rekognition = boto3.client('rekognition')

image = open('image.jpg', 'rb')
response = rekognition.detect_labels(Image={'Bytes': image.read()})
print(response['Labels'])
```

## Database or AI/RAG Workflow
-----------------------------

The application uses Amazon Rekognition, a cloud-based image analysis service, for AI-powered image analysis.

## Testing Instructions
---------------------

No tests are provided in the repository.

## Docker or Deployment Instructions
---------------------------------

No Docker or deployment instructions are provided.

## Security Notes
----------------

* Ensure that AWS credentials are secure and not committed to the repository
* Use environment variables to store sensitive information

## Limitations and Future Improvements
--------------------------------------

* The application does not handle errors or exceptions properly
* The `build_llm` function in `configuration/config.py` is not clear
* The `detect_image_labels` function in `backend/rekognition_service.py` is not well-documented

## Contribution and License
-------------------------

This project is not open-sourced and is for personal use only.
