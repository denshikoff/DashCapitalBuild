
import pandas as pd
from pip._vendor import requests

response = requests.get('https://api.reformagkh.ru/json-rpc')
df = pd.json_normalize(response.json())

print(df.columns)
