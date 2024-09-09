import csv

# Input and output file paths
input_file = 'input.csv'
output_file = 'output.csv'

# Open the input and output files
with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    
    # Initialize csv reader and writer
    reader = csv.reader(infile, delimiter=';')
    writer = csv.writer(outfile, delimiter=',')
    
    # Read the header
    header = next(reader)
    
    # Remove double quotes from the header and write it to the output file
    header = [col.replace('""', '').replace('"', '') for col in header]
    writer.writerow(header)
    
    # Process the rows
    for row in reader:
        # Remove double quotes from each field in the row
        clean_row = [field.replace('""', '').replace('"', '') for field in row]
        writer.writerow(clean_row)

print("CSV file has been cleaned and saved as", output_file)
