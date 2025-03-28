from functools import total_ordering


@total_ordering
class Student:

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def _get_avg_grade(self):
        all_grades = [grade for course_grades in self.grades.values() for grade in course_grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._get_avg_grade() == other._get_avg_grade()

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._get_avg_grade() < other._get_avg_grade()

    def __str__(self):
        all_numbers = [num for sublist in self.grades.values() for num in sublist]
        return (f"Имя: {self.name} \n"
                f"Фамилия: {self.surname} \n"
                f"Средняя оценка за домашние задания: {round(sum(all_numbers) / len(all_numbers) if all_numbers else 0, 2)} \n"
                f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)} \n"
                f"Завершенные курсы: {', '.join(self.finished_courses)}")

    def rate_lecturer(self, lecturer, course, grade):
        if not isinstance(lecturer, Lecturer):
            raise TypeError("Оценивать можно только лекторов")
        if course not in self.courses_in_progress:
            raise ValueError("Студент не изучает этот курс")
        if course not in lecturer.courses_attached:
            raise ValueError("Лектор не преподает на этом курсе")
        if not (0 < grade <= 10):
            raise ValueError("Оценка должна быть от 1 до 10")
        if course in lecturer.grades:
            lecturer.grades[course] += [grade]
        else:
            lecturer.grades[course] = [grade]


class Mentor:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


@total_ordering
class Lecturer(Mentor):

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def _get_avg_grade(self):
        all_grades = [grade for course_grades in self.grades.values() for grade in course_grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._get_avg_grade() == other._get_avg_grade()

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._get_avg_grade() < other._get_avg_grade()

    def __str__(self):
        all_numbers = [num for sublist in self.grades.values() for num in sublist]
        return (f"Имя: {self.name} \n"
                f"Фамилия: {self.surname} \n"
                f"Средняя оценка за лекции: {round(sum(all_numbers) / len(all_numbers) if all_numbers else 0, 2)}")


class Reviewer(Mentor):

    def __str__(self):
        return (f"Имя: {self.name} \n"
                f"Фамилия: {self.surname}")

    def rate_hw(self, student, course, grade):
        if not isinstance(student, Student):
            raise TypeError("Оценивать можно только студентов")
        if course not in self.courses_attached:
            raise ValueError("Проверяющий не прикреплен к этому курсу")
        if course not in student.courses_in_progress:
            raise ValueError("Студент не учится на этом курсе")
        if not (0 < grade <= 10):
            raise ValueError("Оценка должна быть от 1 до 10")
        if course in student.grades:
            student.grades[course] += [grade]
        else:
            student.grades[course] = [grade]


def course_hw_avg(students, course):

    if not students:
        raise  ValueError("Список студентов не может быть пустым")

    all_grades = []

    for student in students:
        if not isinstance(student, Student):
            continue
        if course in student.grades:
            all_grades.extend(student.grades[course])

    if not all_grades:
        return 0

    return  round(sum(all_grades) / len(all_grades), 2)


def lecturers_grade_avg(lecturers, course):

    if not lecturers:
        raise  ValueError("Список студентов не может быть пустым")

    all_grades = []

    for lecturer in lecturers:
        if not isinstance(lecturer, Lecturer):
            continue
        if course in lecturer.grades:
            all_grades.extend(lecturer.grades[course])

    if not all_grades:
        return 0

    return  round(sum(all_grades) / len(all_grades), 2)


ivan_student = Student('Иван', 'Иванов', 'М')
ivan_student.courses_in_progress += ['Python', 'CSS']
piter_student = Student('Петр', 'Петров', 'М')
piter_student.courses_in_progress += ['Python', 'JS']

vasili_reviewer = Reviewer('Василий', 'Васькин')
vasili_reviewer.courses_attached += ['Python', 'CSS']
george_reviewer = Reviewer('Георгий', 'Гошин')
george_reviewer.courses_attached += ['Python', 'JS']

nikolay_lecturer = Lecturer('Николай', 'Николин')
nikolay_lecturer.courses_attached += ['Python', 'CSS']
eugene_lecturer = Lecturer('Евгений', 'Евгенин')
eugene_lecturer.courses_attached += ['Python', 'JS']

ivan_student.rate_lecturer(nikolay_lecturer, 'Python', 9)

vasili_reviewer.rate_hw(piter_student, 'Python', 8)

ivan_student.grades['Python'] = [1, 6, 7, 3]
ivan_student.grades['CSS'] = [4, 8, 1, 9]

piter_student.grades['Python'] += [8, 3, 4, 3]
piter_student.grades['JS'] = [2, 8, 3, 9]

nikolay_lecturer.grades['Python'] += [2, 7, 8, 9]
nikolay_lecturer.grades['CSS'] = [5, 6, 7, 10]

eugene_lecturer.grades['Python'] = [2, 4, 8, 1]
eugene_lecturer.grades['JS'] = [5, 4, 7, 9]
print()
print(ivan_student, piter_student, nikolay_lecturer, eugene_lecturer, vasili_reviewer, george_reviewer, sep="\n\n")
print()
print(ivan_student >= piter_student)
print(nikolay_lecturer < eugene_lecturer)

print()
hw_course_avg = course_hw_avg([piter_student, ivan_student], 'Python')
print(f'Средняя оценка студентов по курсу Python: {hw_course_avg}')
lecturers_course_avg = lecturers_grade_avg([nikolay_lecturer, eugene_lecturer], 'Python')
print(f'Средняя оценка лекторов по курсу Python: {lecturers_course_avg}')
# best_student.courses_in_progress += ['Python']
#
# cool_mentor = Mentor('Some', 'Buddy')
# cool_mentor.courses_attached += ['Python']
#
# cool_mentor.rate_hw(best_student, 'Python', 10)
# cool_mentor.rate_hw(best_student, 'Python', 10)
# cool_mentor.rate_hw(best_student, 'Python', 10)
#
# print(best_student.grades)
