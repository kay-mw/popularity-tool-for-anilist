from flask import Flask, render_template, request, redirect, url_for
import jsonpickle

app = Flask(__name__)


def process_data(anilist_id):
    import fetch_anime_data_by_user
    fetch_anime_data_by_user.fetch_data(anilist_id)


@app.route("/", methods=['GET', 'POST'])
def anilist():
    if request.method == 'POST':
        anilist_id = request.form.get('anilist_id')
        process_data(anilist_id)
        return redirect(url_for('anilist'))
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
