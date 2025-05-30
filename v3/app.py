from flask import Flask, render_template, request, send_file
import io
from openpyxl import Workbook

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    timetable = None
    classrooms = 0
    days_options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    replace = 0

    if request.method == 'POST':
        days = request.form.getlist('days')
        replace = int(request.form.get('replace'))
        subjects = request.form.get('subjects').strip().split(',')
        classrooms = int(request.form.get('classrooms'))

        timetable = {}
        sub_index = 0
        for day in days:
            timetable[day] = {}
            for cr in range(1, classrooms + 1):
                timetable[day][f'Classroom {cr}'] = []
                for slot in range(replace):
                    timetable[day][f'Classroom {cr}'].append(subjects[sub_index % len(subjects)].strip())
                    sub_index += 1

    return render_template('index.html', timetable=timetable, days_options=days_options, classrooms=classrooms, replace=replace)

@app.route('/download/xlsx', methods=['POST'])
def download_xlsx():
    import json

    data = request.form.get('timetable_data')
    timetable = json.loads(data)

    wb = Workbook()
    ws = wb.active
    ws.title = "Time Table"

    # timetable is day -> classroom -> list of subjects

    # Write header row
    # First cell empty, then for each classroom and slot, a header cell
    classrooms = []
    for day in timetable:
        classrooms = list(timetable[day].keys())
        break  # get classrooms from first day only

    # Write days, classrooms, and replace horizontally
    # Format: Day | Classroom 1 Slot 1 | Classroom 1 Slot 2 | ... | Classroom 2 Slot 1 | ...
    header = ['Day']
    slot_count = 0
    if classrooms:
        slot_count = len(timetable[list(timetable.keys())[0]][classrooms[0]])

    for cr in classrooms:
        for s in range(1, slot_count + 1):
            header.append(f'{cr} Slot {s}')
    ws.append(header)

    for day, class_dict in timetable.items():
        row = [day]
        for cr in classrooms:
            row.extend(class_dict[cr])
        ws.append(row)

    # Save to bytes buffer
    bio = io.BytesIO()
    wb.save(bio)
    bio.seek(0)

    return send_file(
        bio,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='timetable.xlsx'
    )

if __name__ == '__main__':
    app.run(debug=True)
