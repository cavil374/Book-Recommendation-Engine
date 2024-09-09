import csv
import random

# Function to assign a taste profile to each user
def assign_taste_profile():
    profiles = [
        'Generalist', 
        'Sci-Fi Lover', 
        'History Buff', 
        'Literature Enthusiast', 
        'Fantasy Fanatic',
        'Horror Enthusiast'  # Added Horror Enthusiast profile
    ]
    return random.choice(profiles)

# Function to generate a rating based on taste profile and genre
def generate_rating(taste_profile, genres):
    # Default rating range
    rating = random.randint(1, 10)
    
    # Adjust rating based on taste profile
    if taste_profile == 'Sci-Fi Lover':
        if any(genre in genres for genre in ['Science Fiction', 'Dystopian Fiction', 'Space Opera']):
            rating = random.randint(7, 10)
        else:
            rating = random.randint(1, 7)
    
    elif taste_profile == 'History Buff':
        if any(genre in genres for genre in ['History', 'Historical Fiction', 'Military History', 'American Civil War']):
            rating = random.randint(7, 10)
        else:
            rating = random.randint(1, 7)
    
    elif taste_profile == 'Literature Enthusiast':
        if any(genre in genres for genre in ['Literary Fiction', 'Drama', 'Classic Literature', 'Contemporary Fiction']):
            rating = random.randint(7, 10)
        else:
            rating = random.randint(1, 7)
    
    elif taste_profile == 'Fantasy Fanatic':
        if any(genre in genres for genre in ['Fantasy', 'Adventure', 'Urban Fantasy', 'Epic Fiction']):
            rating = random.randint(7, 10)
        else:
            rating = random.randint(1, 7)
    
    elif taste_profile == 'Horror Enthusiast':
        if any(genre in genres for genre in ['Horror', 'Thriller', 'Gothic Fiction', 'Supernatural Fiction']):
            rating = random.randint(7, 10)
        else:
            rating = random.randint(1, 7)
    
    # Generalist: no adjustment needed, rates everything equally
    
    return rating

# Function to generate mock user data with increased overlap for similar profiles
def generate_user_data(input_csv_file, output_csv_file):
    # Open the input CSV file
    with open(input_csv_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        books = list(reader)
    
    # Generate 50 unique user IDs with taste profiles
    user_profiles = [{'User_ID': user_id, 'Taste_Profile': assign_taste_profile()} for user_id in range(100001, 101051)]
    random.shuffle(user_profiles)  # Shuffle to randomize user IDs
    
    # Group users by taste profile to increase overlap
    users_by_profile = {}
    for user in user_profiles:
        profile = user['Taste_Profile']
        if profile not in users_by_profile:
            users_by_profile[profile] = []
        users_by_profile[profile].append(user)
    
    # Open the output CSV file for writing
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['User_ID', 'ISBN', 'Book_Rating']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for profile, users in users_by_profile.items():
            # Select a common subset of books to increase overlap
            common_books_to_rate = random.sample(books, min(60, len(books)))

            for user in users:
                user_id = user['User_ID']
                
                # Randomly determine additional books to rate
                num_books_to_rate = random.randint(10, min(60, len(books)))
                
                # Combine common books with random selection
                selected_books = common_books_to_rate + random.sample(books, num_books_to_rate)

                for book in selected_books:
                    # Gather all genres of the book
                    genres = [book['Genre'], book['Genre1'], book['Genre2'], book['Genre3']]
                    
                    # Generate a rating based on the user's taste profile
                    book_rating = generate_rating(user['Taste_Profile'], genres)
                    
                    writer.writerow({'User_ID': user_id, 'ISBN': book['ISBN'], 'Book_Rating': book_rating})

# Input CSV file name (contains book data)
input_csv_file = r'C:\Users\Carlos Avila-Salazar\Desktop\booksRecAura\genresList.csv'
# Output CSV file name (will contain generated user data)
output_csv_file = r'C:\Users\Carlos Avila-Salazar\Desktop\booksRecAura\auraUsers.csv'

# Generate the user data
generate_user_data(input_csv_file, output_csv_file)

print(f"User data generated and saved to {output_csv_file}")
