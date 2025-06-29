# Drone Deconfliction System

## 📌 Overview

This project implements a modular drone deconfliction system in Python. It simulates multiple drone trajectories, checks for spatial and temporal conflicts, and visualizes results in both 2D and 3D with optional animations.

## ✅ Features

* Conflict detection with configurable safety buffer
* Waypoint time interpolation for continuous checks
* 2D and 3D static plots and animations
* Multiple demo scenarios: Basic, Complex, Safe, and Planar (2D)
* Interactive CLI for running scenarios

## 🗂️ File Structure

```
.
├── deconfliction.py      # Core conflict logic and system class
├── models.py             # Data models: Waypoint, Mission, Conflict
├── demo.py               # Predefined demo scenarios
├── main.py               # CLI entry point with interactive menu
├── visualisation_2d.py   # 2D visualization logic
├── visualisation_3d.py   # 3D visualization logic
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── reflection.md         # Design reflection and justification
```

## ⚙️ Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/hrishisharma/drone_deconfliction.git
pip install -r requirements.txt
```

## ▶️ Running

Run the interactive menu:

```bash
python main.py
```

Choose a scenario: Basic, Complex, Safe, 2D or run all.

## 📈 Visualizations

* Close plot windows to continue through scenarios.
* Animations show live drone positions over time.

## ✏️ Requirements

```
numpy
matplotlib
```

## 🧩 Extending

This system can be extended with real flight data feeds, AI-based path prediction, or more advanced 4D conflict detection.

---

**Author:** Hrishi Sharma
