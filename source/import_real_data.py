import pandas as pd
import numpy as np

# Runner parameters
def import_and_clean_results(file_path: str) -> pd.DataFrame:
    
    
    # Load the Excel sheet, skipping the first four rows and using the fifth row as headers
    df = pd.read_excel(file_path, skiprows=0)
    
    # Drop rows where 'Rank' is NaN (irrelevant rows)
    df_cleaned = df.drop(columns=['Bib', 'Expected'])
    df_cleaned['GrossTime'] = pd.to_timedelta(df_cleaned['Bruto'], errors='coerce')
    df_cleaned['NetTime'] = pd.to_timedelta(df_cleaned['Netto'], errors='coerce')
    df_cleaned['StartTimeHalf'] = pd.to_timedelta(df_cleaned['TimeStartHalf'], errors='coerce')
    df_cleaned['StartTimeFull'] = pd.to_timedelta(df_cleaned['TimeStart'], errors='coerce')
    df_cleaned = df_cleaned.dropna(subset=['StartTimeHalf'])
    
    # Covert to minutes to be used in analysis
    df_cleaned['GrossTime'] = df_cleaned['GrossTime'].dt.total_seconds() / 60
    df_cleaned['NetTime'] = df_cleaned['NetTime'].dt.total_seconds() / 60
    df_cleaned['StartTimeHalf'] = df_cleaned['StartTimeHalf'].dt.total_seconds() / 60 - 11.5 * 60     # subtract 14 * 60 is for start time at 11:30
    df_cleaned['StartTimeFull'] = df_cleaned['StartTimeFull'].dt.total_seconds() / 60 - 10 * 60     # subtract 14 * 60 is for start time at 10:00
    df_cleaned['Pace'] = np.where((df_cleaned['Afstand'] == 'Marathon') | (df_cleaned['Afstand'] == 'Estafette Marathon'), df_cleaned['NetTime'] / 42.2, np.nan)
    df_cleaned['Pace'] = np.where(df_cleaned['Afstand'] == 'Halve Marathon', df_cleaned['NetTime'] / 21.1, df_cleaned['Pace'])
    df_cleaned['Pace'] = np.where(df_cleaned['Afstand'] == 'Kwart Marathon', df_cleaned['NetTime'] / 10.55, df_cleaned['Pace'])
    
    # Quick and dirty filtering on half only
    df_cleaned = df_cleaned.loc[(df_cleaned['Afstand'] == 'Halve Marathon') & (df_cleaned['GrossTime'].notna())]
    
    print(df_cleaned)
    
    # Number of starters per minute
    StartRate = len(df_cleaned['StartTimeHalf']) / max(df_cleaned['StartTimeHalf'])
    print(f'Average number of starting runners per minute: {StartRate:.1f}')
         
    return df_cleaned



