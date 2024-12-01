import hashlib
import hmac

from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    #add your passward from mysql
    'password': '2004',
    'database': 'book_reviews',
    #'auth_plugin':'mysql_native_password'
}

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Hash password using hashlib
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Verify password
def verify_password(stored_password, provided_password):
    return hmac.compare_digest(stored_password, hash_password(provided_password))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Hash the password
        hashed_password = hash_password(password)

        # Debug: Print user details
        print(f"Attempting to register: {username}, {email}, {hashed_password}")

        # Insert the user into the database
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                "INSERT INTO Users (username, email_address, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )
            connection.commit()  # Commit changes to the database
            print("User successfully inserted into the database.")
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            # Debug: Log the error
            print(f"Database error: {err}")
            flash('Error: ' + str(err), 'danger')
        finally:
            cursor.close()
            connection.close()

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Debug: Print submitted email and password
        print(f"Email: {email}, Password: {password}")

        # Fetch user from the database
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE email_address = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        # Debug: Check if user is found
        if user:
            print(f"User found: {user}")
        else:
            print("No user found with that email.")

        # Verify password
        if user and verify_password(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            print("Login successful, redirecting to search_data.")
            return redirect(url_for('search_data'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            print("Invalid credentials.")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def search_data():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

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
        SELECT isbn, title, author, genre, publisher, publication_year, page_count
        FROM Books
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

@app.route('/advanced_search', methods=['GET', 'POST'])
def advanced_search():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

    search_query = None
    rows = []

    # If the form is submitted
    if request.method == 'POST':

        isbn = request.form.get('isbn', '').strip()
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        genre = request.form.get('genre', '').strip()
        publisher = request.form.get('publisher', '').strip()
        publication_year = request.form.get('publication_year', '').strip()
        min_page_count = request.form.get('min_page_count', '').strip()
        max_page_count = request.form.get('max_page_count', '').strip()
    
        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # SQL query with wildcard search
        query = """
        SELECT isbn, title, author, genre, publisher, publication_year, page_count
        FROM Books
        WHERE (%s = '' OR isbn LIKE %s)
          AND (%s = '' OR title LIKE %s)
          AND (%s = '' OR author LIKE %s)
          AND (%s = '' OR genre LIKE %s)
          AND (%s = '' OR publisher LIKE %s)
          AND (%s = '' OR publication_year = %s)
          AND (%s = '' OR page_count >= %s)
          AND (%s = '' OR page_count <= %s)
        """
        params = [
            isbn, f"%{isbn}%",
            title, f"%{title}%",
            author, f"%{author}%",
            genre, f"%{genre}%",
            publisher, f"%{publisher}%",
            publication_year, publication_year,
            min_page_count, min_page_count,
            max_page_count, max_page_count
        ]
        cursor.execute(query, params)

        # Fetch the results
        rows = cursor.fetchall()

        # Close the connection
        cursor.close()
        connection.close()

    # Render the HTML template
    return render_template('advanced_search.html', search_query=search_query, rows=rows)

@app.route('/add_review/<isbn>', methods=['GET', 'POST'])
def add_review(isbn):
    if 'user_id' not in session:
        flash('Please log in to leave a review.', 'warning')
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Books WHERE isbn = %s", (isbn,))
    book = cursor.fetchone()

    if not book:
        flash('Sorry, we could not fetch the book for some reason.', 'danger')
        return redirect(url_for('search_data'))
    
    if request.method == 'POST':
        rating = request.form.get('rating')
        written_review = request.form.get('written_review')

        if not rating or not rating.isdigit() or not (1 <= int(rating) <= 5):
            flash('Rating must be a number between 1 and 5.', 'danger')
        else:
            try:
                cursor.execute(
                    """
                    INSERT INTO Reviews (book_id, user_id, rating, written_review)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (isbn, session['user_id'], int(rating), written_review)
                )
                connection.commit()  
                flash('Review submitted successfully!', 'success')
                return redirect(url_for('search_data'))  # Redirect to search page
            except mysql.connector.Error as err:
                flash(f'Error submitting review: {err}', 'danger')

    cursor.close()
    connection.close()
    return render_template('add_review.html', book=book)


if __name__ == '__main__':
    app.run(debug=True)
