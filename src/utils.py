import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

def get_user_coordinates(file_path: str):
    try:
        column_index = 0
        # Load the spreadsheet into a pandas DataFrame
        df = pd.read_excel(file_path, sheet_name='Coordinates', header=None) if file_path.endswith('.xlsx') else pd.read_csv(file_path, header=None)
        
        # Extract the specified column as a list
        coordinates = df.iloc[:, column_index].tolist()
        
        # Return the cleaned list, ignoring any NaNs
        return [int(coord) for coord in coordinates if pd.notna(coord)]
    
    except Exception as e:
        print(f"Error loading coordinates: {e}")
        return []

def save_data(file_path: str, columns: list, datapoints,
              sheet_name='Datapoints'):
    if not isinstance(datapoints, (list, np.ndarray)):
        raise ValueError("Variable datapoints needs to be a list or a numpy array.")
    if isinstance(datapoints, list):
        datapoints = np.array(datapoints)
    if datapoints.shape[-1]%2 != 0 or len(datapoints.shape) != 2:
        print(f'datapoints is shape {datapoints.shape}')
        raise ValueError("Datapoints must be an Nx2 array.")
    output_folder, file_name = os.path.split(file_path)
    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, file_name)
    _, extension = os.path.splitext(file_name)
    if extension == '.xlsx':
        # Convert to pandas dataframe
        df = pd.DataFrame(datapoints, columns=columns)
        try:
            # Read the existing file
            with pd.ExcelFile(file_path) as existing_file:
                # Load all existing sheets
                sheets = {sheet: pd.read_excel(existing_file, sheet_name=sheet) 
                        for sheet in existing_file.sheet_names}
        except FileNotFoundError:
            # If the file doesn't exist, start with an empty dictionary
            sheets = {}
        # Add or replace the new sheet
        sheets[sheet_name] = df
        # Write back all the sheets to the file
        with pd.ExcelWriter(file_path, mode="w") as writer:
            for sheet, data in sheets.items():
                data.to_excel(writer, sheet_name=sheet, index=False)
    else:
        raise ValueError("Please enter in a path to a spreadsheet (.xlsx)")
    return
