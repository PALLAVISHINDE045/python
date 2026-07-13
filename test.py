# 1 Student -5 variables
student1_name = "vinayak"
student1_marks = 85
student1_roll_number = 101
student_subject = "Mathematics"
student1_city = "hingoli"

student = 44
#List
students = ["pallavi", "sneha", "priya", "ankita", "vinayak"]
marks = [90, 85, 88, 92, 80]
roll_numbers = [101, 102, 103, 104, 105]
subjects = ["Mathematics", "Science", "English", "History", "Geography"]
cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata"]

# Get roll nmber of sneha
# rolls[1] = 102

#solution - Dictionary
# Dictionary - Key:value pair

student = {
    "name": "vinayak",
    "marks": 85,
    "roll_number": 101,
    "subject": "Mathematics",
    "city": "hingoli"
}

# Accessing values from the dictionary
print(student["name"])
print(student["marks"])
print(student["roll_number"])
print(student["subject"])
print(student["city"])

#Update values in the dictionary
student["marks"] = 90
print(student["marks"])

#New field
student ["grade"] = "A"
print(student["grade"])

#check
print("name" in student) #True
print("age" in student) #False

#keys and values
print(student.keys())
print(student.values())