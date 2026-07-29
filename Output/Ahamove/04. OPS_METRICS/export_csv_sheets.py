import pandas as pd
import openpyxl

excel_path = "/Users/ts-1148/Desktop/Pulu-workspace/Output/Ahamove/04. OPS_METRICS/2026-07-DM-QM-Tag-Management-System.xlsx"
wb = openpyxl.load_workbook(excel_path, data_only=True)

for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    data = sheet.values
    cols = next(data)
    data = list(data)
    
    # Filter out empty title rows at top if any
    df = pd.DataFrame(data, columns=cols)
    csv_filename = f"/Users/ts-1148/Desktop/Pulu-workspace/Output/Ahamove/04. OPS_METRICS/export_{sheet_name}.csv"
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    print(f"Exported: {csv_filename}")
