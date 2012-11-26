from sqlalchemy.sql import select, and_, join


class Model:
    def __init__(self, meta):
        self.engine = meta.bind
        for (tablename, table) in meta.tables.iteritems():
            setattr(self, tablename, table)

    def id(self, insert_result):
        return insert_result.inserted_primary_key[0]

    def all(query):
        return lambda self, *args: self.engine.execute(query(self, *args)).fetchall()

    def one(query):
        return lambda self, *args: self.engine.execute(query(self, *args)).fetchone()


    def addStudent(self, username, name):
        return self.student.insert().execute(username=username, name=name) 

    def addSemester(self, name):
        return id(self.semester.insert().execute(name=name, active=True))

    def delete_semester(self, id):
        self.semester.delete().where(self.semester.c.id == id).execute()

    def delete_hours(self, id):
        self.hours_entry.delete().where(self.hours_entry.c.id == id).execute()

    def close_semester(self, id):
        self.semester.update().values(active=False).where(self.semester.c.id == id).execute()

    def open_semester(self, id):
        self.semester.update().values(active=True).where(self.semester.c.id == id).execute()

    def semesterHasEntries(self, id):
        return 0 != self.student_semester.count(self.student_semester.c.semester == id).execute().first()[0]

    @one
    def getStudentSemester(self, student_id, semester_id):
        return select([self.student_semester],
                and_(self.student_semester.c.student == student_id,
                    self.student_semester.c.semester == semester_id))

    @all 
    def getSemesterReflections(self, semester_id):
        return select([self.student_semester.c.reflection, self.student.c.name, self.semester.c.name],
                self.student_semester.c.semester == semester_id, [join(self.student_semester, self.student).join(self.semester)], use_labels=True);

    def getReflection(self, student_id, semester_id):
        studentSemester = self.getStudentSemester(student_id, semester_id)

        if studentSemester is not None and studentSemester.reflection is not None:
             return studentSemester.reflection
        else:
             return ""

    def updateReflection(self, student_id, semester_id, reflection):
        print reflection
        if self.getStudentSemester(student_id, semester_id) is None:
            self.student_semester.insert().execute(student=student_id, semester=semester_id)

        self.student_semester.update().where(
                and_(self.student_semester.c.student == student_id, 
                    self.student_semester.c.semester == semester_id)) \
                .values(reflection=reflection).execute()

    def addHourEntry(self, student_id, semester_id, date, hours, activity, organization):
        if self.getStudentSemester(student_id, semester_id) is None:
            self.student_semester.insert().execute(student=student_id, semester=semester_id)

        self.hours_entry.insert().execute(student=student_id, semester=semester_id, event_date=date, hours=hours, activity=activity, organization=organization)

    @one
    def findStudent(self, name):
        return select([self.student], self.student.c.username == name)

    @all
    def listStudents(self):
        return select([self.student])

    @all
    def listSemesters(self):
        return select([self.semester])

    @all
    def listStudentsForSemester(self, semester_id):
        return select([self.student],
                and_(self.student.c.id == self.student_semester.c.student,
                     self.student_semester.c.semester == semester_id))

    @all
    def listSemestersForStudent(self, student_id):
        return select([self.semester],
                and_(self.semester.c.id == self.student_semester.c.semester,
                     self.student_semester.c.student == student_id))

    @one
    def getStudent(self, student_id):
        return select([self.student], self.student.c.id == student_id)

    @one
    def getSemester(self, semester_id):
        return select([self.semester], self.semester.c.id == semester_id)

    @one
    def findSemester(self, name):
        return select([self.semester], self.semester.c.name == name)

    @all
    def listHourEntries(self, student_id, semester_id):
        return select([self.hours_entry, self.organization.c.name], 
                and_(self.hours_entry.c.student == student_id, 
                     self.hours_entry.c.semester == semester_id), 
                [join(self.hours_entry, self.organization)])
                
    def getTotalHours(self, student_id, semester_id):
        total = 0

        query = select([self.hours_entry])
        if student_id is not None:
            query = query.where(self.hours_entry.c.student == student_id)

        if semester_id is not None:
            query = query.where(self.hours_entry.c.semester == semester_id)

        hours_entries = self.engine.execute(query)

        for entry in hours_entries:
            total += entry.hours

        return total

    @all
    def listOrganizations(self):
        return select([self.organization])

    def addOrganization(self, name, cname, cphone):
        return self.id(self.organization.insert().execute(name=name, contact_name=cname, contact_phone=cphone))

    @one
    def getOrganization(self, org_id):
        return select([self.organization], self.organization.c.id == org_id)
    
    @one
    def findOrganization(self, name):
        return select([self.organization], self.organization.c.name == name)

    def organizationHasEntries(self, id):
        return 0 != self.hours_entry.count(self.hours_entry.c.organization == id).execute().first()[0]

    def delete_organization(self, id):
        self.organization.delete().where(self.organization.c.id == id).execute()
