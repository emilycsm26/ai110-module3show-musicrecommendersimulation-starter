# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

---

## 2. Intended Use  

VibeFinder recommends songs from a small catalog based on a user's taste profile.
It assumes the user has one favorite genre, one favorite mood, a target energy
level, and a yes/no acoustic preference. It is built for classroom exploration,
not real users.

---

## 3. How the Model Works  

The model looks at each song's genre, mood, energy, and acousticness. It compares
those to what the user asked for and awards points for each match. A matching
genre is worth the most (2 points), a matching mood is worth 1 point, and songs
whose energy is close to the user's target earn up to 1.5 more points. Songs that
match the user's acoustic preference get a small 0.5 bonus. Every song gets a
total score, and the highest scores are recommended first. Compared to the
starter code, I filled in the empty scoring and ranking logic and expanded the
catalog from 10 to 18 songs.

---

## 4. Data  

The catalog has 18 songs. Genres include pop, lofi, rock, jazz, ambient,
synthwave, indie pop, hip hop, classical, EDM, country, R&B, metal, reggae, and
folk. Moods range from happy and chill to intense, sad, romantic, and aggressive.
I added 8 songs to the original 10 to widen the variety. Musical taste is still
narrow: there are no lyrics, languages, decades, or regional styles, and each
genre only has a song or two.

---

## 5. Strengths  

The system works well for users with clear, consistent tastes. The Chill Lofi and
Deep Intense Rock profiles returned exactly the songs I expected at the top. The
energy score correctly separates loud songs from calm ones, so a workout profile
and a study profile get almost opposite lists. When a profile is well-aligned,
the top pick usually matches my own intuition.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly.

**Weakness discovered during experiments:** the genre weight (+2.0) can
overpower the energy score, so a song that is the *complete opposite* energy
of what the user wants can still win purely because its genre label matches.
In the "Conflicted (loud + sad)" test the user asked for high energy (0.9), but
the top result was *Winter Elegy*, a classical piece at energy 0.30 — it won on
a +2.0 genre match even though it is the quietest kind of song available. In
other words, the system treats a single categorical label as more important than
the actual "feel" of the music. This also produces a **filter bubble**: because
only *exact* genre matches earn points, musically adjacent styles (e.g. metal for
a rock fan) get zero genre credit and are pushed down the list, so users only
ever see more of the exact label they typed. Finally, the catalog is small and
uneven (pop and lofi are the most common genres), so those genres surface more
often and rarer genres like reggae or country almost never reach the top 5.

Other limitations: the model ignores lyrics, language, artist, and release era;
`likes_acoustic` is a coarse yes/no flag applied to a continuous 0–1 column; and
a single favorite genre/mood can't represent users who like several things.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected.

### Profiles tested

I ran five profiles through `python -m src.main`: three "normal" tastes
(High-Energy Pop, Chill Lofi, Deep Intense Rock) and two adversarial ones
designed to try to trick the scorer — a "Conflicted" user who wants loud *and*
sad music, and a "Ghost Taste" user whose genre/mood don't exist in the catalog
at all.

### Baseline output (documented recipe: genre 2.0, mood 1.0, energy ×1.5)

```
=== Profile: High-Energy Pop ===
prefs: genre=pop, mood=happy, energy=0.9, likes_acoustic=False
1. Sunrise City - Neon Echo  (score: 4.88)  [genre + mood + energy + acoustic]
2. Gym Hero - Max Pulse  (score: 3.96)       [genre + energy + acoustic]
3. Rooftop Lights - Indigo Parade  (score: 2.79) [mood + energy + acoustic]
4. Storm Runner - Voltline  (score: 1.98)    [energy + acoustic]
5. Neon Overdrive - Pulsewave  (score: 1.93) [energy + acoustic]

=== Profile: Chill Lofi ===
prefs: genre=lofi, mood=chill, energy=0.35, likes_acoustic=True
1. Library Rain - Paper Lanterns  (score: 5.00)  [genre + mood + energy + acoustic]
2. Midnight Coding - LoRoom  (score: 4.89)       [genre + mood + energy + acoustic]
3. Focus Flow - LoRoom  (score: 3.92)            [genre + energy + acoustic]
4. Spacewalk Thoughts - Orbit Bloom  (score: 2.90) [mood + energy + acoustic]
5. Coffee Shop Stories - Slow Stereo  (score: 1.97) [energy + acoustic]

=== Profile: Deep Intense Rock ===
prefs: genre=rock, mood=intense, energy=0.9, likes_acoustic=False
1. Storm Runner - Voltline  (score: 4.98)    [genre + mood + energy + acoustic]
2. Gym Hero - Max Pulse  (score: 2.96)       [mood + energy + acoustic]
3. Neon Overdrive - Pulsewave  (score: 1.93) [energy + acoustic]
4. Concrete Kings - Rhyme Theory  (score: 1.92) [energy + acoustic]
5. Iron Verdict - Blacksteel  (score: 1.88)  [energy + acoustic]

=== Profile: Conflicted (loud + sad) ===
prefs: genre=classical, mood=sad, energy=0.9, likes_acoustic=True
1. Winter Elegy - String Quartet No.4  (score: 3.10) [genre + energy(far) + acoustic]
2. Paper Boats - Ellie Wren  (score: 2.07)   [mood + energy(far) + acoustic]
3. Storm Runner - Voltline  (score: 1.48)    [energy only]
4. Gym Hero - Max Pulse  (score: 1.46)       [energy only]
5. Neon Overdrive - Pulsewave  (score: 1.43) [energy only]

=== Profile: Ghost Taste (no matches) ===
prefs: genre=k-pop, mood=dreamy, energy=0.5, likes_acoustic=False
1. Velvet Hours - Smooth Tide  (score: 1.92) [energy + acoustic]
2. Island Time - Sunny Roots  (score: 1.92)  [energy + acoustic]
3. Night Drive Loop - Neon Echo  (score: 1.62) [energy + acoustic]
4. Rooftop Lights - Indigo Parade  (score: 1.61) [energy + acoustic]
5. Sunrise City - Neon Echo  (score: 1.52)   [energy + acoustic]
```

