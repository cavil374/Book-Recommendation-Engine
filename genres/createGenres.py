import openai
import pandas as pd
import re
import time

# Initialize OpenAI API key
openai.api_key = '[INSERT API KEY HERE]'

def extract_genres(response_text):
    # Use a regular expression to find genre lines
    genre_lines = re.findall(r'\d+\.\s*(.*)', response_text)
    return genre_lines[:3]  # Return the first 3 genres

def predict_genres(isbn):
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Suggest 3 genres for the book with ISBN {isbn}. Do not give any description. Only the genres."}
            ]
        )
        response_text = response.choices[0].message.content.strip()
        genres = extract_genres(response_text)
        
        # If no genres are returned, print the raw response for debugging
        if not genres:
            print(f"Warning: No genres found for ISBN {isbn}. Response was: '{response_text}'")
        
        return genres
    except Exception as e:
        print(f"Error with ISBN {isbn}: {e}")
        return [None, None, None]

# Load the existing CSV
input_csv_path = r'C:\Users\Carlos Avila-Salazar\Desktop\booksRecAura\ISBN1Clean.csv'
df = pd.read_csv(input_csv_path)

# Initialize new columns
df['Genre'] = None
df['Genre1'] = None
df['Genre2'] = None
df['Genre3'] = None

# Process in batches to manage rate limits
batch_size = 50  # Adjust batch size as needed
num_rows = df.shape[0]
print(f"Total rows to process: {num_rows}")

for start in range(0, num_rows, batch_size):
    end = min(start + batch_size, num_rows)
    batch = df.iloc[start:end]
    
    print(f"Processing batch {start // batch_size + 1} (rows {start + 1} to {end})")
    
    for index, row in batch.iterrows():
        isbn = row['ISBN']
        print(f"  Processing ISBN: {isbn}")
        genres = predict_genres(isbn)
        if len(genres) >= 3:
            df.at[index, 'Genre'] = genres[0]
            df.at[index, 'Genre1'] = genres[1] if len(genres) > 1 else None
            df.at[index, 'Genre2'] = genres[2] if len(genres) > 2 else None
            df.at[index, 'Genre3'] = genres[2] if len(genres) > 2 else None

    # Optional: Add a delay between batches to handle rate limits
    print(f"Batch {start // batch_size + 1} completed. Pausing for 10 seconds...")
    time.sleep(10)  # Sleep for 10 seconds between batches

# Save to new CSV
output_csv_path = r'C:\Users\Carlos Avila-Salazar\Desktop\booksRecAura\genresList.csv'
df.to_csv(output_csv_path, index=False)
print(f"Processing complete. Results saved to {output_csv_path}")
