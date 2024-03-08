from flask import Flask, render_template, request, redirect, url_for
from fetch_anime_data_by_user import FetchAnimeDataByUser
from waitress import serve

app = Flask(__name__)

anilist_fetcher = None


def process_data(anilist_id):
    global anilist_fetcher
    anilist_fetcher = FetchAnimeDataByUser(anilist_id)
    anilist_fetcher.fetch_data()


@app.route('/', methods=['GET', 'POST'])
def anilist():
    if request.method == 'POST':
        anilist_id = request.form.get('anilist_id')
        process_data(anilist_id)
        return redirect(url_for('dashboard'))
    return render_template('home.html')


@app.route('/dashboard')
def dashboard():
    return render_template(
        'dashboard.html',
        image1=anilist_fetcher.cover_image_1,
        image2=anilist_fetcher.cover_image_2,
        u_score_max=anilist_fetcher.score_max,
        u_score_min=anilist_fetcher.score_min,
        avg_score_max=anilist_fetcher.avg_max,
        avg_score_min=anilist_fetcher.avg_min,
        title_max=anilist_fetcher.title_max,
        title_min=anilist_fetcher.title_min
    )


mode = "prod"

if __name__ == '__main__':
    if mode == "dev":
        app.run(host='0.0.0.0', debug=True)
    else:
        serve(app, host='0.0.0.0', port=50100, threads=2)
