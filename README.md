# Transclation Service

[System Overview Documentation](https://daffodil-throne-f06.notion.site/SamurAI-System-Overview-14c82c979e8480348029ec1cc43e9249?pvs=4)

This service is part of the SamurAI system, a microservices-based platform for processing and analyzing video content. The system consists of multiple services working together through RabbitMQ message queues and RESTful APIs.

## System Overview
![System Architecture](https://github.com/itsomar278/samurai_video_service/blob/main/ezgif-4-77c29e34de%20(1).gif)

The Transclation Service works by:
1. Consuming messages from RabbitMQ queues for video translation requests
2. Processing audio using the Faster Whisper model with CUDA for enhanced performance on GPU
3. Uploading the transcription results to AWS S3
4. Returning the status and results via a REST API

## Prerequisites

- RabbitMQ server running on port 5672
- CUDA-capable GPU (for optimal performance)
- Python 3.8+

## Installation

1. Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/itsomar278/samurai_video_service
cd transclation-service
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Set up the `.env` file with the required environment variables (details below).

## Environment Variables

Create a `.env` file in the root directory and include the following variables:

```env
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
S3_BUCKET_NAME=
MYSQL_DB=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_HOST=
MYSQL_PORT=
```

## Running the Service

1. Apply the database migrations:

```bash
python manage.py migrate
```

2. Start the Django development server:

```bash
python manage.py runserver 0.0.0.0:5050
```

3. Start the RabbitMQ consumer:

```bash
python manage.py rabbitmq_start_consume --threads <number of threads>
```

## Technologies Used

### Faster Whisper
This service uses [Faster Whisper](https://github.com/guillaumekln/faster-whisper), a high-performance library for audio transcription and translation. CUDA is utilized to accelerate processing on NVIDIA GPUs, ensuring faster and more efficient model inference.

### RabbitMQ
RabbitMQ is used for message queuing to handle video translation requests asynchronously, allowing the system to process multiple tasks concurrently and facilitate intercommunication with other services.

### AWS S3
Transcription results are stored in an AWS S3 bucket, providing a scalable and reliable storage solution.

## Key Features

- **Batch Processing**: Handles multiple translation requests using RabbitMQ and threading
- **High-Performance Transcription**: Leveraging Faster Whisper with CUDA for GPU acceleration
- **Cloud Integration**: Transcription results are uploaded to AWS S3 for accessibility
- **RESTful APIs**: Exposes endpoints for checking translation status and retrieving user-specific requests

## API Endpoints

### Check Translation Status
`GET /api/translation-status`

**Query Parameters:**
- `request_id`: ID of the translation request
- `user_id`: ID of the user

### Get Translations by User
`GET /api/translations-by-user`

**Query Parameters:**
- `user_id`: ID of the user

## Related Services

### Authentication Service
Authentication and user management service:
[samurai_auth_service](https://github.com/itsomar278/samurai_auth_service)

### API Gateway
Central API gateway for routing and service orchestration:
[samurai_api_gateway](https://github.com/itsomar278/samurai_api_gateway)

### LLM Interaction Service
Service for handling language model interactions:
[samurai_LLM_interaction](https://github.com/itsomar278/samurai_LLM_interaction)

## Notes

- Ensure CUDA is properly installed and configured on your system to utilize GPU acceleration with Faster Whisper
- Update the `.env` file with appropriate values before running the service
- Make sure RabbitMQ server is installed and running on port 5672 before starting the service
