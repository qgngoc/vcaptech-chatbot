# API Documentations

---

### 1. Chat (Generate Response)
- **Endpoint:** `POST /chat`
- **Description:** Generate a response based on the input messages and client information.

#### Request Schema (dict)
- `messages` (list[dict]): List of messages. Each message:
  - `role` (str): Role of the sender (e.g., 'user', 'assistant')
  - `content` (any): Content of the message
  - `tool_calls` (list, optional): List of tool calls
- `client` (dict): Client info. Example: `{ "id": "client_id" }`
- `rag_config` (dict): RAG config, e.g. `{ "llm_config": { ... }, "top_k": 5 }`

#### Response Schema (dict)
- `blocked_by_input_rail` (bool)
- `answer` (str | null)
- `citations` (list[dict] | null): Each citation includes file name, path, page number, and content
- `trace_id` (str)
- `flag` (int)


### 2. Get Tracing Logs
- **Endpoint:** `GET /metrics/{tracing_id}`
- **Description:** Get tracing logs for a specific tracing ID.

#### Path Parameter
- `tracing_id` (str): The tracing ID

#### Response Schema (dict)
- `logs` (list[dict]): List of log entries for the tracing ID
