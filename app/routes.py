from flask import request, render_template, request, redirect, url_for, Blueprint, session
from .api_request.fetch_anime_data_by_user import FetchAnimeDataByUser

main = Blueprint("main", __name__)

anilist_fetcher = None


def taste_message(avg_score_diff):
    if abs(avg_score_diff) > 10:
        return "Woah... are you trying to be controversial or something?"
    elif abs(avg_score_diff) > 5:
        return "You have pretty unpopular taste!"
    elif abs(avg_score_diff) > 2.5:
        return "You have kinda unpopular taste..."
    else:
        return "You have very popular taste!"


def score_diff_direction(true_score_diff):
    if true_score_diff > 0:
        return "Specifically, you tend to give more positive scores ヽ(*・ω・)ﾉ"
    else:
        return "Specifically, you tend to give harsher scores ・`ω´・"


def process_data(username):
    global anilist_fetcher
    anilist_fetcher = FetchAnimeDataByUser(username)
    anilist_fetcher.fetch_data()

    session_data = {
        'image1': anilist_fetcher.cover_image_1,
        'image2': anilist_fetcher.cover_image_2,
        'u_score_max': anilist_fetcher.score_max,
        'u_score_min': anilist_fetcher.score_min,
        'avg_score_max': anilist_fetcher.avg_max,
        'avg_score_min': anilist_fetcher.avg_min,
        'title_max': anilist_fetcher.title_max,
        'title_min': anilist_fetcher.title_min,
        'avg_score_diff': anilist_fetcher.avg_score_diff,
        'taste_message': taste_message(anilist_fetcher.avg_score_diff),
        'true_score_diff': anilist_fetcher.true_score_diff,
        'true_score_diff_msg': score_diff_direction(anilist_fetcher.true_score_diff)
    }

    session['username'] = session_data
    return session['username']


@main.route('/', methods=['GET', 'POST'])
def anilist():
    if request.method == 'POST':
        username = request.form.get('username')
        process_data(username)
        return redirect(url_for('main.dashboard'))
    return render_template('home.html')


@main.route('/dashboard')
def dashboard():
    if "username" in session:
        user_session_data = session['username']
        return render_template(
            'dashboard.html',
            image1=user_session_data['image1'],
            image2=user_session_data['image2'],
            u_score_max=user_session_data['u_score_max'],
            u_score_min=user_session_data['u_score_min'],
            avg_score_max=user_session_data['avg_score_max'],
            avg_score_min=user_session_data['avg_score_min'],
            title_max=user_session_data['title_max'],
            title_min=user_session_data['title_min'],
            avg_score_diff=user_session_data['avg_score_diff'],
            taste_message=user_session_data['taste_message'],
            true_score_diff=user_session_data['true_score_diff'],
            true_score_diff_msg=user_session_data['true_score_diff_msg']
        )
    else:
        return redirect(url_for('main.anilist'))
