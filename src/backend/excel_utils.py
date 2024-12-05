from dotenv import load_dotenv
import pandas as pd
import openpyxl
from datetime import datetime
import shutil
import os

load_dotenv()

def create_deposits_sheet(df):
    try:
        print("Made it this far 1.")
        print(df)
        DEP_PATH = os.getenv("DEPOSITS_PATH")

        if DEP_PATH is None:
            raise ValueError("DEPOSITS_PATH environment variable is not set.")

        print("Made it this far 2.")

        today_date = datetime.now().strftime('%m-%d-%y')
        destination_file = os.path.join(DEP_PATH, f"Deposits for Client Trust {today_date}.xlsx")

        # Check if template exists
        template_path = os.path.join(DEP_PATH, 'template.xlsx')
        if not os.path.exists(template_path):
            raise FileNotFoundError("Template file not found")

        print("Made it this far 3.")

        # Ensure the 'amount' column is numeric
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        if df['amount'].isnull().any():
            raise ValueError("Amount conversion failed; non-numeric data found.")
        
        print("Made it this far 4.")

        shutil.copy(template_path, destination_file)

        print("Made it this far 5.")

        workbook = openpyxl.load_workbook(destination_file)
        print("Made it this far 6.")

        sheet1 = workbook['Sheet1']
        sheet2 = workbook['Sheet2']

        row_sheet1 = 8  # Start data entry on Sheet1 from row 8
        row_sheet2 = 8  # Start data entry on Sheet2 from row 8 if spillover occurs
        spillover_occurred = False  # Flag to track if spillover happens

        # Group the data by type
        grouped_data = df.groupby('type')
        grouped_data = df.groupby('type')
        print("Grouped Data Info:")
        for deposit_type, group in grouped_data:
            print(f"Group: {deposit_type}")
            print(group.head())
        print("Made it this far 7.")

        # Initialize totals for both sheets
        totals = {
            "Sheet1": {"Cash": 0, "Check": 0, "Credit": 0},
            "Sheet2": {"Cash": 0, "Check": 0, "Credit": 0},
        }

        print("Made it this far 8.")

        loop_number = 0
        inner_for_loop_number = 0

        # Populate data into sheets
        for deposit_type, group in grouped_data:
            print(f"Made it this far. Outer loop: {loop_number}")
            loop_number += 1
            current_sheet = sheet1
            current_row = row_sheet1

            # Check if data will exceed Sheet1 limits
            if current_row + len(group) + 1 > 28:
                current_sheet = sheet2
                current_row = row_sheet2
                spillover_occurred = True  # Mark that spillover occurred

            type_start_row = current_row

            for _, data in group.iterrows():
                # Skip rows with empty essential data
                if pd.isna(data['first_name']) or pd.isna(data['last_name']) or pd.isna(data['type']) or pd.isna(data['amount']) or data['amount'] == 0:
                    print("Skipping empty or invalid data row.")
                    continue  # Skip to the next iteration of the loop

                print(f"Made it this far. Inner loop: {inner_for_loop_number}")
                try:
                    print(f"Processing {data['first_name']} {data['last_name']}, Type: {deposit_type}, Amount: {data['amount']}")
                except Exception as e:
                    print(f"Error printing data: {e}")

                inner_for_loop_number += 1
                current_sheet[f'B{current_row}'].value = data['last_name']
                current_sheet[f'D{current_row}'].value = data['first_name']
                current_sheet[f'F{current_row}'].value = deposit_type
                current_sheet[f'H{current_row}'].value = data['amount']

                # Update totals
                sheet_name = "Sheet1" if current_sheet == sheet1 else "Sheet2"
                totals[sheet_name][deposit_type] += data['amount']

                current_row += 1

            # Add type total
            if current_row > type_start_row:
                current_sheet[f'H{current_row}'] = f"=SUM(H{type_start_row}:H{current_row - 1})"
                current_row += 2

            # Update row tracker
            if current_sheet == sheet1:
                row_sheet1 = current_row
            else:
                row_sheet2 = current_row


        # If spillover occurred, add "Next Page" message to Sheet1
        if spillover_occurred:
            sheet1['H30'].value = "Next Page →"

        # Write totals and formulas
        for sheet_name, sheet in [("Sheet1", sheet1), ("Sheet2", sheet2)]:
            sheet['D31'].value = totals[sheet_name]["Cash"]
            sheet['F31'].value = totals[sheet_name]["Check"]
            sheet['D33'].value = totals[sheet_name]["Credit"]

            # Grand Total Formula
            if sheet_name == "Sheet1":
                sheet['F33'].value = f"=D31+F31+D33+Sheet2!F33"
            else:
                sheet['F33'].value = f"=D31+F31+D33"
        print("Made it this far 9.")
        workbook.save(destination_file)
        print("Made it this far 10.")
        return {"message": "Deposit sheet created successfully", "status": "success"}
    except Exception as e:
        # Raise with an appropriate error message and let the caller handle it
        raise Exception(f"Failed to process deposit sheet: {str(e)}")
