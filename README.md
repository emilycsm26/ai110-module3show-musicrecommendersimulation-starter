# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version is a **content-based** music recommender. It stores a small catalog of songs (with attributes like genre, mood, and energy) and a single user "taste profile," then scores every song by how closely it matches that profile. It ranks the songs by score and returns the top matches, along with a short explanation of *why* each one was picked. There are no other users involved, so it recommends purely from the songs' own attributes.

---

## How The System Works

### How real systems do it at scale

Big streaming platforms like Spotify and YouTube predict what you'll love next
using two main strategies:

- **Collaborative filtering** uses *other users' behavior* — "listeners who liked
  the songs you like also played this one." It's great for discovery, but it
  struggles with brand-new songs or brand-new users that have no history yet
  (the "cold-start" problem).
- **Content-based filtering** uses the *song's own attributes* — tempo, energy,
  mood, genre — and finds songs similar to the ones you already play. It works
  from day one and is easy to explain, but it tends to keep giving you more of
  the same (a "filter bubble").

Real systems combine both, along with signals like likes, skips, replays,
playlist adds, and listen-through time. **My simulation is content-based only**,
because there is just one user and no crowd behavior to learn from.

### What my version prioritizes

My recommender prioritizes matching the user's **genre and mood** first (the
strongest, most stable signals of taste), then fine-tunes with how close a song's
**energy** is to what the user wants. Genre is weighted highest because it's the
coarsest identity of taste; mood and the numeric "vibe" features refine the result.

### Features each `Song` uses

The `Song` object stores: `id`, `title`, `artist`, `genre`, `mood`, `energy`,
`tempo_bpm`, `valence`, `danceability`, and `acousticness`. My scoring focuses on
**genre, mood, energy, and acousticness** as the most effective simple signals.

### What the `UserProfile` stores

- `favorite_genre` — the user's preferred genre (e.g. `pop`)
- `favorite_mood` — the user's preferred mood (e.g. `happy`)
- `target_energy` — the energy level they want, `0.0`–`1.0`
- `likes_acoustic` — whether they prefer acoustic tracks (`True`/`False`)

### Finalized Algorithm Recipe (Scoring Rule)

For each song, the score adds up weighted points:

| Feature   | Rule                                              | Points   |
|-----------|---------------------------------------------------|----------|
| genre     | exact match with `favorite_genre`                 | +2.0     |
| mood      | exact match with `favorite_mood`                  | +1.0     |
| energy    | `(1 − abs(song.energy − target_energy)) × 1.5`    | 0 → +1.5 |
| acoustic  | `song.acousticness ≥ 0.5` agrees with `likes_acoustic` | +0.5 |

Numeric features (energy) reward **closeness**, not bigger values: a song near the
user's `target_energy` scores higher than one that's far away in either direction.
Genre is weighted at 2× mood because genre is the more stable, primary signal of
taste, while mood cuts across genres and acts as a refinement.

**Example user profile used for testing:**

```python
user_prefs = {
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.9,
    "likes_acoustic": False,
}
```

### Potential biases I expect

- **Genre over-prioritization.** Because genre is worth the most, the system may
  ignore a song that perfectly matches the user's mood and energy just because its
  genre label is different (e.g. skipping an intense metal track for a rock fan).
- **No sense of similar genres.** Only exact genre matches score, so musically
  adjacent styles get zero credit — the model has no notion of "close" genres.
- **Narrow single-value profile.** One favorite genre and one mood can't express
  users who like several things, so the catalog gets sorted around one taste axis.
- **Popularity/coverage bias.** With a tiny catalog and hard weights, a few songs
  will almost always float to the top for a given profile, and quieter matches
  rarely surface.

### How I choose which songs to recommend (Ranking Rule)

The **Scoring Rule** answers "how well does *this one song* fit?" The **Ranking
Rule** scores *every* song, sorts them from highest to lowest, and returns the
top `k`. I need both: scoring makes songs comparable, and ranking turns those
scores into an actual choice.

```
Recommendation flow:
  songs.csv ──▶ [Song objects]
  user      ──▶  UserProfile
                     │
                     ▼
        score each song (Scoring Rule)
                     │
                     ▼
        sort by score, take top k (Ranking Rule)
                     │
                     ▼
          top recommendations + reasons
```

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Below is real terminal output from `python -m src.main` using the default
`pop / happy / energy 0.8` profile against the 18-song catalog:

```
Loaded songs: 18

User profile: genre=pop, mood=happy, energy=0.8, likes_acoustic=False

Top recommendations:

1. Sunrise City - Neon Echo  (score: 4.97)
   Because: genre match (+2.0); mood match (+1.0); energy close to target (+1.47); acoustic preference match (+0.5)

2. Gym Hero - Max Pulse  (score: 3.80)
   Because: genre match (+2.0); energy close to target (+1.30); acoustic preference match (+0.5)

3. Rooftop Lights - Indigo Parade  (score: 2.94)
   Because: mood match (+1.0); energy close to target (+1.44); acoustic preference match (+0.5)

4. Concrete Kings - Rhyme Theory  (score: 1.93)
   Because: energy close to target (+1.43); acoustic preference match (+0.5)

5. Night Drive Loop - Neon Echo  (score: 1.92)
   Because: energy close to target (+1.42); acoustic preference match (+0.5)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



