"""https://www.wikidata.org/w/api.php?action=wbgetentities&props=labels&ids=Q1000048&languages=en&format=json"""
import requests
import pandas as pd

INPUT_DATASET_PATH = 'filtered_dataset.csv'
SAVE_AS_DATASET_PATH = 'prepared_dataset_'

def query_wikidata(wiki_id):
    request_url = "https://www.wikidata.org/w/api.php"
    params = {'action': 'wbgetentities', 'props': 'labels', 'ids': wiki_id,
              'languages': 'en', 'format': 'json'}
    response = requests.get(url=request_url, params=params)
    entity_value = ""
    try:
        if response.status_code == 200:
            response_json = response.json()
            entity_value = response_json['entities'][wiki_id]['labels']['en']['value']
    except Exception as e:
        pass
    return entity_value

def extract_entities_and_types(df, start_index, batch_size):
    value_list = []
    end_index = min(start_index + batch_size, len(df))
    print(f'starting with index {start_index} and end index {end_index}')
    for i in range (start_index, end_index):
        row = df.iloc[i]
        entity_value = query_wikidata(row['WikiID'])
        if entity_value is not None and entity_value != '':
            entry = [row['WikiID'], entity_value, row['Type']]
            #print(entry)
            value_list.append(entry)
    result_df = pd.DataFrame(value_list, columns =['WikiID', 'Entity', 'Type'])
    return result_df

def process(input_dataset_path = INPUT_DATASET_PATH, save_as_dataset_path = SAVE_AS_DATASET_PATH):
    df = pd.read_csv(input_dataset_path)
    n = len(df)
    batch_size = 100000
    df_list = []
    for i in range(0, n, batch_size):
        result_df = extract_entities_and_types(df, start_index = i, batch_size = batch_size)
        df_list.append(result_df)
        filename = f'{save_as_dataset_path}{i}.csv'
        result_df.to_csv(filename)

if __name__ == '__main__':
    process()
#response_json = query_wikidata(query_id)
#print(response_json['entities'][query_id]['labels']['en']['value'])
