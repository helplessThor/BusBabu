# BusBabu 🚌🚖

**BusBabu** is an intelligent transit routing application for Kolkata, designed to help commuters find the most efficient bus and metro connections across the city. 

> **Project Inception:** Work on this project started in **January 2026** with the vision of providing a sleek, modern, and highly thematic transit router for Kolkata commuters.

## Features

- 🚇 **Dynamic Metro Routing**: Fully integrated with Kolkata's Metro network (Blue, Green, Orange, Yellow, and Purple lines). The routing algorithm smartly prioritizes metro transfers for faster travel.
- 🎨 **Dynamic Thematics**: The app embraces the spirit of Kolkata with two randomly selected dynamic themes:
  - **Bus Theme**: Inspired by the classic Blue & Yellow Kolkata buses.
  - **Taxi Theme**: A tribute to the iconic Ambassador Yellow Taxis.
- 🌓 **Light & Dark Mode**: A premium, glassmorphic UI that adapts to your system preferences with distinct color gradients for each metro line.
- 🗺️ **Interactive Maps**: Plot your selected journey directly on an interactive map.
- ⚡ **Offline-Ready routing logic**: Powered by a heavily optimized graph traversal algorithm to find direct, one-change, and two-change transit paths instantly.

## Data Pipeline

The routing data is automatically compiled from raw JSON/text dumps (sourced from Kolbusopedia and the community Bus Repository). Our custom Python script normalizes thousands of inconsistent bus stop names, connects them via a spatial adjacency graph, and interpolates missing geographical coordinates.

To regenerate the data payload manually:
```bash
python data/build.py
```
*(This parses the latest transit dumps and outputs the optimized graph into `public/busdata.json`)*

## Development

This project is built with Vanilla JS, HTML, CSS, and Vite.

```bash
# Install dependencies
npm install

# Start the local development server
npm run dev

# Build for production
npm run build
```

## Journey & Milestones
- **Jan 2026**: Project inception and foundation architecture. Implementation of the core route-finding graph algorithm and initial "Taxi/Bus" thematic UI.
- **May 2026**: Major upgrade integrating the Metro connectivity graph, JS-based bus repositories, and dynamic color-coded Metro routing interfaces.
