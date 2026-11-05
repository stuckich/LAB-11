import json
import os
from analysis import validate_todos, completion_counts, top_users

INPUT_FILE = "todos.json"
OUTPUT_FILE = "leaders.json"

def main():
    try:
        if not os.path.exists(INPUT_FILE):
            print(f"Ошибка: Файл '{INPUT_FILE}' не найден.")
            return

        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        validate_todos(data)
        
    except json.JSONDecodeError as e:
        print(f"Ошибка: Некорректный формат JSON в файле. Подробности: {e}")
        return
    except ValueError as e:
        print(f"Ошибка валидации данных: {e}")
        return
    except LookupError:
        print("Ошибка: Указана неправильная или неподдерживаемая кодировка файла.")
        return
    except PermissionError:
        print(f"Ошибка: Нет прав на чтение файла '{INPUT_FILE}' или запись '{OUTPUT_FILE}'.")
        return
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при обработке: {e}")
        return

    counts = completion_counts(data)
    leaders_ids = top_users(counts)
    
    print("--- Сводка анализа ---")
    print(f"Всего задач обработано: {len(data)}")
    print(f"Статистика выполненных задач по пользователям: {counts}")
    print(f"Идентификаторы лидеров: {leaders_ids}")
    
    if not leaders_ids:
        print("Нет пользователей с выполненными задачами. Сводка завершена.")
        return

    leaders_tasks = [item for item in data if item["userId"] in leaders_ids and item["completed"]]
    leaders_task_ids = [item["id"] for item in leaders_tasks]
    
    print(f"Задачи лидеров (сохранен оригинальный порядок): {leaders_task_ids}")

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(leaders_task_ids, f, ensure_ascii=False, indent=2)
        print(f"Результаты успешно сохранены в файл '{OUTPUT_FILE}'.")
    except PermissionError:
        print(f"Ошибка: Запрещено изменять или создавать файл '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()
