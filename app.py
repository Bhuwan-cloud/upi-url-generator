import secrets
from flask import Flask, redirect, request, render_template

app = Flask(__name__)

# Store generated links and their shortened URLs
upi_links = {}

# Function to generate a dynamic shortened URL using a random 10-character alphanumeric string
def shorten_url(upi_url):
    # Generate a secure random 10-character alphanumeric string
    short_hash = secrets.token_hex(5)  # Generates 10 characters (5 bytes)
    return short_hash  # Just the 10-character hash, no domain

# Home page with a form to generate UPI payment URL
@app.route('/')
def home():
    return render_template('index.html', upi_links=upi_links)

# Generate UPI payment URL, its shortened version, and return them to the frontend
@app.route('/generate', methods=['POST'])
def generate():
    # Get form data
    upi_id = request.form.get('upi_id')
    amount = request.form.get('amount')
    person_name = request.form.get('person name')

    # Generate UPI payment URL
    upi_url = f"upi://pay?pa={upi_id}&am={amount}&tn={person_name}"

    # Generate shortened URL (10-character hash)
    shortened_url = shorten_url(upi_url)

    # Add to generated links dictionary
    upi_links[shortened_url] = {"upi_id": upi_id, "amount": amount, "person name": person_name, "upi_url": upi_url}

    # Return to home page with generated links
    return render_template('index.html', upi_links=upi_links)

# Display the custom payment page for the shortened URL
@app.route('/<shortened_hash>')
def payment_page(shortened_hash):
    # Check if the shortened hash exists
    if shortened_hash in upi_links:
        # Retrieve the full UPI URL and payment details
        payment_details = upi_links[shortened_hash]
        return render_template('payment_page.html', payment_details=payment_details)
    else:
        # If hash not found, return a 404 or an error page
        return "Shortened URL not found.", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
