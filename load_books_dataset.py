import pandas as pd
import mysql.connector

# Load the dataset
df = pd.read_csv('books_dataset.csv')

# Normalize column names to lowercase
df.columns = df.columns.str.lower()

# Ensure required columns are present
required_columns = ['isbn', 'title', 'author', 'genre', 'publisher', 'publicationyear', 'pagecount']
if not all(column in df.columns for column in required_columns):
    raise ValueError(f"CSV file is missing one or more required columns: {required_columns}")

# Ask for MySQL Password
mySQLpassword = input("Please Enter Your MySQL Password: ") 

# Connect to the database
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password=mySQLpassword,  # Replace with your MySQL password
    database='book_reviews'
)
cursor = connection.cursor()

# Insert data into the database
for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO Books (isbn, title, author, genre, publisher, publication_year, page_count) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (row['isbn'], row['title'], row['author'], row['genre'], row['publisher'], row['publicationyear'], row['pagecount'])
    )

# Commit changes and close connection
connection.commit()
cursor.close()
connection.close()

print("Books dataset loaded successfully!")