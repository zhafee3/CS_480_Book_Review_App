from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    #(enter your password)'password': '',
    'database': 'book_database',
}

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/', methods=['GET', 'POST'])
def search_data():
    search_query = None
    rows = []

    # If the form is submitted
    if request.method == 'POST':
        search_query = request.form.get('search_query')

        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # SQL query with wildcard search
        query = """
        SELECT isbn, title, author, genre, publisher, publicationyear, pagecount
        FROM books
        WHERE isbn LIKE %s OR title LIKE %s OR author LIKE %s OR genre LIKE %s
        """
        like_query = f"%{search_query}%"
        cursor.execute(query, (like_query, like_query, like_query, like_query))

        # Fetch the results
        rows = cursor.fetchall()

        # Close the connection
        cursor.close()
        connection.close()

    # Render the HTML template
    return render_template('search.html', search_query=search_query, rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
