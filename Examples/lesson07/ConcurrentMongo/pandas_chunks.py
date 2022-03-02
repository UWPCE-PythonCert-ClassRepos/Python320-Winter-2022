import pandas as pd

def import_csv_in_chunks(size=10):
    '''
    Imports CSV file in chunks of a defined size
    '''
    chunk_number = 0
    for chunk in pd.read_csv('accounts.csv', chunksize=size, iterator=True):
        print(f"CHUNK {chunk_number}")
        for index, row in chunk.iterrows():
            print(f"{row['USER_ID']} {row['EMAIL']} {row['NAME']} {row['LASTNAME']}")
        chunk_number += 1

if __name__ == "__main__":
    import_csv_in_chunks()
