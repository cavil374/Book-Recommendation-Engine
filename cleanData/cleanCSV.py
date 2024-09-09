import csv

# Input and output file paths
input_file = r'C:\Users\Carlos Avila-Salazar\Desktop\booksRecAura\split_1.csv'
output_file = r'C:\Users\Carlos Avila-Salazar\Desktop\booksRecAura\split1Clean.csv'

# Open the input and output files
with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    
    # Read the entire content of the file
    content = infile.read()
    
    # Replace semicolons with commas
    content = content.replace(';', ',')
    
    # Remove unnecessary quotes
    content = content.replace('""', '').replace('"', '')
    
    # Remove the comma after "&amp"
    content = content.replace('&amp,', '&amp')
    
    # Fix specific instances where the comma issue might split the publisher name
   # content = content.replace('Ryland Peters &amp, Small Ltd', 'Ryland Peters &amp Small Ltd')
    #content = content.replace('Mary-Kate &amp, Ashley', 'Mary-Kate &amp Ashley')
    
    # Write the cleaned content to the output file
    outfile.write(content)

print("CSV file has been cleaned and saved as", output_file)
