import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

DB_NAME = 'projects.db'

def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database and create the projects table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            status TEXT,
            created_date TEXT NOT NULL,
            updated_date TEXT NOT NULL,
            map_link TEXT,
            resources_link TEXT,
            proposal_briefing_link TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def get_all_projects() -> List[Dict]:
    """Retrieve all projects from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM projects ORDER BY updated_date DESC')
    projects = cursor.fetchall()
    
    conn.close()
    
    return [dict(project) for project in projects]

def get_project(project_id: int) -> Optional[Dict]:
    """Get a single project by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
    project = cursor.fetchone()
    
    conn.close()
    
    return dict(project) if project else None

def create_project(data: Dict) -> Dict:
    """Create a new project in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    
    cursor.execute('''
        INSERT INTO projects (name, description, status, created_date, updated_date, 
                             map_link, resources_link, proposal_briefing_link)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('name', ''),
        data.get('description', ''),
        data.get('status', 'Active'),
        now,
        now,
        data.get('map_link', ''),
        data.get('resources_link', ''),
        data.get('proposal_briefing_link', '')
    ))
    
    project_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return get_project(project_id)

def update_project(project_id: int, data: Dict) -> Optional[Dict]:
    """Update an existing project."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    
    cursor.execute('''
        UPDATE projects 
        SET name = ?, description = ?, status = ?, updated_date = ?,
            map_link = ?, resources_link = ?, proposal_briefing_link = ?
        WHERE id = ?
    ''', (
        data.get('name', ''),
        data.get('description', ''),
        data.get('status', 'Active'),
        now,
        data.get('map_link', ''),
        data.get('resources_link', ''),
        data.get('proposal_briefing_link', ''),
        project_id
    ))
    
    conn.commit()
    conn.close()
    
    return get_project(project_id)

def delete_project(project_id: int) -> bool:
    """Delete a project from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
    deleted = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    
    return deleted

def search_projects(query: str) -> List[Dict]:
    """Search projects by name or description."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    search_term = f'%{query}%'
    cursor.execute('''
        SELECT * FROM projects 
        WHERE name LIKE ? OR description LIKE ?
        ORDER BY updated_date DESC
    ''', (search_term, search_term))
    
    projects = cursor.fetchall()
    conn.close()
    
    return [dict(project) for project in projects]


