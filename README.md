# Anime Taste Tool (using AniList)

This is a basic web app/data pipeline that takes an AniList username and determines your most and least popular takes compared to the side-wide average.

To try it, you can use [this link](https://ani-pop.azurewebsites.net/).

Alternatively, you can run it locally using the following steps:

1. Clone the github repo.

`git clone https://github.com/kay-mw/anilist-popularity.git`

2. Change into the directory.

`cd /path/to/anilist-popularity`

3. Set up a virtual environment and activate it.

`python3 -m venv .venv`

`source .venv/bin/activate`

4. Install the required packages.

`pip install -r requirements.txt`

5. Run the local server.

`python3 startup.py`

6. Finally, type localhost:8000 in the search bar of your preferred browser and enjoy!
