# app/app.py
from flask import Flask, render_template, request, jsonify
import pandas as pd
from clustering import perform_clustering
import os

app = Flask(__name__,
            template_folder=os.path.abspath('app/templates'),
            static_folder=os.path.abspath('app/static'))

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error rendering template: {e}")
        return str(e), 500

@app.route('/search', methods=['POST'])
def search():
    agent_number = request.form.get('agent_number')
    if not agent_number or len(agent_number) != 11:
        return jsonify({'error': 'Invalid agent number'})

    df = pd.read_csv('agent_data.csv')
    agent_data = df[df['Agent Account Number'] == int(agent_number)]
    
    if agent_data.empty:
        return jsonify({'error': 'Agent not found'})

    # Get clustering results
    clustering_results = perform_clustering(agent_data)
    
    # Prepare location data
    locations = []
    for _, row in agent_data.iterrows():
        locations.append({
            'lat': row['Pinned Latitude'],
            'lng': row['Pinned Longitude'],
            'agent': row['Agent Account Number'],
            'address': row['Pinned Address'],
            'accuracy': row['Accuracy']
        })

    return jsonify({
        'locations': locations,
        'clusters': clustering_results
    })

if __name__ == '__main__':
    app.run(debug=True)