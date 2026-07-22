import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

# --- Algorithm Recipe weights (see README "Finalized Algorithm Recipe") ---
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.5
ACOUSTIC_WEIGHT = 0.5
ACOUSTIC_THRESHOLD = 0.5  # songs at/above this acousticness count as "acoustic"

# Columns in songs.csv that must be numbers so we can do math on them.
FLOAT_FIELDS = ("energy", "valence", "danceability", "acousticness")
INT_FIELDS = ("id", "tempo_bpm")


@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """Object-oriented wrapper around the scoring and ranking logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k Song objects ranked by how well they fit the user."""
        prefs = _profile_to_prefs(user)
        scored = [(song, score_song(prefs, asdict(song))[0]) for song in self.songs]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, _score in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string of the reasons this song scored as it did."""
        _score, reasons = score_song(_profile_to_prefs(user), asdict(song))
        return "; ".join(reasons) if reasons else "No strong matches"


def _profile_to_prefs(user: UserProfile) -> Dict:
    """Translate a UserProfile dataclass into the prefs dict the scorer expects."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs.csv into a list of dicts, converting numeric columns to numbers."""
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in INT_FIELDS:
                row[field] = int(row[field])
            for field in FLOAT_FIELDS:
                row[field] = float(row[field])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user prefs, returning (score, list of reason strings)."""
    score = 0.0
    reasons: List[str] = []

    if user_prefs.get("genre") == song.get("genre"):
        score += GENRE_WEIGHT
        reasons.append(f"genre match (+{GENRE_WEIGHT})")

    if user_prefs.get("mood") == song.get("mood"):
        score += MOOD_WEIGHT
        reasons.append(f"mood match (+{MOOD_WEIGHT})")

    target_energy = user_prefs.get("energy")
    if target_energy is not None:
        closeness = 1 - abs(song.get("energy", 0.0) - target_energy)
        energy_points = closeness * ENERGY_WEIGHT
        score += energy_points
        reasons.append(f"energy close to target (+{energy_points:.2f})")

    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None:
        song_is_acoustic = song.get("acousticness", 0.0) >= ACOUSTIC_THRESHOLD
        if song_is_acoustic == likes_acoustic:
            score += ACOUSTIC_WEIGHT
            reasons.append(f"acoustic preference match (+{ACOUSTIC_WEIGHT})")

    return score, reasons


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """Score every song, rank highest-first, and return the top-k with explanations."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "No strong matches"
        scored.append((song, score, explanation))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
