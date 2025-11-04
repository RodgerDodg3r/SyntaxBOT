import json
import os


def load_json(file_path):
    project_root = os.path.dirname(os.path.dirname(__file__))
    final_path = os.path.join(project_root, file_path)
    try:
        with open(final_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print("Upon executing found error: ", e)
        return {"Error": f"{e}"}

def get_value(data, value):
    try:
        return data[value]
    except Exception as e:
        print(f"Error found upon accessing {value} : {e}")
        return "ErrorValue"