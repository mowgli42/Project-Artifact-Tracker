# Project Artifact Tracker

A web-based application for tracking projects with links to maps, resources, and proposal briefings. Built with Flask (Python) backend and vanilla JavaScript frontend, using SQLite for data persistence.

<img width="1256" height="689" alt="Project Artifact Tracker" src="https://github.com/user-attachments/assets/9aac7b71-1daa-467c-80d9-a240873b746f" />

## Features

- **CRUD Operations**: Create, read, update, and delete projects
- **Search**: Real-time search across project names and descriptions
- **Filtering**: Filter projects by status (Active, Completed, On Hold, Planning)
- **Link Management**: Direct links to map, resources, and proposal briefing for each project
- **Date Tracking**: Automatic tracking of created and updated dates
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Modern UI**: Clean, card-based dashboard with smooth animations

## Requirements

- Python 3.7+
- Flask 3.0.0

## Installation

1. Clone or navigate to the project directory:
```bash
cd Project-Artifact-Tracker
```

2. Install dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Running tests

```bash
source .venv/bin/activate
pytest
```

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. The application will automatically create the SQLite database (`projects.db`) on first run.

## Project Structure

```
Project-Artifact-Tracker/
├── app.py                 # Flask application and routes
├── database.py            # Database initialization and operations
├── requirements.txt       # Python dependencies
├── projects.db            # SQLite database (created automatically)
├── static/
│   ├── css/
│   │   └── style.css     # Dashboard styling
│   └── js/
│       └── main.js        # Frontend logic (search, filters, CRUD)
├── templates/
│   └── index.html        # Main dashboard page
└── README.md             # This file
```

## Database Schema

The `projects` table contains:
- `id` - Primary key
- `name` - Project name (required)
- `description` - Project description
- `status` - Project status (Active, Completed, On Hold, Planning)
- `created_date` - Creation timestamp
- `updated_date` - Last update timestamp
- `map_link` - URL to project map
- `resources_link` - URL to project resources
- `proposal_briefing_link` - URL to proposal briefing

## API Endpoints

- `GET /` - Serve dashboard HTML
- `GET /api/projects` - List all projects (supports `?search=` and `?status=` query parameters)
- `GET /api/projects/<id>` - Get single project
- `POST /api/projects` - Create new project
- `PUT /api/projects/<id>` - Update project
- `DELETE /api/projects/<id>` - Delete project

## Usage Tips

- Click the "+ Add Project" button to create a new project
- Use the search bar to find projects by name or description
- Use the status filter dropdown to filter projects by status
- Click the edit icon (✏️) on a project card to modify it
- Click the delete icon (🗑️) to remove a project
- Click the Map, Resources, or Proposal buttons to open the respective links in a new tab

## License

This project is open source and available for use.


