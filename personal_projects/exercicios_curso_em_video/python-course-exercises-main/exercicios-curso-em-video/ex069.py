# Generation of names, ages and sexes
from faker import Faker

fake = Faker()

num_entries = int(input('Type it quantity of names, ages and sexes you want to generate: '))

name_list = []
age_list = []
sex_list = []

for _ in range(num_entries):

    name = fake.name()
    age = fake.random_int(min=12, max=35)
    sex = fake.random_element(elements=('Male', 'Female'))

    name_list.append(name.strip().upper())
    age_list.append(age)
    sex_list.append(sex[0])

# Storing in the list
print('=-=-=' * 15)
print('                     Registration of people')
print('=-=-=' * 15)

for i in range(num_entries):
    print('Name: {}, Age: {}, Sex: {}'.format(
        name_list[i], age_list[i], sex_list[i]))

print('''\nList of names: {}
List of ages: {}
List of sex: {}'''.format(name_list, age_list, sex_list))

# Data analysis in age
age_cont = 0
for age in age_list:
    if age > 18:
        age_cont += 1

print('\nNumber of people over 18: {} people.'.format(age_cont))

# Data analysis in Sex
sex_cont = 0
for sex in sex_list:
    if sex == 'M':
        sex_cont += 1

print('In the list, there are {} male sex.'.format(sex_cont))

# Data analysis - womans with less 20 years.
woman_less_20 = 0
for sex_woman, age_woman in zip(sex_list, age_list):
    if sex_woman == 'F' and age_woman < 20:
        woman_less_20 += 1

print('Womans with less 20 years: {} womans'.format(woman_less_20))
