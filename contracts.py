# client -> master
'''
{
    "command": text
    "data": [][]
}
'''

# db -> master -> node
'''
{
    "node_task_id": int,
    "command": text,
    "data": []?
}
'''

# node -> master
'''
"result" -> db.update_node_task_result(node_task_id, result)

type: result
{
    "type" : result,
    "results": [
            {
                "task_id": int,
                "result": text,
            }
        ]
}

"state" -> scheduler.push_single_node_state(node_id, state)

type: status
{
    "type" : status,
    "state": 
            {
                "node_id": int
                "wait": int,
                "busy": int,
                "done" int
            }
}
'''
