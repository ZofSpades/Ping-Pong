# Pygame Ping Pong (SE - vibe-coding project)

A simple real-time ping pong game built with Pygame featuring refined collisions, a game over screen, replay options (Best of 3/5/7), and lightweight synthetic sound effects generated with NumPy. 

---

## Features

- Player paddle with W/S controls and an AI paddle that tracks the ball for responsive gameplay.  
- Ball movement with rectangle overlap detection and snap-and-reflect collision to avoid tunneling at high speeds.  
- Score tracking with a game over state that displays “Player Wins!” or “AI Wins!” when the target is reached.  
- Replay menu after game over: choose Best of 3, 5, 7, or Exit via keys 3, 5, 7, or ESC to continue or quit.  
- Synthetic audio generated with NumPy and played via pygame.mixer for paddle hits, wall bounces, and scoring.  

---

## Requirements

- Python 3.10+ is recommended for running the game reliably.  
- Install dependencies from requirements.txt using pip.  

```
pip install -r requirements.txt
```

---

## Run

Launch the game from the project root.  

```
python main.py
```

If using PowerShell on Windows, the command is the same and should be run from the directory containing main.py.  

---

## Controls

- W: Move player paddle up.  
- S: Move player paddle down.  
- After Game Over: press 3 for Best of 3, 5 for Best of 5, 7 for Best of 7, ESC to Exit.  
- Close the window or use ESC on the replay menu to quit cleanly.  

---

## How It Works

- The update loop moves the ball, immediately checks paddle collisions using rectangle overlap, and snaps the ball outside the paddle before reflecting horizontal velocity.  
- Scores increment when the ball crosses a side boundary, with the ball reset to center for the next rally.  
- When a side reaches the target score, a centered winner message is rendered and the game enters a non-playing state so the message remains visible.  
- A replay menu is shown in the game over state, and selecting a series updates the target score to first-to (N//2 + 1) and resets positions to resume play.  

---

## Audio Notes

- The mixer is initialized at startup, and synthetic sounds are created from NumPy int16 arrays using pygame.sndarray to avoid external assets.  
- If your mixer is configured for stereo, arrays are produced in a 2D shape ((N, 2)) by duplicating the mono channel to satisfy pygame.mixer expectations.  

---

## Folder Structure

```
pygame-pingpong/
├── main.py
├── requirements.txt
├── game/
│   ├── game_engine.py
│   ├── paddle.py
│   └── ball.py
└── README.md
```

---

## Troubleshooting

- If “Array must be 2-dimensional for stereo mixer” appears, ensure the mixer is initialized before creating sounds so tone generation matches the active channel count.  
- Verify Python and dependencies via `python --version` and `pip show pygame numpy` if encountering import or audio initialization issues.  

---

## Submission Checklist

✅ All features implemented: collision, game over screen, replay menu, and sound effects.
✅ Game runs without crashes and behaves as described.
✅ Dependencies installed from requirements.txt.
✅ README instructions followed for setup and running.
✅ Codebase remains clean, modular, and understandable.
