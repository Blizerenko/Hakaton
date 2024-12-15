import json
import os
import datetime

# Определение пути к файлу для хранения данных
data_file_path = "school_helper_data.json"

# Список заданий с дедлайнами
assignments = [
    {"subject": "Math", "task": "Solve equations", "deadline": "2024-12-18"},
    {"subject": "English", "task": "Read the book", "deadline": "2024-12-20"},
    {"subject": "History", "task": "Write essay", "deadline": "2024-12-25"},
]

# Класс для работы с оценками
class GradeSystem:
    def init(self):
        self.grades = {}

    def add_grade(self, subject, student, grade):
        if subject not in self.grades:
            self.grades[subject] = {}
        if student not in self.grades[subject]:
            self.grades[subject][student] = []
        self.grades[subject][student].append(grade)
        print(f"Оценка {grade} добавлена ученику {student} по предмету '{subject}'.")

    def display_grades(self, role, student=None):
        if not self.grades:
            print("Оценки отсутствуют.")
            return

        if role == "Учитель":
            print("Оценки по предметам:")
            for subject, students in self.grades.items():
                print(f"{subject}:")
                for student, grades in students.items():
                    grades_list = ', '.join(map(str, grades))
                    print(f"  {student}: {grades_list}")
        elif role == "Ученик" and student:
            print(f"Оценки ученика {student}:")
            for subject, students in self.grades.items():
                if student in students:
                    grades_list = ', '.join(map(str, students[student]))
                    print(f"  {subject}: {grades_list}")
        elif role == "Родитель" and student:
            if student in self.grades.get("Math", {}):  # Предположим, что родитель всегда видит все оценки
                print(f"Оценки ученика {student}:")
                for subject, students in self.grades.items():
                    if student in students:
                        grades_list = ', '.join(map(str, students[student]))
                        print(f"  {subject}: {grades_list}")

    def display_statistics(self):
        if not self.grades:
            print("Статистика отсутствует, так как нет оценок.")
            return
        print("Статистика успеваемости:")
        for subject, students in self.grades.items():
            all_grades = [grade for grades in students.values() for grade in grades]
            average = sum(all_grades) / len(all_grades) if all_grades else 0
            print(f"{subject}: Средний балл - {round(average, 2)}")

