import json
import requests


def prepare_json(tasks, data):
    payload = {
        "tasks": tasks,
        "data": data
    }
    return json.dumps(payload)


def send_to_master_node(json_payload, master_node_url):
    headers = {"Content-Type": "application/json"}
    response = requests.post(master_node_url, data=json_payload, headers=headers)
    return response.json()