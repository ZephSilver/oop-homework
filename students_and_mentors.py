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

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented

        self_all_numbers = [num for sublist in self.grades.values() for num in sublist]
        self_avg = sum(self_all_numbers) / len(self_all_numbers) if self_all_numbers else 0

        other_all_numbers = [num for sublist in other.grades.values() for num in sublist]
        other_avg = sum(other_all_numbers) / len(other_all_numbers) if other_all_numbers else 0

        return self_avg == other_avg

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented

        self_all_numbers = [num for sublist in self.grades.values() for num in sublist]
        self_avg = sum(self_all_numbers) / len(self_all_numbers) if self_all_numbers else 0

        other_all_numbers = [num for sublist in other.grades.values() for num in sublist]
        other_avg = sum(other_all_numbers) / len(other_all_numbers) if other_all_numbers else 0

        return self_avg < other_avg

    def __str__(self):
        all_numbers = [num for sublist in self.grades.values() for num in sublist]
        return (f"Имя: {self.name} \n"
                f"Фамилия: {self.surname} \n"
                f"Средняя оценка за домашние задания: {round(sum(all_numbers) / len(all_numbers) if all_numbers else 0, 2)} \n"
                f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)} \n" 
                f"Завершенные курсы: {', '.join(self.finished_courses)}")

    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if 0 < grade <= 10:
                if course in lecturer.grades:
                    lecturer.grades[course] += [grade]
                else:
                    lecturer.grades[course] = [grade]
            else:
                return "Ошибка! Оценка должна быть от 0 до 10"
        else:
            return "Ошибка"


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

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented

        self_all_numbers = [num for sublist in self.grades.values() for num in sublist]
        self_avg = sum(self_all_numbers) / len(self_all_numbers) if self_all_numbers else 0

        other_all_numbers = [num for sublist in other.grades.values() for num in sublist]
        other_avg = sum(other_all_numbers) / len(other_all_numbers) if other_all_numbers else 0

        return self_avg == other_avg

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented

        self_all_numbers = [num for sublist in self.grades.values() for num in sublist]
        self_avg = sum(self_all_numbers) / len(self_all_numbers) if self_all_numbers else 0

        other_all_numbers = [num for sublist in other.grades.values() for num in sublist]
        other_avg = sum(other_all_numbers) / len(other_all_numbers) if other_all_numbers else 0

        return self_avg < other_avg

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
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if 0 < grade <= 10:
                if course in student.grades:
                    student.grades[course] += [grade]
                else:
                    student.grades[course] = [grade]
            else:
                return "Ошибка! Оценка должна быть от 0 до 10"
        else:
            return "Ошибка"


# best_student = Student('Ruoy', 'Eman', 'your_gender')
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
