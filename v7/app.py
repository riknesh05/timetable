from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import json
import os
import io
from openpyxl import Workbook

app = Flask(__name__)

DATA_DIR = 'data'
STAFF_FILE = os.path.join(DATA_DIR, 'staff.json')
os.makedirs(DATA_DIR, exist_ok=True)

def load_staff():
    if not os.path.exists(STAFF_FILE):
        return []
    with open(STAFF_FILE, 'r') as f:
        return json.load(f)

def save_staff(data):
    with open(STAFF_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def generate_staff_id(staff_list):
    if not staff_list:
        return 'S001'
    last_id = staff_list[-1]['id']
    num = int(last_id[1:]) + 1
    return f'S{num:03d}'

@app.route('/staff')
def staff_page():
    staff = load_staff()
    departments = [
        'CSE 1st A', 'CSE 1st B', 'CSE 1st C',
        'CSE 2nd A', 'CSE 2nd B', 'CSE 2nd C',
        'CSE 3rd A', 'CSE 3rd B', 'CSE 3rd C',
        'CSE 4th A', 'CSE 4th B', 'CSE 4th C',
        'IT 3rd A', 'IT 3rd B',
        'AI & ML',
        'AIDS',
        'ECE 1st',
        'Cyber Security',
        'MECH'
    ]

    # Build a map: department -> unique subjects of staff belonging to it
    subjects_by_dept = {}
    for dept in departments:
        subjects_set = set()
        for s in staff:
            if dept in s.get('departments', []):
                subjects_set.update(s.get('subjects', []))
        subjects_by_dept[dept] = sorted(subjects_set)

    return render_template('staff.html', staff=staff, departments=departments, subjects_by_dept=subjects_by_dept)

@app.route('/staff/add', methods=['POST'])
def add_staff():
    name = request.form['name'].strip()
    subjects = request.form.getlist('subjects')
    departments = request.form.getlist('departments')

    staff_list = load_staff()
    new_id = generate_staff_id(staff_list)

    staff_list.append({
        'id': new_id,
        'name': name,
        'subjects': subjects,
        'departments': departments
    })

    save_staff(staff_list)
    return redirect(url_for('staff_page'))

@app.route('/staff/delete/<staff_id>')
def delete_staff(staff_id):
    staff_list = load_staff()
    staff_list = [s for s in staff_list if s['id'] != staff_id]
    save_staff(staff_list)
    return redirect(url_for('staff_page'))

@app.route('/staff/edit/<staff_id>', methods=['GET', 'POST'])
def edit_staff(staff_id):
    staff_list = load_staff()
    staff = next((s for s in staff_list if s['id'] == staff_id), None)
    if not staff:
        return "Staff Not Found", 404

    departments = [
        'CSE 1st A', 'CSE 1st B', 'CSE 1st C',
        'CSE 2nd A', 'CSE 2nd B', 'CSE 2nd C',
        'CSE 3rd A', 'CSE 3rd B', 'CSE 3rd C',
        'CSE 4th A', 'CSE 4th B', 'CSE 4th C',
        'IT 3rd A', 'IT 3rd B',
        'AI & ML',
        'AIDS',
        'ECE 1st',
        'Cyber Security',
        'MECH'
    ]

    if request.method == 'POST':
        staff['name'] = request.form['name'].strip()
        staff['subjects'] = request.form.getlist('subjects')
        staff['departments'] = request.form.getlist('departments')
        save_staff(staff_list)
        return redirect(url_for('staff_page'))

    # On GET, send staff data and departments to template
    return render_template('edit_staff.html', staff=staff, departments=departments)

if __name__ == '__main__':
    app.run(debug=True)
