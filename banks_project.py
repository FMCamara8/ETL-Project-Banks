# importing the required library
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3

# variables initialisation
url = "https://web.archive.org/web/20230908091635 /https://en.wikipedia.org/wiki/List_of_largest_banks"
table_attribs = ["name", "Market cap (US$ billion)"]
output_path = "./Largest_banks_data.csv"
db_name = "Banks.db"
table_name = "Largest_banks"
log_file = "code_log.txt"

def log_progress(message):
    timestamp_format = "%Y-%h-%d-%H:%M:%S" # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp
    timestamp = now.strftime(timestamp_format)
    with open("./code_log.txt","a") as f :
        f.write(timestamp + " : " + message + "\n")

log_progress('Preliminaries complete. Initiating ETL process')

def extract(url, table_attribs):
    page = requests.get(url).text
    data = BeautifulSoup(page, 'html.parser')
    df = pd.DataFrame(columns=table_attribs)
    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')
    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:
            data_dict = {"name": col[1].text.strip(),
                        "Market cap (US$ billion)": col[2].text.strip()}
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df, df1], ignore_index=True)
    df["Market cap (US$ billion)"] = df["Market cap (US$ billion)"].astype(float)
    df.rename(columns={"Market cap (US$ billion)" : "MC_USD_Billion"}, inplace=True)

    return df
            
df = extract(url, table_attribs)
print('---'*25)
print()
print('The extracted dataframe \n\n', df) # print the extracted dataframe
print()
print('---'*25)

log_progress('Data extraction complete. Initiating Transformation process')

def transform(df):
    df_exchange_rate = pd.read_csv('exchange_rate.csv')
    exchange_rate = df_exchange_rate.set_index('Currency').to_dict()['Rate']
    gbp_rate = float(exchange_rate['GBP'])
    df['MC_GBP_Billion'] = [np.round(x * gbp_rate, 2) for x in df["MC_USD_Billion"]]
    eur_rate = float(exchange_rate['EUR'])
    df['MC_EUR_Billion'] = [np.round(x * eur_rate, 2) for x in df["MC_USD_Billion"]]
    inr_rate = float(exchange_rate['INR'])
    df['MC_INR_Billion'] = [np.round(x * inr_rate, 2) for x in df["MC_USD_Billion"]]
    
    return df

df = transform(df)
print()
print(f'The transformed dataframe\n\n', df) # print the transfomed dataframe
print('---'*25)
print()
print(f"The market capitalization of the 5th largest bank in billion EUR : {df['MC_EUR_Billion'][4]}")
print()
print('---'*25)

log_progress('Data transformation complete. Initiating loading process')

def load_to_csv(df, output_path):
    df.to_csv(output_path)

load_to_csv(df, output_path)

log_progress('Data saved to CSV file')

sql_connection = sqlite3.connect("Banks.db")

log_progress('SQL Connection initiated.')

def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)

load_to_db(df, sql_connection, table_name)

log_progress('Data loaded to Database as table. Running the query')

def run_query(query_statement, sql_connection):
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print()
    print(query_output)
    print()
    print('---'*25)

queries = ['SELECT * FROM Largest_banks',
            'SELECT AVG(MC_GBP_Billion) FROM Largest_banks',
            'SELECT name FROM Largest_banks LIMIT 5']

for q in queries:
    run_query(q, sql_connection)

log_progress('Process Complete.')

sql_connection.close()