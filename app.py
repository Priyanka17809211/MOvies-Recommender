from flask import Flask, render_template, request, redirect, url_for, jsonify
import pickle
import pandas as pd
import re
import requests

app = Flask(__name__)

# Load trained recommendation model
model = pickle.load(open("movie_recommender.pkl", "rb"))  # Load recommendation model
movies_df = pd.read_csv("movies.csv")  # Load movies dataset

# TMDB API Key (Replace with your API key)
TMDB_API_KEY = "81a12d39554979ad96715cf3c8f16610"

# Temporary storage for user IDs (In real case, use a database)
users = set()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create_user", methods=["POST"])
def create_user():
    user_id = request.form.get("user_id")
    if user_id and user_id.isdigit() and len(user_id) == 3:
        users.add(user_id)  # Store user ID
        return redirect(url_for("home"))  # Redirect back to homepage
    return "Invalid User ID. Must be a 3-digit number.", 400

@app.route('/movies')
def movies():
    return render_template('movies.html')

# Function to clean & match movie names dynamically
def find_movie_in_dataset(user_input):
    user_input = user_input.strip().lower()

    for movie in movies_df["title"]:
        cleaned_title = re.sub(r"\(\d{4}\)", "", movie).strip().lower()
        if user_input == cleaned_title:
            return movie  # Return exact movie title with the year

    return None  # No match found


# Function to get movie details from TMDB
def get_movie_details_from_tmdb(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
    response = requests.get(url).json()

    if response.get("results"):
        movie_info = response["results"][0]  # Get first search result
        return {
            "id": movie_info["id"],
            "title": movie_info["title"],
            "overview": movie_info["overview"],
            "poster": f"https://image.tmdb.org/t/p/w500{movie_info['poster_path']}" if movie_info["poster_path"] else None
        }

    return None  # No details found


# Function to get recommendations from the model
def get_recommendations(movie_name):
    if movie_name in model:
        return model[movie_name]  # Assuming model gives a list of recommended movies

    return None  # Model does not have recommendations


# Function to get recommended movies' posters & details
def get_movie_posters_and_details(movie_list):
    movies_info = []
    for movie in movie_list:
        movie_data = get_movie_details_from_tmdb(movie)
        if movie_data:
            movies_info.append(movie_data)
    return movies_info


@app.route("/recommend", methods=["GET"])
def recommend():
    user_query = request.args.get("movie")
    if not user_query:
        return jsonify({"error": "Movie name is required"}), 400

    # Step 1: Search movie in dataset
    matched_movie = find_movie_in_dataset(user_query)

    if matched_movie:
        # Step 2: Get recommendations from model
        recommendations = get_recommendations(matched_movie)

        if recommendations:
            # Step 3: Fetch poster & details for recommended movies
            recommended_movies_info = get_movie_posters_and_details(recommendations)

            return jsonify({
                "searched_movie": matched_movie,
                "recommendations": recommended_movies_info
            })

    # Step 4: If model fails, get recommendations directly from TMDB
    movie_details = get_movie_details_from_tmdb(user_query)

    if movie_details:
        tmdb_movie_id = movie_details["id"]
        tmdb_recommend_url = f"https://api.themoviedb.org/3/movie/{tmdb_movie_id}/recommendations?api_key={TMDB_API_KEY}"
        tmdb_recommendations = requests.get(tmdb_recommend_url).json()

        recommended_movies_info = []
        if tmdb_recommendations.get("results"):
            for movie in tmdb_recommendations["results"][:5]:  # Get top 5 recommendations
                recommended_movies_info.append({
                    "title": movie["title"],
                    "overview": movie["overview"],
                    "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie["poster_path"] else None
                })

        return jsonify({
            "searched_movie": movie_details["title"],
            "recommendations": recommended_movies_info
        })

    return jsonify({"error": "Movie not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
