from flask import Flask, render_template, request, jsonify
from database import init_db, get_all_projects, get_project, create_project, update_project, delete_project, search_projects

app = Flask(__name__)

# Initialize database on startup
init_db()

@app.route('/')
def index():
    """Serve the main dashboard page."""
    return render_template('index.html')

@app.route('/api/projects', methods=['GET'])
def api_get_projects():
    """Get all projects, optionally filtered by search query."""
    search_query = request.args.get('search', '').strip()
    
    if search_query:
        projects = search_projects(search_query)
    else:
        projects = get_all_projects()
    
    # Filter by status if provided
    status_filter = request.args.get('status', '').strip()
    if status_filter:
        projects = [p for p in projects if p.get('status') == status_filter]
    
    return jsonify(projects)

@app.route('/api/projects/<int:project_id>', methods=['GET'])
def api_get_project(project_id):
    """Get a single project by ID."""
    project = get_project(project_id)
    
    if project is None:
        return jsonify({'error': 'Project not found'}), 404
    
    return jsonify(project)

@app.route('/api/projects', methods=['POST'])
def api_create_project():
    """Create a new project."""
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Project name is required'}), 400
    
    project = create_project(data)
    return jsonify(project), 201

@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def api_update_project(project_id):
    """Update an existing project."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    project = update_project(project_id, data)
    
    if project is None:
        return jsonify({'error': 'Project not found'}), 404
    
    return jsonify(project)

@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def api_delete_project(project_id):
    """Delete a project."""
    deleted = delete_project(project_id)
    
    if not deleted:
        return jsonify({'error': 'Project not found'}), 404
    
    return jsonify({'message': 'Project deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