# Функции для работы с расписанием и домашними заданиями
def load_data():
    if os.path.isfile(data_file_path):
        try:
            with open(data_file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Ошибка чтения данных. Файл поврежден. Начинаем с пустых данных.")
    return {"schedule": {}, "homework": []}

def save_data(data):
    with open(data_file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def add_schedule(data):
    day = input("Введите день недели (например, Понедельник): ").strip().capitalize()
    subjects = input("Введите предметы, разделённые запятой: ").strip().split(",")
    if subjects:
        data["schedule"][day] = [subject.strip() for subject in subjects]
        print(f"Расписание для {day} обновлено.")
    else:
        print("Вы не ввели ни одного предмета.")
    save_data(data)

def view_schedule(data):
    day = input("Введите день недели для просмотра расписания: ").strip().capitalize()
    schedule = data.get("schedule", {}).get(day)
    if schedule:
        print(f"Расписание на {day}:")
        for idx, subject in enumerate(schedule, 1):
            print(f"{idx}. {subject}")
    else:
        print(f"Для {day} расписания нет.")

#############################


def add_homework(data):
    subject = input("Введите предмет: ").strip()
    task = input("Введите задание: ").strip()
    if subject and task:
        data["homework"].append({"subject": subject, "task": task, "completed": False})
        print("Домашнее задание добавлено.")
    else:
        print("Ошибка: предмет и задание не могут быть пустыми.")
    save_data(data)

def view_homework(data):
    homework_list = data.get("homework", [])
    if homework_list:
        print("Домашние задания:")
        for idx, hw in enumerate(homework_list, 1):
            status = "✓" if hw["completed"] else "✗"
            print(f"{idx}. [{status}] {hw['subject']}: {hw['task']}")
    else:
        print("Список домашних заданий пуст.")

def mark_homework_completed(data):
    view_homework(data)
    try:
        index = int(input("Введите номер задания для отметки как выполненного: ")) - 1
        homework_list = data.get("homework", [])
        if 0 <= index < len(homework_list):
            homework_list[index]["completed"] = True
            print("Задание отмечено как выполненное.")
        else:
            print("Неверный номер задания.")
    except ValueError:
        print("Ошибка: Введите число.")
    save_data(data)

def delete_homework(data):
    view_homework(data)
    try:
        index = int(input("Введите номер задания для удаления: ")) - 1
        homework_list = data.get("homework", [])
        if 0 <= index < len(homework_list):
            removed_task = homework_list.pop(index)
            print(f"Удалено задание: {removed_task['subject']} - {removed_task['task']}")
        else:
            print("Неверный номер задания.")
    except ValueError:
        print("Ошибка: Введите число.")
    save_data(data)

def check_deadlines(assignments):
    today = datetime.date.today()
    found = False
    for assignment in assignments:
        deadline = datetime.datetime.strptime(assignment["deadline"], "%Y-%m-%d").date()
        if deadline <= today + datetime.timedelta(days=3):  # Напоминаем за 3 дня до дедлайна
            print(f"Reminder: Deadline for '{assignment['task']}' in {assignment['subject']} is approaching! Due date: {deadline}")
            found = True
    if not found:
        print("No upcoming deadlines.")

def add_assignment():
    subject = input("Enter the subject: ")
    task = input("Enter the task description: ")
    deadline_input = input("Enter the deadline (YYYY-MM-DD): ")
    
    try:
        deadline = datetime.datetime.strptime(deadline_input, "%Y-%m-%d").date()
        assignments.append({"subject": subject, "task": task, "deadline": str(deadline)})
        print(f"New task '{task}' in {subject} has been added with deadline {deadline}.")
    except ValueError:
        print("Invalid date format. Please enter the date in the format YYYY-MM-DD.")

def remove_assignment_by_task():
    task_name = input("Enter the name of the task to remove: ")
    global assignments
    before_count = len(assignments)
    assignments = [assignment for assignment in assignments if assignment["task"] != task_name]
    if len(assignments) < before_count:
        print(f"Task '{task_name}' has been removed.")
    else:
        print(f"Task '{task_name}' not found.")

def view_assignments():
    if not assignments:
        print("No assignments available.")
    else:
        print("Current assignments:")
        for i, assignment in enumerate(assignments, start=1):
            print(f"{i}. Subject: {assignment['subject']}, Task: {assignment['task']}, Deadline: {assignment['deadline']}")

# Обёртка для обработки ввода
def input_handler(prompt):
    try:
        return input(prompt)
    except OSError:
        print("Ввод недоступен в текущей среде.")
        return ""

# Основное меню программы
def main_menu():
    data = load_data()
    grade_system = GradeSystem()

    role = input("Выберите роль (Учитель/Ученик/Родитель): ").strip().capitalize()





    ##################################


    options = {
        "Учитель": {
            "1": ("Добавить расписание", add_schedule),
            "2": ("Просмотреть расписание", view_schedule),
            "3": ("Добавить домашнее задание", add_homework),
            "4": ("Просмотреть домашние задания", view_homework),
            "5": ("Удалить домашнее задание", delete_homework),
            "8": ("Добавить оценку", grade_system.add_grade),
            "9": ("Показать оценки", grade_system.display_grades),
            "10": ("Показать статистику успеваемости", grade_system.display_statistics),
        },
        "Ученик": {
            "2": ("Просмотреть расписание", view_schedule),
            "3": ("Просмотреть домашние задания", view_homework),
            "4": ("Отметить домашнее задание как выполненное", mark_homework_completed),
            "5": ("Проверить дедлайны", check_deadlines),
            "6": ("Просмотреть задания", view_assignments),
            "9": ("Показать оценки", grade_system.display_grades),
        },
        "Родитель": {
            "9": ("Показать оценки", grade_system.display_grades),
        }
    }

    while True:
        if role not in options:
            print("Неверная роль. Попробуйте снова.")
            role = input("Выберите роль (Учитель/Ученик/Родитель): ").strip().capitalize()
            continue

        print(f"\nДобро пожаловать, {role}!")
        for key, (desc, _) in options[role].items():
            print(f"{key}. {desc}")

        choice = input_handler("Выберите действие: ").strip()

        if choice in options[role]:
            if choice == "7":
                print("До свидания!")
                break
            elif choice == "8":
                subject = input("Введите предмет: ")
                student = input("Введите имя ученика: ")
                try:
                    grade = float(input("Введите оценку (0-5): "))
                    if 0 <= grade <= 5:
                        grade_system.add_grade(subject, student, grade)
                    else:
                        print("Ошибка: Оценка должна быть в диапазоне от 0 до 5.")
                except ValueError:
                    print("Ошибка: Пожалуйста, введите числовое значение для оценки.")
            else:
                options[role][choice][1](data)
        else:
            print("Неверный выбор. Попробуйте снова.")

# Запуск программы
if name == "main":
    main_menu()
