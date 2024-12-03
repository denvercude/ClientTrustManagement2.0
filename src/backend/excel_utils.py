from dotenv import load_dotenv
import pandas as pd
import openpyxl
from datetime import datetime
import shutil
import os

load_dotenv()

def create_deposits_sheet(df):
    DEP_PATH = os.getenv("DEPOSITS_PATH")
    today_date = datetime.now().strftime('%m-%d-%y')
    destination_file = os.path.join(DEP_PATH, f"Deposits for Client Trust {today_date}.xlsx")

    # Check if template exists, otherwise raise an error
    template_path = os.path.join(DEP_PATH, 'template.xlsx')  # Ensure there is a template.xlsx in DEP_PATH
    if not os.path.exists(template_path):
        return {"message": "Template file not found", "status": "failure"}

    shutil.copy(template_path, destination_file)
    workbook = openpyxl.load_workbook(destination_file)
    sheet = workbook['Sheet 1']

    row = 8  # Start row for data entry in Excel
    type_groups = df.groupby('type', sort=False)  # Group by 'Type', maintain the order of appearance

    for type_name, group_data in type_groups:
        type_sum = group_data['amount'].sum()
        for index, data in group_data.iterrows():
            if row == 28:  # Check if row limit reached, switch sheet
                sheet = workbook['Sheet 2']
                row = 8

            sheet[f'B{row}'].value = data['last_name']
            sheet[f'D{row}'].value = data['first_name']
            sheet[f'F{row}'].value = data['type']
            sheet[f'H{row}'].value = data['amount']
            row += 1
        
        # Print type total
        sheet[f'H{row}'] = type_sum
        row += 2  # Leave a blank row after each type's data

    workbook.save(destination_file)
    return {"message": "Deposit sheet created successfully", "status": "success"}
