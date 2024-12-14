from flask import Flask, jsonify, request
import requests

def fetch_movie_details(imdb_id):
    """ Fetch movie details from TMDB or IMDb API (placeholder) """
    # Replace the URL with your TMDB API endpoint and key
    return {
        "imdb_id": imdb_id,
        "title": f"Movie for {imdb_id}",
    }

def fetch_tv_details(imdb_id):
    """ Fetch TV series details from TMDB or IMDb API (placeholder) """
    return {
        "imdb_id": imdb_id,
        "title": f"TV Show for {imdb_id}",
    }

def generate_embed_links(media_type, imdb_id, season=None, episode=None):
    """ Generate the embed link for a movie, TV series, or episode """
    base_url = "https://vidsrc.to/embed"

    if media_type == "movie":
        return f"{base_url}/movie/{imdb_id}"
    elif media_type == "tv":
        if season and episode:
            return f"{base_url}/tv/{imdb_id}/{season}/{episode}"
        elif season:
            return f"{base_url}/tv/{imdb_id}/{season}"
        else:
            return f"{base_url}/tv/{imdb_id}"
    return None

app = Flask(__name__)

# In-memory database
movies = []
tv_series = []

@app.route("/add/movie", methods=["POST"])
def add_movie():
    data = request.json
    imdb_id = data.get("imdb_id")
    if not imdb_id:
        return jsonify({"error": "IMDB ID is required"}), 400

    details = fetch_movie_details(imdb_id)
    embed_url = generate_embed_links("movie", imdb_id)

    movie = {
        "imdb_id": imdb_id,
        "title": details.get("title"),
        "embed_url": embed_url,
    }
    movies.append(movie)
    return jsonify(movie), 201

@app.route("/add/tv", methods=["POST"])
def add_tv():
    data = request.json
    imdb_id = data.get("imdb_id")
    season = data.get("season")
    episode = data.get("episode")

    if not imdb_id:
        return jsonify({"error": "IMDB ID is required"}), 400

    details = fetch_tv_details(imdb_id)
    embed_url = generate_embed_links("tv", imdb_id, season, episode)

    tv_show = {
        "imdb_id": imdb_id,
        "title": details.get("title"),
        "embed_url": embed_url,
    }
    tv_series.append(tv_show)
    return jsonify(tv_show), 201

@app.route("/movies", methods=["GET"])
def list_movies():
    return jsonify(movies), 200

@app.route("/tv-series", methods=["GET"])
def list_tv_series():
    return jsonify(tv_series), 200

if __name__ == "__main__":
    app.run(debug=True)
