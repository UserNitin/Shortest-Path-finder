🧭 Shortest Path Finder with Pygame
This project is a 2D shortest path visualizer using Python and Pygame. It lets users select a start and end point on a school-like map and calculates the shortest path using the A (A-Star) pathfinding algorithm*.

📌 Features
🎮 Interactive GUI with room names (e.g., Library, Labs, Classrooms)

🧠 A* algorithm for shortest path calculation

🧱 Wall detection to avoid obstacles (rooms)

🎨 Color-coded rooms and path visualization

📜 Scrollable map for navigating large layouts

🔴 Red start and end points

🟡 Yellow path showing shortest route

🚀 Technologies Used
Python 3

Pygame – for 2D graphics and GUI

🗺️ How It Works
The map is created using a tile-based grid.

Pre-defined rooms are added to the map with names and colors.

These rooms act as obstacles (walls).

The user clicks to set a start and end point.

The A pathfinding algorithm* finds the shortest path.

The path is shown in yellow with red start/end markers.

🧠 Algorithm Used
A* (A-Star) Search Algorithm:
Uses Manhattan Distance as a heuristic.

Fast and accurate for grid-based maps.

Avoids walls and selects the optimal route.

🖱️ Controls
🖱️ Click once → Select start point

🖱️ Click again → Select end point

🔁 Press R → Reset path

⬅️➡️⬆️⬇️ Arrow Keys → Scroll map

🔮 Future Enhancements
📡 Real-time traffic integration for dynamic routing

🌐 Web and mobile version for broader access

🤖 AI-enhanced heuristics using machine learning

🧭 Multi-modal routing: walking, biking, driving
