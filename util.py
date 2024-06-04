import csv
import json
  

def retrieve_style(filename):
    data = None
    if filename.endswith('.csv'):
        with open(filename, 'r', encoding='utf-8') as csv_file:
            data = csv.reader(csv_file)
            data = [{"style": row[0], "positive": row[1],"negative":row[2]} for row in data]     
    elif filename.endswith('.json'):
    # TODO : needs to be tested 
        with open(filename, 'r') as file:
            data = json.load(file)
    return data

def read_all_files(dir_path):
    files = [f"{dir_path}/{file}" for file in os.listdir(dir_path) if file.endswith('.csv') or file.endswith('.json')]
    data = []
    for file in files:
        data.append(retrieve_style(file))
    return data