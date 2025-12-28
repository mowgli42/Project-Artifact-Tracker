#!/usr/bin/env python3
"""
Import script for Project Artifact Tracker.

This script can ingest a folder structure where each sub-folder represents a project.
It will prompt for each project import and provide guidance on data organization.

Expected folder structure:
    projects_folder/
        project_name_1/
            map.html (or map.pdf, map.png, etc.)
            resources/ (folder with resources)
            proposal_briefing.pdf (or .doc, .txt, etc.)
        project_name_2/
            ...
"""

import os
import sys
from pathlib import Path
from database import init_db, create_project, get_all_projects
import mimetypes

def print_help():
    """Print help information about folder structure and file naming."""
    print("\n" + "="*70)
    print("PROJECT FOLDER STRUCTURE GUIDE")
    print("="*70)
    print("""
For best results, organize your project folders as follows:

📁 project_folder_name/
    ├── 📄 map.*          (Any file with 'map' in the name)
    │   └── Examples: map.html, map.pdf, map.png, project_map.html
    │
    ├── 📁 resources/     (Folder containing project resources)
    │   ├── documents/
    │   ├── images/
    │   └── data files...
    │
    └── 📄 proposal*     (Any file with 'proposal' or 'briefing' in the name)
        └── Examples: proposal.pdf, briefing.docx, proposal_briefing.txt

FILE NAMING CONVENTIONS:
  • Map files: Should contain 'map' in the filename
  • Proposal files: Should contain 'proposal' or 'briefing' in the filename
  • Resources: Should be in a folder named 'resources' or 'resource'

The script will:
  1. Use the folder name as the project name
  2. Search for map files automatically
  3. Search for proposal/briefing files automatically
  4. Ask you to specify the resources link (file or folder)
  5. Allow you to add a description and set the status
""")
    print("="*70 + "\n")

def find_map_files(folder_path):
    """Find map-related files in the folder."""
    map_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_lower = file.lower()
            if 'map' in file_lower:
                full_path = os.path.join(root, file)
                map_files.append(full_path)
    return map_files

def find_proposal_files(folder_path):
    """Find proposal or briefing files in the folder."""
    proposal_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_lower = file.lower()
            if 'proposal' in file_lower or 'briefing' in file_lower:
                full_path = os.path.join(root, file)
                proposal_files.append(full_path)
    return proposal_files

def find_resources_folder(folder_path):
    """Find resources folder in the project directory."""
    resources_folders = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            item_lower = item.lower()
            if 'resource' in item_lower:
                resources_folders.append(item_path)
    return resources_folders

def get_file_url(file_path, base_folder):
    """Convert file path to a file:// URL or relative path."""
    # For web applications, you might want to use relative paths
    # or configure a static file server
    relative_path = os.path.relpath(file_path, base_folder)
    return f"file://{os.path.abspath(file_path)}"

def prompt_user(prompt, default=None, choices=None):
    """Prompt user for input with optional default and choices."""
    if choices:
        prompt += f" [{', '.join(choices)}]"
    if default:
        prompt += f" (default: {default})"
    prompt += ": "
    
    while True:
        response = input(prompt).strip()
        if not response and default:
            return default
        if not response:
            print("Please provide a value.")
            continue
        if choices and response not in choices:
            print(f"Please choose from: {', '.join(choices)}")
            continue
        return response

def import_project_folder(folder_path, base_folder):
    """Import a single project folder."""
    folder_name = os.path.basename(folder_path.rstrip('/'))
    
    print(f"\n{'='*70}")
    print(f"Importing Project: {folder_name}")
    print(f"{'='*70}")
    
    # Find map files
    map_files = find_map_files(folder_path)
    map_link = ""
    if map_files:
        print(f"\nFound {len(map_files)} map file(s):")
        for i, mf in enumerate(map_files, 1):
            print(f"  {i}. {os.path.basename(mf)}")
        
        if len(map_files) == 1:
            use_map = prompt_user("Use this map file?", default="y", choices=["y", "n"])
            if use_map.lower() == 'y':
                map_link = get_file_url(map_files[0], base_folder)
        else:
            choice = prompt_user(f"Select map file (1-{len(map_files)}) or 'n' for none", default="1")
            if choice.lower() != 'n':
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(map_files):
                        map_link = get_file_url(map_files[idx], base_folder)
                except ValueError:
                    pass
    else:
        print("\nNo map files found.")
        map_input = prompt_user("Enter map link (URL or file path, or press Enter to skip)", default="")
        if map_input:
            map_link = map_input
    
    # Find proposal files
    proposal_files = find_proposal_files(folder_path)
    proposal_link = ""
    if proposal_files:
        print(f"\nFound {len(proposal_files)} proposal/briefing file(s):")
        for i, pf in enumerate(proposal_files, 1):
            print(f"  {i}. {os.path.basename(pf)}")
        
        if len(proposal_files) == 1:
            use_proposal = prompt_user("Use this proposal file?", default="y", choices=["y", "n"])
            if use_proposal.lower() == 'y':
                proposal_link = get_file_url(proposal_files[0], base_folder)
        else:
            choice = prompt_user(f"Select proposal file (1-{len(proposal_files)}) or 'n' for none", default="1")
            if choice.lower() != 'n':
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(proposal_files):
                        proposal_link = get_file_url(proposal_files[idx], base_folder)
                except ValueError:
                    pass
    else:
        print("\nNo proposal/briefing files found.")
        proposal_input = prompt_user("Enter proposal briefing link (URL or file path, or press Enter to skip)", default="")
        if proposal_input:
            proposal_link = proposal_input
    
    # Find resources
    resources_folders = find_resources_folder(folder_path)
    resources_link = ""
    if resources_folders:
        print(f"\nFound {len(resources_folders)} resources folder(s):")
        for i, rf in enumerate(resources_folders, 1):
            print(f"  {i}. {os.path.basename(rf)}")
        
        if len(resources_folders) == 1:
            use_resources = prompt_user("Use this resources folder?", default="y", choices=["y", "n"])
            if use_resources.lower() == 'y':
                resources_link = get_file_url(resources_folders[0], base_folder)
        else:
            choice = prompt_user(f"Select resources folder (1-{len(resources_folders)}) or 'n' for none", default="1")
            if choice.lower() != 'n':
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(resources_folders):
                        resources_link = get_file_url(resources_folders[idx], base_folder)
                except ValueError:
                    pass
    else:
        print("\nNo resources folder found.")
        resources_input = prompt_user("Enter resources link (URL or file path, or press Enter to skip)", default="")
        if resources_input:
            resources_link = resources_input
    
    # Get description and status
    print("\n" + "-"*70)
    description = prompt_user("Enter project description (or press Enter to skip)", default="")
    status = prompt_user("Enter project status", default="Active", 
                        choices=["Active", "Completed", "On Hold", "Planning"])
    
    # Create project data
    project_data = {
        'name': folder_name,
        'description': description,
        'status': status,
        'map_link': map_link,
        'resources_link': resources_link,
        'proposal_briefing_link': proposal_link
    }
    
    return project_data

