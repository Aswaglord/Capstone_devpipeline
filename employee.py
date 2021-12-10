from user import User
import sqlite3

connection = sqlite3.connect('competency_tracker.db')
cursor = connection.cursor()

class Employee(User):

    def view_personal_info(self):
        run = True
        while run:
            print()
            print('''
what would you like to view:
[1] view competencies
[2] view assessments
''')
            option = input()

            if option == '1':
                rows = cursor.execute('SELECT c.name, cr.level FROM competency_results cr, Competencies c WHERE person_id = ? AND c.comp_id=cr.comp_id', (self.user_id[0],)).fetchall()
                print('Competency      Level')
                for row in rows:
                    print(f'{row[0]:<15} {row[1]}')
            elif option == '2':
                rows = cursor.execute('SELECT a.name, ar.score FROM Assessments a, assessment_results ar WHERE ar.person_id = ? AND a.assessment_id=ar.assessment_id', (self.user_id[0],)).fetchall()
                print('Assessment                Score')
                for row in rows:
                    print(f'{row[0]:<25} {row[1]}')

            continue_updating = input('\nWould you like to view something else? (type <Y> for Yes, or <ENTER> for menu)').upper()

            if continue_updating == '':
                run = False