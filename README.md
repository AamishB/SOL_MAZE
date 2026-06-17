# <img src="assets/icon.png" style="height:25px;width:25px"></img> <img src="assets/title.png" style="height:25px"></img>

Welcome to **Sol Maze**, a grid-based maze game built with Pygame where the core mechanic revolves around the duality of light and shadow during the solstice, but it also features various [modes](#modes) to play.

## 🎮 Gameplay (Standard Mode)

- **Day Phase**: Light zones are walkable paths. Shadows are impassable walls.
- **Night Phase**: The mechanics invert. Shadows become paths, and light zones become walls.
- **Goal**: Navigate the changing environment to collect **Sun Stones** (in the light) and **Moon Stones** (in the dark) to unlock the exit.

## 🚀 How to Run Locally

1. **Install Dependencies**
   Make sure you have Python 3 installed. Then, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the Game**
   ```bash
   python main.py
   ```

## 🛠️ Controls

- **Arrow Keys**: Move the player
- **Tab / S**: Skip to the next solstice phase (Day <-> Night)
- **F11**: Toggle Fullscreen
- **ESC / P**: Pause Menu

<h2 id="modes">🗺️ Modes</h2>

- **Standard**: The original game with the duality of light and shadow.
- **Solstice Shift**: A maze with a shifting solstice mechanic.
- **June Celebration Calendar**: Features various modes based on the calendar, such as:
  - **Pride Maze**: A maze with rainbow-colored paths and obstacles.
  - **World Environment Day**: A maze with different environments such as forests and oceans.
  - **Juneteenth**: A maze with a freedom theme.
  - **Solstice Maze**: The standard maze for the day.
  - **Fathers Day**: A maze with a father theme.
  - **World Music Day**: A maze with a music theme.

## 🎨 Credits

- **Code**: This project was made with assistance of **Antigravity**.
- **Background Art**: Some background images and visual assets used in this game were generated with the assistance of **Google Gemini AI**.
