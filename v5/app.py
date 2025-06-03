from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

STAFF_DATA_FILE = 'data/staff.json'
os.makedirs('data', exist_ok=True)

# Utility function to load staff data
def load_staff():
    if not os.path.exists(STAFF_DATA_FILE):
        return []
    with open(STAFF_DATA_FILE, 'r') as f:
        return json.load(f)

# Utility function to save staff data
def save_staff(data):
    with open(STAFF_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Auto-generate staff ID
def generate_staff_id(existing_staff):
    if not existing_staff:
        return 'S001'
    last_id = existing_staff[-1]['id']
    num = int(last_id[1:]) + 1
    return f"S{num:03d}"

@app.route('/')
def index():
    staff_list = load_staff()
    return render_template('index.html', staff=staff_list)

@app.route('/add', methods=['POST'])
def add_staff():
    name = request.form['name'].strip()
    subjects = request.form.getlist('subjects')
    departments = request.form.getlist('departments')

    staff_list = load_staff()
    new_id = generate_staff_id(staff_list)

    staff_entry = {
        'id': new_id,
        'name': name,
        'subjects': subjects,
        'departments': departments
    }

    staff_list.append(staff_entry)
    save_staff(staff_list)
    return redirect(url_for('index'))

@app.route('/delete/<staff_id>')
def delete_staff(staff_id):
    staff_list = load_staff()
    staff_list = [s for s in staff_list if s['id'] != staff_id]
    save_staff(staff_list)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
