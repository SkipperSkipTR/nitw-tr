import os
import csv
import re

def load_translations(csv_file):
    """
    Reads the CSV file and returns a dictionary mapping keys (filename, line_number, line_id)
    to the translated text. If no translation is provided, it falls back to the original text.
    """
    translations = {}
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = (row['filename'], int(row['line_number']), row['line_id'])
            # Use the translated text if available; otherwise, keep the original
            translations[key] = row['translated_text'].strip() or row['original_text']
    return translations

def repack_file(file_path, translations, filename):
    """
    Reads a single file, replaces the dialogue text on matching lines with the translated version,
    and writes back the content.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Regex to find lines with the #line: marker
    pattern = re.compile(r'^(.*?)(\s*#line:(\w+))\s*$')
    for index, line in enumerate(lines):
        match = pattern.match(line)
        if match:
            line_id = match.group(3)
            key = (filename, index, line_id)
            if key in translations:
                # Replace original dialogue with the translated text while keeping the marker
                new_dialogue = translations[key]
                new_line = f"{new_dialogue}{match.group(2)}\n"
                lines[index] = new_line

    # Write the updated content back to the file (or you could write to a new file)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def repack_directory(directory, csv_file):
    """
    Loads translations from CSV and repacks all .yarn.txt files in the directory.
    """
    translations = load_translations(csv_file)
    for filename in os.listdir(directory):
        if filename.endswith('.yarn.txt'):
            file_path = os.path.join(directory, filename)
            repack_file(file_path, translations, filename)

if __name__ == '__main__':
    # Ensure these paths match your setup
    directory = 'path/to/your/yarn/files'
    csv_file = 'extracted_lines.csv'
    repack_directory(directory, csv_file)
