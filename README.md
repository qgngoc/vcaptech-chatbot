# VCAPTECH Agent

## Getting Started

### Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/qgngoc/vcaptech-chatbot
   cd vcaptech-chatbot
   ```

2. **Configure environment variables:**
   - Copy the `.env` and `env.docker` files with your credentials (Replace your OpenAI API Key only).

3. **Start the services:**
   
    Note: In order to deply these smoothly, all sudo permission must be granted to this directory. Command to grant permission: `sudo chmod -R 777 ./`

   ```bash
   sh build.sh
   docker compose --env-file .env.docker up -d
   ```
   **Or Start the services locally:**
   - Install the requirements:
   ```bash
   pip install -r src/requirements.txt
   ```
   - Run service:
   ```bash
   cd src/
   python main.py
   ```

5. **Run usecases**

   API `/health`:
   ```
   curl -X 'GET' \
     'http://localhost:8000/health' \
     -H 'accept: application/json'
   ```
   
   API `/chat` (Important: `client.id` must be `"0"`.):
   ```
   curl -X 'POST' \
     'http://localhost:8000/api/v1/chat' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{
           "messages": [
               {"role": "user", "content": "If the load is 1500 and the modulus is 30000, what is the settlement?"}
           ],
           "client": {
                   "id": "0"
               },
               "rag_config": {
                   "llm_config": {
                       "model_path": "gpt-4.1-mini"
                   },
                   "top_k": 5
               }
           }'
   ```
   
   API `/metrics` (Replace `trace_id` by the `trace_id` returned from `/chat`):
   ```
   curl -X 'GET' \
     'http://localhost:8000/api/v1/metrics/{trace_id}' \
     -H 'accept: application/json'
   ```

Please checkout `API Documentations.md` to get more details of those APIs.

# Evaluation
   Note: The service must be deployed by Docker to run the evaluation script.
   
   Run retrieval evaluation scripts:
   ```bash
   python retrieval_evaluation/eval.py
   ```
   Results are saved in `retrieval_evaluation/data/`.
   Results stats:
   ```
   +---------+---------+-----------+
   |   Top K |   Total |   Matched |
   +=========+=========+===========+
   |       1 |       8 |         7 |
   +---------+---------+-----------+
   |       2 |       8 |         8 |
   +---------+---------+-----------+
   |       3 |       8 |         8 |
   +---------+---------+-----------+
   ```

## Unit Testing
   Run unit tests:
   ```bash
   PYTHONPATH=src/ pytest
   ```
