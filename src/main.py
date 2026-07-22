"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

It uses the functional API in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    }

    print(
        "\nUser profile: "
        f"genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
        f"energy={user_prefs['energy']}, likes_acoustic={user_prefs['likes_acoustic']}"
    )

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} - {song['artist']}  (score: {score:.2f})")
        print(f"   Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
