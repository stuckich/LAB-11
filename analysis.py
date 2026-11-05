# analysis.py

def validate_todos(data):
    if type(data) is not list:
        raise ValueError("Корень JSON должен быть списком.")
    
    seen_ids = set()
    
    for index, item in enumerate(data):
        if type(item) is not dict:
            raise ValueError(f"Элемент с индексом {index} должен быть словарем.")
        
        for key in ["id", "userId", "title", "completed"]:
            if key not in item:
                raise ValueError(f"В элементе с индексом {index} отсутствует обязательный ключ '{key}'.")
        
        if type(item["id"]) is not int:
            raise ValueError(f"Поле 'id' в элементе {index} должно быть целым числом (int).")
        
        if type(item["userId"]) is not int:
            raise ValueError(f"Поле 'userId' в элементе {index} должно быть целым числом (int).")
            
        if type(item["title"]) is not str or not item["title"].strip():
            raise ValueError(f"Поле 'title' в элементе {index} должно быть непустой строкой.")
            
        if type(item["completed"]) is not bool:
            raise ValueError(f"Поле 'completed' в элементе {index} должно быть логическим значением (bool).")
        
        todo_id = item["id"]
        if todo_id in seen_ids:
            raise ValueError(f"Обнаружен дублирующийся идентификатор id: {todo_id}.")
        seen_ids.add(todo_id)


def completion_counts(todos):
    counts = {}
    for item in todos:
        user_id = item["userId"]
        if user_id not in counts:
            counts[user_id] = 0
        if item["completed"]:
            counts[user_id] += 1
    return counts


def top_users(counts):
    if not counts:
        return []
    
    max_completed = max(counts.values())
    if max_completed == 0:
        return []
        
    leaders = [user_id for user_id, count in counts.items() if count == max_completed]
    return sorted(leaders)
