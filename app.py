from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)


def process_data(anilist_id):
    import fetch_anime_data_by_user
    fetch_anime_data_by_user.fetch_data(anilist_id)


@app.route("/", methods=['GET', 'POST'])
def anilist():
    if request.method == 'POST':
        anilist_id = request.form.get('anilist_id')
        socketio.emit('start_processing', namespace='/loader')
        process_data(anilist_id)
        socketio.emit('stop_processing', namespace='/loader')
        return redirect(url_for('dashboard'))
    return render_template('home.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True, use_reloader=False, allow_unsafe_werkzeug=True)
