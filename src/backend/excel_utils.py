from dotenv import load_dotenv
import pandas as pd
import openpyxl
from datetime import datetime, timedelta
import shutil
import os
from dateutil.relativedelta import relativedelta
import holidays

load_dotenv()

def get_next_workday(date):
    us_holidays = holidays.US()  # Adjust to your locale if needed
    while date.weekday() >= 5 or date in us_holidays:  # Saturday (5) or Sunday (6)
        date += timedelta(days=1)
    return date

def create_deposits_sheet(df):
    try:
        DEP_PATH = os.getenv("DEPOSITS_PATH")

        if DEP_PATH is None:
            raise ValueError("DEPOSITS_PATH environment variable is not set.")

        today = datetime.now()
        deposit_date = get_next_workday(today)
        year = deposit_date.year
        today_date_str = deposit_date.strftime('%m-%d-%y')

        year_dir = os.path.join(DEP_PATH, f"{year} Deposits")
        if not os.path.exists(year_dir):
            os.makedirs(year_dir)

        destination_file = os.path.join(year_dir, f"Deposits for Client Trust {today_date_str}.xlsx")

        if os.path.exists(destination_file):
            raise FileExistsError(f"The file '{destination_file}' already exists. Please check the destination folder.")

        template_path = os.path.join(year_dir, 'template.xlsx')
        if not os.path.exists(template_path):
            raise FileNotFoundError("Template file not found")

        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        if df['amount'].isnull().any():
            raise ValueError("Amount conversion failed; non-numeric data found.")
        
        shutil.copy(template_path, destination_file)

        workbook = openpyxl.load_workbook(destination_file)

        sheet1 = workbook['Sheet1']
        sheet2 = workbook['Sheet2']

        row_sheet1 = 8
        row_sheet2 = 8
        spillover_occurred = False

        df = df.sort_values(by='last_name')
        grouped_data = df.groupby('type')

        totals = {
            "Sheet1": {"Cash": 0, "Check": 0, "Credit": 0},
            "Sheet2": {"Cash": 0, "Check": 0, "Credit": 0},
        }

        loop_number = 0
        inner_for_loop_number = 0

        for deposit_type, group in grouped_data:
            loop_number += 1
            current_sheet = sheet1
            current_row = row_sheet1

            if current_row + len(group) + 1 > 28:
                current_sheet = sheet2
                current_row = row_sheet2
                spillover_occurred = True

            type_start_row = current_row

            for _, data in group.iterrows():
                if pd.isna(data['first_name']) or pd.isna(data['last_name']) or pd.isna(data['type']) or pd.isna(data['amount']) or data['amount'] == 0:
                    print("Skipping empty or invalid data row.")
                    continue

                try:
                    print(f"Processing {data['first_name']} {data['last_name']}, Type: {deposit_type}, Amount: {data['amount']}")
                except Exception as e:
                    print(f"Error printing data: {e}")

                inner_for_loop_number += 1
                current_sheet[f'B{current_row}'].value = data['last_name']
                current_sheet[f'D{current_row}'].value = data['first_name']
                current_sheet[f'F{current_row}'].value = deposit_type
                current_sheet[f'H{current_row}'].value = data['amount']

                sheet_name = "Sheet1" if current_sheet == sheet1 else "Sheet2"
                totals[sheet_name][deposit_type] += data['amount']

                current_row += 1

            if current_row > type_start_row:
                current_sheet[f'H{current_row}'] = f"=SUM(H{type_start_row}:H{current_row - 1})"
                current_row += 2

            if current_sheet == sheet1:
                row_sheet1 = current_row
            else:
                row_sheet2 = current_row

        if spillover_occurred:
            sheet1['H30'].value = "Next Page →"

        for sheet_name, sheet in [("Sheet1", sheet1), ("Sheet2", sheet2)]:
            sheet['D31'].value = totals[sheet_name]["Cash"]
            sheet['F31'].value = totals[sheet_name]["Check"]
            sheet['D33'].value = totals[sheet_name]["Credit"]

            if sheet_name == "Sheet1":
                sheet['F33'].value = f"=D31+F31+D33+Sheet2!F33"
            else:
                sheet['F33'].value = f"=D31+F31+D33"

        workbook.save(destination_file)
        return {"message": "Deposit sheet created successfully", "status": "success"}
    except Exception as e:
        raise Exception(f"Failed to process deposit sheet: {str(e)}")
