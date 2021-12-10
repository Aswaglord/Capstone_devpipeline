from user import *
from manager import *
from employee import *
import sqlite3
import bcrypt

connection = sqlite3.connect('competency_tracker.db')
cursor = connection.cursor()

def create_schema():
    with open('schema.sql') as my_file:
        sqlfile = my_file.read()
        cursor.executescript(sqlfile)
    connection.commit()

create_schema()

def start_program():
    
    credentials_incorrect = True
    while credentials_incorrect:
        username = input('Enter Username (<ENTER> to exit program):\n')

        if username == '':
            exit()

        password = input('Enter password:\n').encode('utf-8')

        salt = b'$2b$12$hXV7K881YN/7dmizgNoyL.'

        hashed = bcrypt.hashpw(password, salt)
        str_hashed = hashed.decode('utf-8')

        try_user = User(username, str_hashed)

        if try_user.check_credentials():
            credentials_incorrect = False
            find_type_user = cursor.execute('SELECT first_name, last_name, user_type FROM Users WHERE username=? AND password=?',(username, str_hashed,)).fetchone()

            menu = True
            
            print(f'\nWelcome, {find_type_user[0]} {find_type_user[1]}')
            while menu:
                if find_type_user[2] == 'Manager':
                    manager = Manager(username,password)
                    
                    print('''
what would you like to do:
[1] view all users
[2] search for user by first or last name
[3] view all user competencies by user
[4] view a report of all users and their competency levels for a given competency
[5] view a competency level report for an individual user
[6] view a list of assessments for a given user
[7] add a user
[8] add a new competency
[9] add a new assessment to a competency
[10] add an assessment result for a user
[11] add competency result
[12] edit a user's information
[13] edit a competency
[14] edit an assessment
[15] edit an assessment result
[16] delete an assessment result
[17] CSV: EXPORT: competency report by competency and users
[18] CSV: EXPORT: Competency report for a single user
[19] CSV: IMPORT: import assessment results from CSV
[20] Change my credentials
[L] logout
[Q] quit the program
''')
                    option = input()
                    if option == '1':
                        try:
                            manager.view_all()
                        except:
                            print('error: something went wrong')
                    elif option == '2':
                        try:
                            manager.search_users()
                        except:
                            print('error: something went wrong')
                    elif option == '3':
                        try:
                            manager.view_user_comp()
                        except:
                            print('error: something went wrong')
                    elif option == '4':
                        try:
                            manager.view_users_comp()
                        except:
                            print('error: something went wrong')
                    elif option == '5':
                        try:
                            manager.user_report()
                        except:
                            print('error: something went wrong')
                    elif option == '6':
                        try:
                            manager.assessment_list()
                        except:
                            print('error: something went wrong')
                    elif option == '7':
                        try:
                            manager.add_user()
                        except:
                            print('error: something went wrong')
                    elif option == '8':
                        try:
                            manager.add_competency()
                        except:
                            print('error: something went wrong')
                    elif option == '9':
                        try:
                            manager.add_assessment()
                        except:
                            print('error: something went wrong')
                    elif option == '10':
                        try:
                            manager.add_assessment_result()
                        except:
                            print('error: something went wrong')
                    elif option == '11':
                        try:
                            manager.add_competency_result()
                        except:
                            print('error, something went wrong')
                    elif option == '12':
                        try:
                            manager.edit_user()
                        except:
                            print('error: something went wrong')
                    elif option == '13':
                        try:
                            manager.edit_competency()
                        except:
                            print('error: something went wrong')
                    elif option == '14':
                        try:
                            manager.edit_assessment()
                        except:
                            print('error: something went wrong')
                    elif option == '15':
                        try:
                            manager.edit_assessment_result()
                        except:
                            print('error: something went wrong')
                    elif option == '16':
                        try:
                            manager.delete_assessment_result()
                        except:
                            print('error: something went wrong')
                    elif option == '17':
                        try:
                            manager.export_comp_report()
                        except:
                            print('error: something went wrong')
                    elif option == '18':
                        try:
                            manager.export_single_user_comp()
                        except:
                            print('error, something went wrong')
                    elif option == '19':
                        try:
                            manager.import_csv_assessments()
                        except:
                            print('error, something went wrong')
                    elif option == '20':
                        try:
                            manager.change_credentials()
                        except:
                            print('error, something went wrong')
                    elif option.upper() == 'L':
                        start_program()
                    elif option.upper() == 'Q':
                        exit()
                        


                elif find_type_user[2] == 'User':
                    run = True
                    while run:
                        user = Employee(username,password)
                        print('''
what would you like to do:
[1] change credentials
[2] view personal information
[L] logout
[Q] quit the program
    ''')
                        option = input()
                        if option == '1':
                            try:
                                user.change_credentials()
                            except:
                                print('error: something went wrong')
                        elif option == '2':
                            try:
                                user.view_personal_info()
                            except:
                                print('error: something went wrong')
                        elif option.upper() == 'L':
                            try:
                                start_program()
                            except: 
                                print('error, something went wrong')
                        elif option.upper() == 'Q':
                            exit()
        else:
            print('Wrong username or password, try again.')
                
start_program()




