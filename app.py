from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    custom_data = "Hello, World! Welcome to my Flask app."
    return render_template('index.html', data=custom_data)

if __name__ == '__main__':
    app.run(debug=True)