def main():
    """Main import function."""
    print("\n" + "="*70)
    print("PROJECT ARTIFACT TRACKER - IMPORT TOOL")
    print("="*70)
    
    # Show help
    show_help = prompt_user("Show folder structure guide?", default="y", choices=["y", "n"])
    if show_help.lower() == 'y':
        print_help()
    
    # Get folder path
    if len(sys.argv) > 1:
        projects_folder = sys.argv[1]
    else:
        projects_folder = prompt_user("\nEnter path to folder containing project sub-folders")
    
    if not os.path.isdir(projects_folder):
        print(f"Error: '{projects_folder}' is not a valid directory.")
        sys.exit(1)
    
    # Initialize database
    print("\nInitializing database...")
    init_db()
    
    # Find all subdirectories (potential projects)
    project_folders = []
    for item in os.listdir(projects_folder):
        item_path = os.path.join(projects_folder, item)
        if os.path.isdir(item_path):
            project_folders.append(item_path)
    
    if not project_folders:
        print(f"No subdirectories found in '{projects_folder}'")
        sys.exit(1)
    
    print(f"\nFound {len(project_folders)} project folder(s):")
    for i, pf in enumerate(project_folders, 1):
        print(f"  {i}. {os.path.basename(pf)}")
    
    # Ask which projects to import
    import_all = prompt_user("\nImport all projects?", default="y", choices=["y", "n"])
    
    folders_to_import = []
    if import_all.lower() == 'y':
        folders_to_import = project_folders
    else:
        selection = prompt_user(f"Enter project numbers to import (comma-separated, e.g., 1,3,5) or 'all'", default="all")
        if selection.lower() == 'all':
            folders_to_import = project_folders
        else:
            try:
                indices = [int(x.strip()) - 1 for x in selection.split(',')]
                folders_to_import = [project_folders[i] for i in indices if 0 <= i < len(project_folders)]
            except (ValueError, IndexError):
                print("Invalid selection. Importing all projects.")
                folders_to_import = project_folders
    
    # Import each project
    imported = 0
    skipped = 0
    
    for folder_path in folders_to_import:
        try:
            project_data = import_project_folder(folder_path, projects_folder)
            
            # Confirm before importing
            print(f"\nProject Summary:")
            print(f"  Name: {project_data['name']}")
            print(f"  Status: {project_data['status']}")
            print(f"  Map Link: {project_data['map_link'] or 'None'}")
            print(f"  Resources Link: {project_data['resources_link'] or 'None'}")
            print(f"  Proposal Link: {project_data['proposal_briefing_link'] or 'None'}")
            
            confirm = prompt_user("\nImport this project?", default="y", choices=["y", "n"])
            
            if confirm.lower() == 'y':
                create_project(project_data)
                print(f"✓ Successfully imported: {project_data['name']}")
                imported += 1
            else:
                print(f"⊘ Skipped: {project_data['name']}")
                skipped += 1
                
        except Exception as e:
            print(f"✗ Error importing {os.path.basename(folder_path)}: {e}")
            skipped += 1
    
    # Summary
    print("\n" + "="*70)
    print("IMPORT SUMMARY")
    print("="*70)
    print(f"Imported: {imported}")
    print(f"Skipped: {skipped}")
    print(f"Total: {imported + skipped}")
    print("="*70 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nImport cancelled by user.")
        sys.exit(0)

