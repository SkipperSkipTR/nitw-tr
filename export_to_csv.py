import os
import csv
import re

def extract_lines_from_file(file_path):
    """
    Reads a file and returns:
      - A list of tuples: (line_index, dialogue_text, line_id)
      - The full file content (list of lines) for later repacking.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Regex to match lines that end with " #line:<id>"
    pattern = re.compile(r'^(.*?)(\s*#line:(\w+))\s*$')
    extracted = []
    for index, line in enumerate(lines):
        match = pattern.match(line)
        if match:
            dialogue = match.group(1).strip()
            line_id = match.group(3)
            extracted.append((index, dialogue, line_id))
    return extracted, lines

def export_to_csv(directory, csv_file):
    """
    Recursively processes all .yarn.txt files in the specified directory,
    extracts lines with #line: markers, and writes them to a CSV file.
    The CSV will include the file's relative path for repacking later.
    """
    all_extracted = []
    # Walk through the directory recursively
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.yarn.txt'):
                file_path = os.path.join(root, file)
                extracted, _ = extract_lines_from_file(file_path)
                # Store the file's path relative to the base directory
                relative_path = os.path.relpath(file_path, directory)
                for line_num, dialogue, line_id in extracted:
                    all_extracted.append({
                        'filepath': relative_path,
                        'line_number': line_num,
                        'line_id': line_id,
                        'original_text': dialogue,
                        'translated_text': ''  # To be filled in after translation
                    })
    
    # Write extracted data to CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['filepath', 'line_number', 'line_id', 'original_text', 'translated_text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in all_extracted:
            writer.writerow(row)

if __name__ == '__main__':
    # Set these paths to match your project setup
    base_directory = './Unity_Assets_Files/'
    csv_output = 'extracted_lines.csv'
    export_to_csv(base_directory, csv_output)
