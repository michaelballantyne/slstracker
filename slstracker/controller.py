from slstracker import app, model
from flask import g, render_template, request, url_for, redirect, flash, jsonify, abort 

@app.before_request
def auth():
    try:
        g.username = request.environ['REMOTE_USER']
        g.fullname = request.environ['fullname']
    except KeyError:
        return abort(500)

    g.admin = g.username in app.config['ADMIN_USERS']

    if not g.admin:
        user = model.findStudent(g.username)
        if user is None:
            model.addStudent(g.username, g.fullname)
            user = model.findStudent(g.username)

        g.user_id = user.id

    if 'admin' in request.path and not g.admin:
        return abort(403)

@app.route('/')
def index():
    if g.admin:
        return redirect(url_for('admin_show_semesters'))
    else:
        return show_semesters()


def show_semesters():
    semesters = model.listSemesters()

    semesters = [dict(row) for row in semesters]

    for semester in semesters:
        semester["hours"] = model.getTotalHours(g.user_id, semester['id'])

    return render_template('semesters.html', 
            student = model.getStudent(g.user_id), 
            semesters = semesters,
            hours = model.getTotalHours(g.user_id, None))

@app.route('/semesters/<id>/hours')
def show_hours(id):
    return render_template('hours.html', 
        student = model.getStudent(g.user_id),
        semester = model.getSemester(int(id)),
        entries = model.listHourEntries(g.user_id, int(id)),
        hours = model.getTotalHours(g.user_id, int(id)))

@app.route('/semesters/<id>/reflection')
def show_reflection(id):
    return render_template('reflection.html',
        student = model.getStudent(g.user_id),
        semester = model.getSemester(int(id)),
        reflection = model.getReflection(g.user_id, int(id)))


@app.route('/semesters/<id>/reflection', methods=['POST'])
def updateReflection(id):
    model.updateReflection(g.user_id, int(id), request.form['reflection'])
    return redirect(url_for('show_reflection', id=id))

@app.route('/semesters/<id>/hours', methods=['POST'])
def add_hours(id):
    model.addHourEntry(g.user_id, int(id), request.form['date'], int(request.form['hours']), request.form['activity'], int(request.form['organization']))
    return redirect(url_for('show_semester', id=id) + '#enterhours')

@app.route('/semesters/<id>/hours/<hid>')
def delete_hours(id, hid):
    if request.args.get('_method', default=None) == 'DELETE':
        model.delete_hours(int(hid), )

    return redirect(url_for('show_semester', id=id))

@app.route('/organizations/')
def organizations_json():
    return jsonify({'organizations': [[x['name'], x['contact_name'],x['contact_phone'], x['id']] for x in model.listOrganizations()]})

@app.route('/organizations/', methods=['POST'])
def add_organization_json():
    if not model.findOrganization(request.form['name']):
        id = model.addOrganization(request.form['name'], request.form['contact_name'], request.form['contact_phone'])
        return jsonify({'id': id})
    else:
        return jsonify({'error': {'name': 'An organization of that name is already present in the system, and duplicates are not supported'}})


@app.route('/admin/organizations/', methods=['POST'])
def admin_add_organization():
    if not model.findOrganization(request.form['name']):
        model.addOrganization(request.form['name'], request.form['contact_name'], request.form['contact_phone'])
    else:
        flash('An organization of that name is already present in the system, and duplicates are not supported')
    return redirect(url_for('admin_show_organizations'))

@app.route('/admin/semesters/')
def admin_show_semesters():
    semesters = model.listSemesters()
    semesters = [dict(row) for row in semesters]

    for semester in semesters:
        semester["hours"] = model.getTotalHours(None, semester['id'])

    return render_template('admin/semesters.html', semesters=semesters)

@app.route('/admin/semesters/', methods=['POST'])
def admin_new_semester():
    if not model.findSemester(request.form['name']):
        model.addSemester(request.form['name'])
    else:
        flash('A semester of that name is already present in the system, and duplicates are not supported')
    return redirect(url_for('admin_show_semesters'))

@app.route('/admin/semesters/<id>', methods=['DELETE'])
def admin_delete_semester(id):
    if not model.semesterHasEntries(int(id)):
        model.delete_semester(int(id));
    else:
        flash("Students have entered hours for that semester - it can no longer be deleted")
    return redirect(url_for('admin_show_semesters'))

@app.route('/admin/semesters/<id>/close')
def admin_close_semester(id):
    model.close_semester(int(id));
    return redirect(url_for('admin_show_semester', id=id))

@app.route('/admin/semesters/<id>/open')
def admin_open_semester(id):
    model.open_semester(int(id));
    return redirect(url_for('admin_show_semester', id=id))

@app.route('/admin/semesters/<id>')
def admin_show_semester(id):
    if request.args.get('_method', default=None) == 'DELETE':
        return admin_delete_semester(id)
    else:
        students = model.listStudentsForSemester(id)
        students = [dict(row) for row in students]

        for student in students:
            student["hours"] = model.getTotalHours(student["id"], id)

        return render_template('admin/semester_students.html', 
                students = students,
                semester = model.getSemester(id),
                hours = model.getTotalHours(None, id),
                reflections = model.getSemesterReflections(id))

@app.route('/admin/students/')
def show_students():
    students = model.listStudents()
    students = [dict(row) for row in students]

    for student in students:
        student["hours"] = model.getTotalHours(student["id"], None)

    return render_template('admin/students.html', students = students)

@app.route('/admin/students/<id>')
def admin_show_student(id):
    semesters = model.listSemestersForStudent(id)

    semesters = [dict(row) for row in semesters]

    for semester in semesters:
        semester["hours"] = model.getTotalHours(None, semester['id'])

    return render_template('admin/student_semesters.html', 
            student = model.getStudent(id), 
            semesters = semesters,
            hours = model.getTotalHours(id, None))

@app.route('/admin/students/<student_id>/semesters/<semester_id>')
@app.route('/admin/semesters/<semester_id>/students/<student_id>')
def admin_show_hours(student_id, semester_id):
    return render_template('admin/hours.html', 
            student = model.getStudent(student_id),
            semester = model.getSemester(semester_id),
            entries = model.listHourEntries(student_id, semester_id),
            hours = model.getTotalHours(student_id, semester_id),
            reflection = model.getReflection(student_id, semester_id))

@app.route('/organizations/<id>/popup')
def organization_popup(id):
    return render_template('orgpopup.html',
            organization = model.getOrganization(int(id)))

@app.route('/admin/organizations/')
def admin_show_organizations():
    return render_template('admin/organizations.html',
            organizations = model.listOrganizations())
    
@app.route('/admin/organizations/<id>', methods=['DELETE'])
def admin_delete_organization(id):
    if not model.organizationHasEntries(int(id)):
        model.delete_organization(int(id));
    else:
        flash("Students have entered hours for that organization - it can no longer be deleted")
    return redirect(url_for('admin_show_organizations'))

@app.route('/admin/organizations/<id>')
def admin_show_organization(id):
    if request.args.get('_method', default=None) == 'DELETE':
        return admin_delete_organization(id)
