import pandas as pd
import json

# Define grade points dictionary
grade_points = {'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'C': 5, 'RA': 0, 'SA': 0, 'W': 0}

# Prompt the user to input the filenames separated by commas
filenames = input("Enter the filenames of the CSV files (separated by commas): ").split(',')
output = {}

if len(filenames) == 1:
    try:
        df = pd.read_csv(filenames[0].strip())
        
        gpa = (df['CREDITS'] * df['GRADE'].map(grade_points)).sum() / df[df['GRADE'].isin(grade_points.keys())]['CREDITS'].sum()
        
        output[filenames[0].strip()] = round(gpa, 2)
    except FileNotFoundError:
        output["error"] = f"File '{filenames[0].strip()}' not found."
    except Exception as e:
        output["error"] = f"An error occurred while processing '{filenames[0].strip()}': {str(e)}"
else:
    total_credits = 0
    total_grade_points = 0

    for filename in filenames:
        try:
            df = pd.read_csv(filename.strip())
        
            file_gpa = (df['CREDITS'] * df['GRADE'].map(grade_points)).sum() / df[df['GRADE'].isin(grade_points.keys())]['CREDITS'].sum()
        
            total_credits += df[df['GRADE'].isin(grade_points.keys())]['CREDITS'].sum()
            total_grade_points += (df['CREDITS'] * df['GRADE'].map(grade_points)).sum()
            
            total_credits = int(total_credits)
            total_grade_points = int(total_grade_points)
        
            output[filename.strip()] = {
                "GPA": round(file_gpa, 2),
                "Total Credits": total_credits
            }
        except FileNotFoundError:
            output[filename.strip()] = f"File '{filename.strip()}' not found"
        except Exception as e:
            output[filename.strip()] = f"An error occurred while processing '{filename.strip()}': {str(e)}"

    cgpa = round(total_grade_points / total_credits, 2)
    output["CGPA"] = cgpa

json_output = json.dumps(output, indent=4)
print(json_output)