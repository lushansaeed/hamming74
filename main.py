from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "some_secret_key"  # This is used for flash messages

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['data']
        if len(user_input) != 4 or any(bit not in ['0', '1'] for bit in user_input):
            flash("Invalid input. Please enter a 4-bit binary number.")
            return redirect(url_for('index'))

        data = [int(bit) for bit in user_input]
        result = generate_hamming74(data)
        return render_template('index.html', result=''.join(map(str, result)))

    return render_template('index.html', result=None)

def generate_hamming74(data):
    # Ensure the data is 4 bits long
    if len(data) != 4:
        raise ValueError("Expected a 4-bit data input")

    # Create an array of size 7 to hold the final encoded sequence
    encoded = [0] * 7

    # Place the data bits in their respective positions
    encoded[2] = data[0]
    encoded[4] = data[1]
    encoded[5] = data[2]
    encoded[6] = data[3]

    # Calculate the parity bits using the XOR operation for even parity

    # For P1 (covers positions 1, 3, 5, 7):
    encoded[0] = encoded[2] ^ encoded[4] ^ encoded[6]

    # For P2 (covers positions 2, 3, 6, 7):
    encoded[1] = encoded[2] ^ encoded[5] ^ encoded[6]

    # For P4 (covers positions 4, 5, 6):
    encoded[3] = encoded[4] ^ encoded[5] ^ encoded[6]

    return encoded[::-1]  # Return reversed list to correct the output order

if __name__ == "__main__":
    app.run(debug=True)
