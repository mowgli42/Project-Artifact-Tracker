#!/usr/bin/env python3
"""
Script to generate 15 sample projects for the Project Artifact Tracker.
Run this script to populate the database with example data.
"""

from database import init_db, create_project
import random
from datetime import datetime, timedelta

# Sample project data
SAMPLE_PROJECTS = [
    {
        'name': 'Urban Green Space Initiative',
        'description': 'Development of community parks and green spaces in urban areas to improve air quality and provide recreational areas for residents.',
        'status': 'Active',
        'map_link': 'https://maps.example.com/urban-green-space',
        'resources_link': 'https://resources.example.com/urban-green-space',
        'proposal_briefing_link': 'https://proposals.example.com/urban-green-space-briefing'
    },
    {
        'name': 'Renewable Energy Grid Expansion',
        'description': 'Expansion of renewable energy infrastructure to support increased demand and reduce carbon footprint.',
        'status': 'Active',
        'map_link': 'https://maps.example.com/renewable-energy',
        'resources_link': 'https://resources.example.com/renewable-energy',
        'proposal_briefing_link': 'https://proposals.example.com/renewable-energy-briefing'
    },
    {
        'name': 'Smart City Traffic Management',
        'description': 'Implementation of AI-powered traffic management system to reduce congestion and improve commute times.',
        'status': 'Planning',
        'map_link': 'https://maps.example.com/traffic-management',
        'resources_link': 'https://resources.example.com/traffic-management',
        'proposal_briefing_link': 'https://proposals.example.com/traffic-management-briefing'
    },
    {
        'name': 'Coastal Erosion Prevention',
        'description': 'Beach restoration and coastal protection measures to prevent erosion and protect shoreline communities.',
        'status': 'Active',
        'map_link': 'https://maps.example.com/coastal-erosion',
        'resources_link': 'https://resources.example.com/coastal-erosion',
        'proposal_briefing_link': 'https://proposals.example.com/coastal-erosion-briefing'
    },
    {
        'name': 'Affordable Housing Development',
        'description': 'Construction of affordable housing units to address housing shortages in metropolitan areas.',
        'status': 'On Hold',
        'map_link': 'https://maps.example.com/affordable-housing',
        'resources_link': 'https://resources.example.com/affordable-housing',
        'proposal_briefing_link': 'https://proposals.example.com/affordable-housing-briefing'
    },
    {
        'name': 'Digital Literacy Program',
        'description': 'Community-based program to improve digital skills and access to technology for underserved populations.',
        'status': 'Active',
        'map_link': 'https://maps.example.com/digital-literacy',
        'resources_link': 'https://resources.example.com/digital-literacy',
        'proposal_briefing_link': 'https://proposals.example.com/digital-literacy-briefing'
    },
    {
        'name': 'Water Quality Improvement',
        'description': 'Upgrade of water treatment facilities and infrastructure to ensure safe drinking water for all residents.',
        'status': 'Completed',
        'map_link': 'https://maps.example.com/water-quality',
        'resources_link': 'https://resources.example.com/water-quality',
        'proposal_briefing_link': 'https://proposals.example.com/water-quality-briefing'
    },
    {
        'name': 'Public Transportation Enhancement',
        'description': 'Expansion of bus and rail networks to improve connectivity and reduce reliance on private vehicles.',
        'status': 'Active',
        'map_link': 'https://maps.example.com/public-transport',
        'resources_link': 'https://resources.example.com/public-transport',
        'proposal_briefing_link': 'https://proposals.example.com/public-transport-briefing'
    },
    {
        'name': 'Waste Management Modernization',
        'description': 'Implementation of recycling programs and waste-to-energy facilities to reduce landfill usage.',
        'status': 'Planning',
        'map_link': 'https://maps.example.com/waste-management',
        'resources_link': 'https://resources.example.com/waste-management',
        'proposal_briefing_link': 'https://proposals.example.com/waste-management-briefing'
    },
    {
        'name': 'Community Health Centers',
        'description': 'Establishment of new health centers in underserved neighborhoods to improve access to healthcare services.',
        'status': 'Active',
        'map_link': 'https://maps.example.com/health-centers',
        'resources_link': 'https://resources.example.com/health-centers',
        'proposal_briefing_link': 'https://proposals.example.com/health-centers-briefing'
    },
    {
        'name': 'Cybersecurity Infrastructure',
        'description': 'Enhancement of cybersecurity measures for critical infrastructure and government systems.',
        'status': 'Active',
        'map_link': 'https://maps.example.com/cybersecurity',
        'resources_link': 'https://resources.example.com/cybersecurity',
        'proposal_briefing_link': 'https://proposals.example.com/cybersecurity-briefing'
    },
    {
        'name': 'Historic Preservation Initiative',
        'description': 'Restoration and preservation of historic buildings and landmarks to maintain cultural heritage.',
        'status': 'On Hold',
        'map_link': 'https://maps.example.com/historic-preservation',
        'resources_link': 'https://resources.example.com/historic-preservation',
        'proposal_briefing_link': 'https://proposals.example.com/historic-preservation-briefing'
    },
    {
        'name': 'Rural Broadband Expansion',
        'description': 'Deployment of high-speed internet infrastructure to rural and remote areas to bridge the digital divide.',
        'status': 'Active',
        'map_link': 'https://maps.example.com/rural-broadband',
        'resources_link': 'https://resources.example.com/rural-broadband',
        'proposal_briefing_link': 'https://proposals.example.com/rural-broadband-briefing'
    },
    {
        'name': 'Emergency Response System Upgrade',
        'description': 'Modernization of emergency services communication and response systems for improved public safety.',
        'status': 'Completed',
        'map_link': 'https://maps.example.com/emergency-response',
        'resources_link': 'https://resources.example.com/emergency-response',
        'proposal_briefing_link': 'https://proposals.example.com/emergency-response-briefing'
    },
    {
        'name': 'Sustainable Agriculture Program',
        'description': 'Support for local farmers with sustainable farming practices and access to markets.',
        'status': 'Planning',
        'map_link': 'https://maps.example.com/sustainable-agriculture',
        'resources_link': 'https://resources.example.com/sustainable-agriculture',
        'proposal_briefing_link': 'https://proposals.example.com/sustainable-agriculture-briefing'
    }
]

def generate_sample_data():
    """Generate and insert sample projects into the database."""
    print("Initializing database...")
    init_db()
    
    print(f"Generating {len(SAMPLE_PROJECTS)} sample projects...")
    
    for i, project_data in enumerate(SAMPLE_PROJECTS, 1):
        try:
            project = create_project(project_data)
            print(f"  [{i}/{len(SAMPLE_PROJECTS)}] Created: {project['name']}")
        except Exception as e:
            print(f"  [{i}/{len(SAMPLE_PROJECTS)}] Error creating {project_data['name']}: {e}")
    
    print("\nSample data generation complete!")
    print(f"Created {len(SAMPLE_PROJECTS)} projects in the database.")

if __name__ == '__main__':
    generate_sample_data()

