import csv

input_file = r'C:\Users\Carlos Avila-Salazar\Desktop\booksRecAura\split1Clean.csv'
output_file = r'C:\Users\Carlos Avila-Salazar\Desktop\booksRecAura\ISBN1Clean.csv'

with open(input_file, mode='r', encoding='utf-8') as infile, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    for row in reader:
        # Write only the first field (assumed to be ISBN) to the output file
        if row:  # Ensure the row is not empty
            writer.writerow([row[0]])

print(f"ISBNs have been extracted to {output_file}.")
