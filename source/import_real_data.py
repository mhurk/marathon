import pandas as pd
import openpyxl

# Runner parameters
def import_and_clean_results(file_path: str, sheet_name: str = 'Vrouwen') -> pd.DataFrame:
    
    # Load the Excel sheet, skipping the first four rows and using the fifth row as headers
    df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=4)
    
    # Rename the columns for better clarity
    df.columns = [
        'Rank', 'BibNumber', 'Name', 'Team/Club/City', 'Category', 'CategoryRank',
        'Net3k9', 'Net5k', 'Net8k9', 'Net10k', 'Net13k9', 'Net15k', 'Net18k9', 
        'GrossTime', 'NetTime', 'StartTimeHalf'
    ]
    
    # Drop rows where 'Rank' is NaN (irrelevant rows)
    df_cleaned = df.drop(columns=['Rank', 'Name', 'BibNumber', 'Team/Club/City', 'Category', 'CategoryRank',
        'Net3k9', 'Net5k', 'Net8k9', 'Net10k', 'Net13k9', 'Net15k', 'Net18k9'])
    df_cleaned['GrossTime'] = pd.to_timedelta(df_cleaned['GrossTime'], errors='coerce')
    df_cleaned['NetTime'] = pd.to_timedelta(df_cleaned['NetTime'], errors='coerce')
    df_cleaned['StartTimeHalf'] = pd.to_timedelta(df_cleaned['StartTimeHalf'], errors='coerce')
    df_cleaned = df_cleaned.dropna(subset=['StartTimeHalf'])
    
    # Covert to minutes to be used in analysis
    df_cleaned['GrossTime'] = df_cleaned['GrossTime'].dt.total_seconds() / 60
    df_cleaned['NetTime'] = df_cleaned['NetTime'].dt.total_seconds() / 60
    df_cleaned['StartTimeHalf'] = df_cleaned['StartTimeHalf'].dt.total_seconds() / 60 - 14 * 60     # subtract 14 * 60 is for start time at 14:00
    df_cleaned['Pace'] = df_cleaned['NetTime'] / 21.1                                               # minute per km
    
    # Number of starters per minute
    StartRate = len(df_cleaned['StartTimeHalf']) / max(df_cleaned['StartTimeHalf'])
    print(f'Number of starting runners per minute: {StartRate:.2f}')
        
    # print(df_cleaned)
    # print(df_cleaned.dtypes)
        
    return df_cleaned






