import pandas as pd
import sqlite3

def load_data(path):
    """
    Loads data from an Excel file and stores it in a SQLite database.
    Args:
        path (str): Path to the Excel file containing well data.
    """
    try:
        # Read Excel data
        data = pd.read_excel(path)
        
        # Group data and calculate annual sums
        calculated_data = data.groupby(['API WELL  NUMBER', 'Production Year'])[['OIL', 'GAS','BRINE']].sum().reset_index()
        print(calculated_data)

        # Connect to SQLite database
        conn = sqlite3.connect('annual_data.db')
        cursor = conn.cursor()

        # Create table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS WellData (
                API_WELL_NUMBER INTEGER,
                Production_Year INTEGER,
                OIL INTEGER,
                GAS INTEGER,
                BRINE INTEGER      
            )
        ''')

        # Insert the aggregated data into the SQLite table
        for _, row in calculated_data.iterrows():
            cursor.execute('''
                INSERT INTO WellData (API_WELL_NUMBER, Production_Year, OIL, GAS, BRINE)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                int(row['API WELL  NUMBER']),
                int(row['Production Year']),
                int(row['OIL']),
                int(row['GAS']),
                int(row['BRINE'])
            ))

        # Commit changes and close the connection
        conn.commit()
        conn.close()
    
    except Exception as e:
        print(f"Error loading data: {e}")


def fetch_annaul_data(well):
    """
    Fetches annual data for a specific well from the SQLite database.
    Args:
        well_number: API well number to query.
    Returns:
        dict: Dictionary containing annual data for the requested well,
                or None if no data is found.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('annual_data.db')
        cursor = conn.cursor()

        # Execute query to fetch data of a specific well
        cursor.execute('''
            SELECT OIL, GAS, BRINE  FROM WellData WHERE API_WELL_NUMBER = ?
        ''', (well,))

        # Fetch all rows that match the query
        results = cursor.fetchall()

        # Close the connection
        conn.close()

        data = {}
        if results:
            for row in results:
                data["oil"] =row[0]
                data["gas"] =row[1]
                data["brine"] =row[2]
            return data
        else:
            return None

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None