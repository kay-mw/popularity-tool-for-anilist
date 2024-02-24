from flask import Flask, render_template, request, redirect, url_for
import jsonpickle

app = Flask(__name__)


def set_anilist_id(anilist_id):
    with open('anilist_id.txt', 'w') as file:
        file.write(jsonpickle.encode(anilist_id))


def get_anilist_id():
    try:
        with open('anilist_id.txt', 'r') as file:
            return jsonpickle.decode(file.read())
    except FileNotFoundError:
        return None


@app.route("/", methods=['GET', 'POST'])
def anilist():
    if request.method == 'POST':
        anilist_id = request.form.get('anilist_id')
        set_anilist_id(anilist_id)
        return redirect(url_for('anilist'))
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
