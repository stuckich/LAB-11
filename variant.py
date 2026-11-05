import json

def select_tasks(todos, user_id, parameter=None):
    if not isinstance(todos, list):
        return []
    
    user_exists = any(isinstance(task, dict) and task.get('userId') == user_id for task in todos)
    if not user_exists:
        return []

    if parameter is not None:
        try:
            parameter = float(parameter)
            if parameter < 0:
                parameter = None
        except (ValueError, TypeError):
            parameter = None

    selected_tasks = []

    for task in todos:
        if not isinstance(task, dict):
            continue
        
        if task.get('userId') == user_id:
            is_completed = task.get('completed') is True
            task_id = task.get('id')
            
            if is_completed:
                if parameter is not None:
                    # Если порог задан, id должен быть <= порога
                    if isinstance(task_id, (int, float)) and task_id <= parameter:
                        selected_tasks.append(task)
                else:
                    selected_tasks.append(task)

    return selected_tasks

sample_todos = [
    {"userId": 1, "id": 1, "title": "Task 1", "completed": True},
    {"userId": 1, "id": 2, "title": "Task 2", "completed": False},
    {"userId": 1, "id": 3, "title": "Task 3", "completed": True},
    {"userId": 2, "id": 4, "title": "Task 4", "completed": True},
]

target_user_id = 1
threshold_parameter = 2 

selected_res = select_tasks(sample_todos, target_user_id, parameter=threshold_parameter)

with open('selected.json', 'w', encoding='utf-8') as f:
    json.dump(selected_res, f, ensure_ascii=False, indent=4)

print(f"Успешно выбрано задач: {len(selected_res)}. Результат сохранен в 'selected.json'.")
