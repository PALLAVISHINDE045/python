def get_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

students = ("Karan", "Kartik", "Kunal", "Krushna")
marks = (85, 95, 86, 81)

for i in range(len(students)):
    grade = get_grade(marks[i])
    print(f"{students[i]} scored {marks[i]} and got grade {grade}")