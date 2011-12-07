from sqlalchemy.sql import select, and_, insert


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
        return insert(self.student, {username: username, name: name}) 

    def addSemester(self, name):
        return id(self.semester.insert().execute(name=name))

    def delete_semester(self, id):
        self.semester.delete().where(self.semester.c.id == id).execute()

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

    @all
    def listHourEntries(self, student_id, semester_id):
        return select([self.hours_entry], 
                and_(self.hours_entry.c.student == student_id, 
                     self.hours_entry.c.semester == semester_id))
                
    def getTotalHoursForStudent(self, student_id, semester_id):
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

