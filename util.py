import csv
import json
  

def retrieve_style(filename):
    # check if the extension is csv or json 
    data = None
    if filename.endswith('.csv'):
        with open(filename, 'r', encoding='utf-8') as csv_file:
            data = csv.reader(csv_file)
            data = [{"style": row[0], "positive": row[1],"negative":row[2]} for row in data]
            
    elif filename.endswith('.json'):
        with open(filename, 'r') as file:
            data = json.load(file)
    return data[-1]