### Weight-shift experiment (energy ×3.0, genre 1.0 — "double energy, half genre")

```
=== Profile: Conflicted (loud + sad) ===
1. Storm Runner - Voltline  (score: 2.97)    [energy only]   <-- was #3 in baseline
2. Gym Hero - Max Pulse  (score: 2.91)       [energy only]
3. Neon Overdrive - Pulsewave  (score: 2.85) [energy only]
```

When energy was doubled and genre halved, the Conflicted profile's #1 flipped
from the quiet *Winter Elegy* (energy 0.30) to the loud *Storm Runner*
(energy 0.91). For the well-aligned profiles (Pop, Rock) the #1 pick did **not**
change, because those songs already match on everything — the experiment mostly
reshuffled the middle of the list. Conclusion: the change made results *different,
not obviously more accurate* for normal users, but it did make conflicting
profiles behave more intuitively (a "loud" request finally returns loud songs).

### What surprised me / pairwise comparisons

- **High-Energy Pop vs Deep Intense Rock:** both want energy 0.9, and both
  surface *Gym Hero* and *Storm Runner* high up — but each ranks *its own* genre
  first. This makes sense: energy pulls the same loud songs into both lists, and
  the +2.0 genre match is the tiebreaker that personalizes the top slot.
- **High-Energy Pop vs Chill Lofi:** near-perfect mirror images. Pop pulls bright,
  loud, non-acoustic tracks; Lofi pulls quiet, acoustic, calm ones. This is the
  clearest sign the energy score is working — the two lists barely overlap.
- **Deep Intense Rock vs Conflicted:** same target energy (0.9), but Conflicted
  asks for classical + sad. Surprisingly its #1 is a *low-energy* classical piece,
  while Rock's #1 is a high-energy rock track — proof that a single genre label can
  outweigh the energy the user actually asked for.
- **Chill Lofi vs Ghost Taste:** Lofi gets strong 5.00/4.89 scores from stacked
  matches; Ghost Taste maxes out around 1.92 because nothing matches its genre or
  mood, so ranking collapses to "closest energy to 0.5." Good failure behavior —
  it degrades gracefully instead of crashing.
- **Conflicted vs Ghost Taste:** both are "broken" inputs, but they fail
  differently — Conflicted still finds a genre match to latch onto (Winter Elegy),
  while Ghost Taste finds none and ranks purely on energy.

**Explaining "Gym Hero" to a non-programmer:** *Gym Hero* is a loud pop workout
song. Anyone who asks for happy, high-energy pop gets it near the top because it
checks three boxes at once — it's pop (big points), it's very energetic (close to
what they asked for), and it's not acoustic (a small bonus). The system isn't
"obsessed" with that song; it just happens to tick more of our scoring boxes than
its neighbors, so it keeps floating up whenever someone wants upbeat pop.

---

## 8. Future Work  

Next I would let users pick several favorite genres and moods instead of just one.
I would add "similar genre" credit so a rock fan can also see metal. I would use
the full 0–1 acousticness value instead of a yes/no flag. I would also add a rule
that prevents one genre from dominating every list, and grow the catalog so rarer
genres have a real chance to appear.

---

## 9. Personal Reflection  

I learned that a recommender is really just a scoring rule plus a ranking rule,
and that the weights you choose quietly decide what users see. The surprising part
was watching a single genre label outweigh the actual energy of a song, which
showed me how easily bias sneaks in. Now I think of apps like Spotify as a set of
tunable choices rather than magic, and I understand why those choices matter.
