from flask import Flask, render_template, request
from fetch_anime_data_by_user import fetch_data_for_user

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    user_id = request.form['user_id']
    fetch_data_for_user(user_id)
    return render_template('result.html', user_id=user_id)

if __name__ == '__main__':
    app.run(debug=True)
