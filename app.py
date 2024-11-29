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
    #'password': '',
    'database': 'book_reviews',
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
        SELECT isbn, title, author, genre, publisher, publicationyear, pagecount
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

if __name__ == '__main__':
    app.run(debug=True)
