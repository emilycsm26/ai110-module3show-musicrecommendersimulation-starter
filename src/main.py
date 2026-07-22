"""
Command line runner for the Music Recommender Simulation.

Runs the recommender against several user profiles so we can stress-test the
scoring logic and compare behavior across very different tastes.

It uses the functional API in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

# Each profile is a named taste dictionary. The first three are "normal" tastes;
# the last two are adversarial / edge cases designed to try to trick the scorer.
PROFILES = {
    "High-Energy Pop": {
        "genre": "pop", "mood": "happy", "energy": 0.9, "likes_acoustic": False,
    },
    "Chill Lofi": {
        "genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False,
    },
    # Adversarial: conflicting signals -- wants high energy but a "sad" mood,
    # and claims to like acoustic. Very few songs are both loud AND sad.
    "Conflicted (loud + sad)": {
        "genre": "classical", "mood": "sad", "energy": 0.9, "likes_acoustic": True,
    },
    # Edge case: genre and mood that do not exist in the catalog at all, so no
    # categorical points can ever be awarded -- ranking falls back to energy only.
    "Ghost Taste (no matches)": {
        "genre": "k-pop", "mood": "dreamy", "energy": 0.5, "likes_acoustic": False,
    },
}


def print_recommendations(name: str, user_prefs: dict, songs: list) -> None:
    """Print the top-5 recommendations for a single named profile."""
    print(f"\n=== Profile: {name} ===")
    print(
        f"prefs: genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
        f"energy={user_prefs['energy']}, likes_acoustic={user_prefs['likes_acoustic']}"
    )
    for rank, (song, score, explanation) in enumerate(
        recommend_songs(user_prefs, songs, k=5), start=1
    ):
        print(f"{rank}. {song['title']} - {song['artist']}  (score: {score:.2f})")
        print(f"   Because: {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, prefs in PROFILES.items():
        print_recommendations(name, prefs, songs)


if __name__ == "__main__":
    main()
