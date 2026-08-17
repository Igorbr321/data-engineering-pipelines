# Create an empty dictionary to store student information
student = dict()

# Input the student's name
student['Name'] = str(input('Name: '))

# Input the student's average grade and store it as a float
student['Average'] = float(input('Average grade for {} : '.format(student['Name'])))

# Determine the student's status based on their average grade
if student['Average'] >= 7:
    student['Status'] = 'Approved'
elif student['Average'] >= 5:
    student['Status'] = 'Recovery'
else:
    student['Status'] = 'Failed'

# Print each key-value pair in the student dictionary
for k, v in student.items():
    print('- {} is equal to {}.'.format(k, v))




