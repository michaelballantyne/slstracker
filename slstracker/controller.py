from slstracker import app, model
from flask import render_template, request, url_for, redirect, session, flash
from functools import wraps

def is_admin():
    return session['admin']

def logged_in(view):
    @wraps(view)
    def new_view(*args,**kwargs):
        if 'username' in session:
            return view(*args,**kwargs)
        else:
            return redirect(url_for('show_login'))

    return new_view

def admin(view):
    @wraps(view)
    def new_view(*args,**kwargs):
        if is_admin():
            return view(*args,**kwargs)
        else:
            return "You are trying to access an admin page when logged in as a regular user"
    
    return logged_in(new_view)

@app.route('/')
@logged_in
def index():
    if is_admin():
        return show_semesters()
    else:
        return show_semesters()


@app.route('/semesters/')
@logged_in
def show_semesters():
    if is_admin():
        semesters = model.listSemesters()
        semesters = [dict(row) for row in semesters]

        for semester in semesters:
            semester["hours"] = model.getTotalHours(None, semester['id'])

        return render_template('semesters.html', semesters=semesters)
    else:
        id = session['userid']
        semesters = model.listSemesters()

        semesters = [dict(row) for row in semesters]

        for semester in semesters:
            semester["hours"] = model.getTotalHours(None, semester['id'])

        return render_template('semesters_student_view.html', 
                student = model.getStudent(id), 
                semesters = semesters,
                hours = model.getTotalHours(id, None))

@app.route('/semesters/', methods=['POST'])
@admin
def new_semester():
    model.addSemester(request.form['name'])
    return redirect(url_for('show_semesters'))

@app.route('/semesters/<id>', methods=['POST'])
@logged_in
def add_hours(id):
    model.addHourEntry(session['userid'], int(id), request.form['date'], request.form['hours'], request.form['activity'])
    return redirect(url_for('show_semester', id=id))

@app.route('/semesters/<id>/hours/<hid>')
@logged_in
def delete_hours(id, hid):
    if request.args.get('_method', default=None) == 'DELETE':
        model.delete_hours(int(hid))

    return redirect(url_for('show_semester', id=id))


@app.route('/semesters/<id>', methods=['DELETE'])
@admin
def delete_semester(id):
    if not model.semesterHasEntries(int(id)):
        model.delete_semester(int(id));
    else:
        flash("Students have entered hours for that semester - it can no longer be deleted")
    return redirect(url_for('show_semesters'))

@app.route('/semesters/<id>/close')
@admin
def close_semester(id):
    model.close_semester(int(id));
    return redirect(url_for('show_semester', id=id))

@app.route('/semesters/<id>/open')
@admin
def open_semester(id):
    model.open_semester(int(id));
    return redirect(url_for('show_semester', id=id))

@app.route('/semesters/<id>')
@logged_in
def show_semester(id):
    if request.args.get('_method', default=None) == 'DELETE':
        return delete_semester(id)
    else:
        if is_admin():
            students = model.listStudentsForSemester(id)
            students = [dict(row) for row in students]

            for student in students:
                student["hours"] = model.getTotalHours(student["id"], id)

            return render_template('semester_students.html', 
                    students = students,
                    semester = model.getSemester(id),
                    hours = model.getTotalHours(None, id))
        else:
            student_id = session['userid']
            return render_template('hours_student_view.html', 
            student = model.getStudent(student_id),
            semester = model.getSemester(int(id)),
            entries = model.listHourEntries(student_id, int(id)),
            hours = model.getTotalHours(student_id, int(id)))

@app.route('/students/<id>')
@admin
def show_student(id):
    semesters = model.listSemestersForStudent(id)

    semesters = [dict(row) for row in semesters]

    for semester in semesters:
        semester["hours"] = model.getTotalHours(None, semester['id'])

    return render_template('student_semesters.html', 
            student = model.getStudent(id), 
            semesters = semesters,
            hours = model.getTotalHours(id, None))

@app.route('/students/')
@admin
def show_students():
    students = model.listStudents()
    students = [dict(row) for row in students]

    for student in students:
        student["hours"] = model.getTotalHours(student["id"], None)

    return render_template('students.html', students = students)

@app.route('/students/<student_id>/semesters/<semester_id>')
@app.route('/semesters/<semester_id>/students/<student_id>')
@admin
def show_hours(student_id, semester_id):
    return render_template('hours.html', 
            student = model.getStudent(student_id),
            semester = model.getSemester(semester_id),
            entries = model.listHourEntries(student_id, semester_id),
            hours = model.getTotalHours(student_id, semester_id))

@app.route('/login/')
def show_login():
    return render_template('login.html')

@app.route('/login/', methods=['POST'])
def login():
    username = request.form['username']
    fullname = request.form['name'] 

    session['username'] = username
    session['name'] = fullname 

    if session['username'] == 'admin':
        session['admin'] = True
    else:
        session['admin'] = False
        user = model.findStudent(username)
        print username
        print user
        if user is None:
            model.addStudent(username, fullname)
            user = model.findStudent(username)
        session['userid'] = user.id

    return redirect("/")

@app.route('/logout/')
def logout():
    session.pop('username')
    session.pop('name')
    session.pop('admin')
    return redirect("/login/")
