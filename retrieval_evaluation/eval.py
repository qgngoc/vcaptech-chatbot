
import json
import requests
from fastapi.testclient import TestClient

# from src.main import app

def run_evaluate_one(data, top_k):
    # client = TestClient(app=app)
    question = data.get('question')
    input_data = {
        "messages": [
            {"role": "user", "content": question}
        ],
        "client": {
                "id": "0"
            },
            "rag_config": {
                "llm_config": {
                    "model_path": "gpt-4.1-mini"
                },
                "top_k": top_k
            }
        }
    # response = client.post("/api/v1/chat", json=input_data)
    response = requests.post("http://localhost:8000/api/v1/chat", json=input_data)
    response.raise_for_status()

    answer = response.json().get("answer")
    citations = response.json().get("citations")

    citation_matched = False
    for citation in citations:
        if citation['file_path'].lower().strip() in data.get('context_source').lower().strip() or data.get('context_source').lower().strip() in citation['file_path'].lower().strip():
            citation_matched = True
            break

    result = {
        "prediction": answer,
        "citations": citations,
        "citation_matched": citation_matched
    }
    data.update(result)
    return data

def evaluate(dataset, top_ks):
    results = []
    for data in dataset:
        for top_k in top_ks:
            eval_result = run_evaluate_one(data.copy(), top_k)
            eval_result['top_k'] = top_k
            results.append(eval_result)
    return results

if __name__ == "__main__":
    TOP_KS = [1, 2, 3]

    with open('retrieval_evaluation/data/benchmark.jsonl') as f:
        dataset = [json.loads(line) for line in f]

    results = evaluate(dataset, TOP_KS)

    # save results
    with open('retrieval_evaluation/data/benchmark_results.json', 'w') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    # save statistics of citation match with each top k
    with open('retrieval_evaluation/data/benchmark_stats.json', 'w') as f:
        stats = {}
        for top_k in TOP_KS:
            stats[top_k] = {
                "total": 0,
                "matched": 0
            }
            for result in results:
                if result['top_k'] == top_k:
                    stats[top_k]['total'] += 1
                    if result['citation_matched']:
                        stats[top_k]['matched'] += 1
        json.dump(stats, f, indent=4, ensure_ascii=False)
