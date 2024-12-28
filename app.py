from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Load or initialize meeting data
try:
    with open('meetings.json', 'r') as file:
        meetings = json.load(file)
except FileNotFoundError:
    meetings = []

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html', meetings=meetings)

# Route to add a new meeting
@app.route('/add_meeting', methods=['POST'])
def add_meeting():
    data = request.json
    try:
        start_time = datetime.strptime(data['start_time'], '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(data['end_time'], '%Y-%m-%dT%H:%M')
        if start_time >= end_time:
            return jsonify({'error': 'End time must be after start time'}), 400

        meeting = {
            'title': data['title'],
            'start_time': start_time.strftime('%Y-%m-%d %H:%M'),
            'end_time': end_time.strftime('%Y-%m-%d %H:%M')
        }

        # Check for conflicts
        for m in meetings:
            existing_start = datetime.strptime(m['start_time'], '%Y-%m-%d %H:%M')
            existing_end = datetime.strptime(m['end_time'], '%Y-%m-%d %H:%M')

            if (start_time < existing_end and end_time > existing_start):
                return jsonify({'error': 'Time conflict with another meeting'}), 400

        meetings.append(meeting)

        # Save to file
        with open('meetings.json', 'w') as file:
            json.dump(meetings, file)

        return jsonify({'message': 'Meeting added successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to delete a meeting
@app.route('/delete_meeting', methods=['POST'])
def delete_meeting():
    data = request.json
    try:
        meeting_id = int(data['id'])
        if 0 <= meeting_id < len(meetings):
            meetings.pop(meeting_id)
            with open('meetings.json', 'w') as file:
                json.dump(meetings, file)
            return jsonify({'message': 'Meeting deleted successfully'})
        else:
            return jsonify({'error': 'Invalid meeting ID'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


