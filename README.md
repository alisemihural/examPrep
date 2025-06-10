# 🧠 Pygame Flashcard Viewer

A simple flashcard application built with Python and Pygame that displays question and answer images for studying purposes.

## 🚀 Features

- Displays question images from a `questions/` folder
- Shows corresponding answer images from an `answers/` folder
- Toggle between question and answer with the spacebar
- Responsive window resizing
- Auto-scales images to fit the screen
- Generates dummy images if folders are missing

## 🎮 Controls

- `Space`: Show answer or load a new question
- `Esc`: Quit the application

## 🖼️ Folders

- `questions/` – images labeled `image1.png`, `image2.png`, etc.
- `answers/` – answer images with matching filenames

## 🛠 Requirements

- Python 3.x
- `pygame`
- `Pillow` (for image generation)

Install dependencies:
```bash
pip install pygame Pillow
