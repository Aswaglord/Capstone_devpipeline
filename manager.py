from user import User
import sqlite3
import csv
import bcrypt

connection = sqlite3.connect('competency_tracker.db')
cursor = connection.cursor()

class Manager(User):

    def view_all(self):

        rows = cursor.execute('SELECT * FROM Users').fetchall()
        print('\nfirst_name   last_name     phone_number   email                  date_created    hire_date     user_type')

        for row in rows:
            print(
                f'{row[1]:<10}   {row[2]:<10}    {row[3]}   {row[4]:<20}   {row[8]:<12}    {row[9]:<12}  {row[10]:<10}')

        return_to_menu = input('\nPress <Enter> to return to main menu')
        if return_to_menu == '':
            return


    def search_users(self):

        run = True
        while run:

            search = input('\nEnter search name: ')
            rows = cursor.execute('SELECT * from Users WHERE first_name=? OR last_name=?', (search, search,)).fetchall()

            if rows == []:
                print(f'\nno searches found for: {search}')
                search_again = input('\nwould you like to search for something else? (press Y or to return to menu with ENTER)').upper()

                if search_again == '':
                    run = False

            else:
                print()
                print('first_name   last_name     phone_number   email                  date_created    hire_date     user_type')

                for row in rows:
                    print(
                        f'{row[1]:<10}   {row[2]:<10}    {row[3]}   {row[4]:<20}   {row[8]:<12}    {row[9]:<12}  {row[10]:<10}')


                search_again = input('\nwould you like to search for something else? (press <Y> or to return to menu with <ENTER>)\n').upper()

                if search_again == '':
                    run = False
                elif search_again != 'Y':
                    print('\nerror, command not found. returning to main menu')
                


    def view_user_comp(self):

        run = True
        while run:
            users = cursor.execute('SELECT person_id, first_name, last_name FROM Users').fetchall()
            print()
            for row in users:
                print(f'[{row[0]}] {row[1]} {row[2]}')

            user_id = int(input('\nChoose an option: ')) - 1

            rows = cursor.execute('SELECT c.name, cr.level, cr.report FROM Competency_results cr, Competencies c WHERE cr.comp_id=c.comp_id AND cr.person_id=?', (user_id + 1,)).fetchall()

            if rows == []:
                print('\nNo competency results found')
            else:
                print('\nCOMPETENCIES   SCORE  REPORT')
                for row in rows:
                    print(f'{row[0]:<15}{row[1]:<7}{row[2]} ')
            print()
            search_again = input('Press <Y> to view another persons competency list or press <ENTER> to return to main menu: ').upper()
            if search_again == '':
                run = False
            elif search_again != 'Y':
                print('\nerror, command not found. returning to main menu')


    def view_users_comp(self):
        
        run = True
        while run:

            comp_list = cursor.execute('SELECT comp_id, name FROM Competencies ORDER BY comp_id ASC').fetchall()
            print()
            for row in comp_list:
                print(f'[{row[0]}] {row[1]}')

            comp_id = int(input('\nenter competency number: ')) - 1
            print()
            print(f'COMPETENCY: {comp_list[int(comp_id)][1]}\n')

            rows = cursor.execute('SELECT u.first_name, u.last_name, cr.level, cr.report FROM Users u, competency_results cr, Competencies c WHERE cr.comp_id=? and u.person_id=cr.person_id GROUP BY u.person_id', (comp_id + 1,)).fetchall()

            if rows == []:
                print(f'No results for: {comp_list[int(comp_id)][1]}')
            else:
                print(f'first_name   last_name   score   report')
                for row in rows:
                    print(f'{row[0]:<12} {row[1]:<10}  {row[2]:<7} {row[3]}')
            
            search_again = input('\ntype <Y> to search again or <ENTER> for main menu:\n').upper()
            if search_again == '':
                run = False
            elif search_again != 'Y':
                print('\nerror, command not found. returning to main menu')


    def user_report(self):

        run = True
        while run:
            users = cursor.execute('SELECT person_id, first_name, last_name FROM Users').fetchall()
            print()
            for row in users:
                print(f'[{row[0]}] {row[1]} {row[2]}')

            user_id = int(input('\nPick a user: ')) - 1

            comp_list = cursor.execute('SELECT comp_id, name FROM Competencies ORDER BY comp_id ASC').fetchall()
            print()
            for row in comp_list:
                print(f'[{row[0]}] {row[1]}')

            comp_id = int(input('\nPick a competency:  ')) - 1

            row = cursor.execute('SELECT level, report  FROM competency_results WHERE person_id=? AND comp_id=?', (user_id + 1, comp_id + 1)).fetchall()

            find_average = cursor.execute('SELECT score FROM assessment_results WHERE person_id=?',(user_id + 1,)).fetchall()

            total = 0
            if find_average != []:
                for num in find_average:
                    total += num[0]
                
                average = total/len(find_average)

            if row == []:
                print('\nno reports found')
            else:
                print(f'\nCOMPETENCY: {comp_list[int(comp_id)][1]}')
                print(f'USER:       {users[int(user_id)][1]} {users[int(user_id)][2]}\n')
                print('Score  average    report')
                print(f'{row[0][0]:<7}{average:<10} {row[0][1]} ')

            print('\npress <Y> to search again, press <ENTER> to return to main menu')
            search_again = input().upper()

            if search_again == '':
                run = False
            elif search_again != 'Y':
                print('\nerror, command not found. returning to main menu')


    def assessment_list(self):

        run = True
        while run:

            users = cursor.execute('SELECT person_id, first_name, last_name FROM Users').fetchall()
            print()
            for row in users:
                print(f'[{row[0]}] {row[1]} {row[2]}')

            user_id = int(input('\nPick a user: ')) - 1
            print()

            rows = cursor.execute('SELECT a.name, ar.score, ar.feedback, ar.completed_date FROM Assessments a, assessment_results ar WHERE ar.person_id=? AND ar.assessment_id=a.assessment_id', (user_id + 1,)).fetchall()

            if rows == []:
                print('no assessments found')
            else:
                print('ASSESSMENT                  SCORE    COMPLETION DATE    FEEDBACK')
                for row in rows:
                    print(f'{row[0]:<28}{row[1]:<8} {row[3]:<18} {row[2]}')

            print('\npress <Y> to search again, press <ENTER> to return to main menu')
            search_again = input().upper()

            if search_again == '':
                run = False
            elif search_again != 'Y':
                print('\nerror, command not found. returning to main menu')


    def add_user(self):

        run = True
        while run:

            first_name = input('\nEnter first name: ')
            last_name = input('Enter last name: ')
            phone = input('Enter phone number: ')
            email = input('Enter email address: ')
            username = input('Enter username: ')
            password = 'password'.encode('utf-8')
            hire_date = input('enter hire date: ')
            user_type = input('enter user type ("Manager" or "User"): ')

            salt = b'$2b$12$hXV7K881YN/7dmizgNoyL.'
            hashed = bcrypt.hashpw(password, salt)

            insert_user = 'INSERT INTO Users (first_name, last_name, phone, email, username, password, date_created, hire_date, user_type) VALUES (?,?,?,?,?,?,?,?,?)'
            values = [first_name, last_name, phone, email, username, hashed, self.current_date, hire_date, user_type]

            cursor.execute(insert_user, values)

            connection.commit()
            print('\nUSER ADDED SUCCESSFULLY!')

            print('\npress <Y> to add another user or <ENTER> for the main menu')
            search_again = input().upper()
            if search_again == '':
                run = False
            elif search_again != 'Y':
                print('\nerror, command not found. returning to main menu')


    def add_competency(self):
        run = True
        while run:

            comp_name = input('\nEnter competency name: ')

            insert_comp = 'INSERT INTO Competencies (name, date_created) VALUES (?,?)'
            values = [comp_name, self.current_date]

            cursor.execute(insert_comp, values)

            connection.commit()

            print('\nCOMPETENCY ADDED SUCCESSFULLY!')

            print('\npress <Y> to add another competency or <ENTER> for the main menu')
            search_again = input().upper()
            if search_again == '':
                run = False
            elif search_again != 'Y':
                print('\nerror, command not found. returning to main menu')


    def add_assessment(self):
        run = True
        while run:
            name = input('\nEnter name of assessment: ')
            description = input('Enter a description: ')

            comp_list = cursor.execute('SELECT comp_id, name FROM Competencies ORDER BY comp_id ASC').fetchall()
            print()
            for row in comp_list:
                print(f'[{row[0]}] {row[1]}')

            comp_id = input('\nChoose a competency to relate it too: ')

            insert_assessment = 'INSERT INTO Assessments (name, description, comp_id) VALUES (?,?,?)'
            values = [name, description, comp_id]
            cursor.execute(insert_assessment, values)

            connection.commit()
            print('\nAssessment added SUCCESSFULLY!')

            print('\npress <Y> to add another assessment or <ENTER> for the main menu')
            search_again = input().upper()
            if search_again == '':
                run = False
            elif search_again != 'Y':
                print('\nerror, command not found. returning to main menu')


    def add_assessment_result(self):

        run = True
        while run:
            print()
            rows = cursor.execute('SELECT * FROM Assessments').fetchall()
            
            for row in rows:
                print(f'[{row[0]}] {row[1]:<25} {row[3]:<7} {row[2]:<7}')

            assessment_id = int(input('\nselect an option for assessment: ')) - 1

            rows = cursor.execute('SELECT person_id, first_name, last_name FROM Users').fetchall()

            for row in rows:
                print(f'{row[0]:<5} {row[1]:<12} {row[2]:<12}')

            person_id = int(input('\nchoose the user: ')) - 1

            score = input('Enter score for the assessment: ')

            feedback = input('give some feedback on the assessment: ')

            insert_assessment_score = 'INSERT INTO assessment_results (assessment_id, person_id, score,feedback,completed_date) values (?,?,?,?,?)'
            values = [assessment_id + 1, person_id + 1, score, feedback, self.current_date]

            cursor.execute(insert_assessment_score, values)

            connection.commit()

            print()
            print('Assessment result SUCCESSFULLY added!')
            print('\npress <Y> to add another assessment result or <ENTER> for the main menu')
            search_again = input().upper()
            
            if search_again == '':
                run = False
            elif search_again != 'Y':
                print('\nerror, command not found. returning to main menu')

    
    def add_competency_result(self):

        run = True
        while run:

            rows = cursor.execute('SELECT person_id, first_name, last_name FROM Users').fetchall()
            print()
            for row in rows:
                print(f'{row[0]:<5} {row[1]:<12} {row[2]:<12}')

            user = int(input('\nchoose a user: ')) - 1

            rows = cursor.execute('SELECT comp_id, name FROM Competencies ORDER BY comp_id').fetchall()
            print()
            for row in rows:
                print(f'[{row[0]}]   {row[1]}')

            comp = int(input('\npick a competency: ')) - 1

            level = input('\nEnter a level: ')

            report = input('\nGive a report on this competency result: ')

            insert_competency_result = 'INSERT INTO competency_results (comp_id, person_id, level, report) VALUES (?,?,?,?)'
            values = [comp + 1, user + 1, level, report]
            cursor.execute(insert_competency_result, values)
            connection.commit()

            print('\nCompetency result added SUCCESSFULLY!\n')

            print('press <Y> to add another competency result or <ENTER> for the main menu')
            search_again = input().upper()
            if search_again == '':
                run = False
            elif search_again != 'Y':
                print('\nerror, command not found. returning to main menu')


    def edit_user(self):
        print()
        users = cursor.execute('SELECT person_id, first_name, last_name FROM Users').fetchall()
        for row in users:
            print(f'[{row[0]}] {row[1]} {row[2]}')

        user_id = int(input('\npick user to update: ')) - 1
        run = True
        while run:
            print('''
What would you like to update:
[1] first name
[2] last name
[3] phone number
[4] email
[5] active
[6] date created
[7] hire_date
[8] user type
            ''')
            option = input('Select an option: ')

            if option == '1':
                first_name = input('Enter new first name: ')
                update_sql = 'UPDATE Users SET first_name=? WHERE person_id=?'
                update_values = (first_name, user_id + 1)
                cursor.execute(update_sql, update_values)
                connection.commit()
                print('UPDATE COMPLETE!')
            elif option == '2':
                last_name = input('Enter new last name: ')
                update_sql = 'UPDATE Users SET last_name=? WHERE person_id=?'
                update_values = (last_name, user_id + 1)
                cursor.execute(update_sql, update_values)
                connection.commit()
                print('UPDATE COMPLETE!')
            elif option == '3':
                phone = input('Enter new phone number ex: (801-123-2345): ')
                update_sql = 'UPDATE Users SET phone=? WHERE person_id=?'
                update_values = (phone, user_id + 1)
                cursor.execute(update_sql, update_values)
                connection.commit()
                print('UPDATE COMPLETE!')
            elif option == '4':
                email = input('Enter new email: ')
                update_sql = 'UPDATE Users SET email=? WHERE person_id=?'
                update_values = (email, user_id + 1)
                cursor.execute(update_sql, update_values)
                connection.commit()
                print('UPDATE COMPLETE!')
            elif option == '5':
                active = int(input('[0] for inactive [1] for active'))
                update_sql = 'UPDATE Users SET active=? WHERE person_id=?'
                update_values = (active, user_id + 1)
                cursor.execute(update_sql, update_values)
                connection.commit()
                print('UPDATE COMPLETE!')
            elif option == '6':
                date_created = input('Enter new date (mm-dd-yyyy)')
                update_sql = 'UPDATE Users SET date_created=? WHERE person_id=?'
                update_values = (date_created, user_id)
                cursor.execute(update_sql, update_values)
                connection.commit()
                print('UPDATE COMPLETE!')
            elif option == '7':
                hire_date = input('Enter new date (mm-dd-yyyy)')
                update_sql = 'UPDATE Users SET hire_date=? WHERE person_id=?'
                update_values = (hire_date, user_id + 1)
                cursor.execute(update_sql, update_values)
                connection.commit()
                print('UPDATE COMPLETE!')
            elif option == '7':
                user_type = input('type Manager or User: ')
                update_sql = 'UPDATE Users SET user_type=? WHERE person_id=?'
                update_values = (user_type, user_id + 1)
                cursor.execute(update_sql, update_values)
                connection.commit()
                print('UPDATE COMPLETE!')

            continue_updating = input('\nWould you like to update something else? (type Y for Yes, N for No)').upper()
            if continue_updating == 'N':
                run = False
            elif continue_updating != 'Y':
                print('\nerror, command not found. returning to main menu')

    def edit_competency(self):

        run = True
        while run:

            comp_list = cursor.execute('SELECT comp_id, name FROM Competencies ORDER BY comp_id ASC').fetchall()
            print()
            for row in comp_list:
                print(f'[{row[0]}] {row[1]}')

            comp_id = int(input('\nChoose competency to update: ')) - 1

        
            print('''
[1] name
[2] date_created
            ''')
            option = input('pick option to update: ')

            if option == '1':
                name = input('Enter new competency name: ')
                update_sql = 'UPDATE Competencies SET name=? WHERE comp_id=?'
                update_values = (name, comp_id + 1)
                cursor.execute(update_sql, update_values)
                connection.commit()
                print('\nUPDATE SUCCESSFUL!')
            elif option == '2':
                date_created = input('Enter new competency name: ')
                update_sql = 'UPDATE Competencies SET date_created=? WHERE comp_id=?'
                update_values = (date_created, comp_id + 1)
                cursor.execute(update_sql, update_values)
                connection.commit()
                print('\nUPDATE SUCCESSFUL!')

            continue_updating = input('\nWould you like to update something else? (type Y for Yes, N for No)').upper()
            if continue_updating == 'N':
                run = False
            elif continue_updating != 'Y':
                print('\nerror, command not found. returning to main menu')

    def edit_assessment(self):

        run = True
        while run:
            print()
            assessment_list = cursor.execute('SELECT assessment_id, name, description, comp_id FROM Assessments').fetchall()
            print('    Name                      competency-relation  description')
            for row in assessment_list:
                print(f'[{row[0]}] {row[1]:<25} {row[3]:<20} {row[2]}')

            assessment_id = int(input('\nchoose assessment to update: ')) - 1

            print('''
[1] name
[2] competency relation
[3] description            
            ''')
            option = input('what would you like to update: ')
            if option == '1':
                name = input('Enter new name: ')
                update_sql = 'UPDATE Assessments SET name = ? WHERE assessment_id = ?'
                update_values = (name, assessment_id + 1)
                cursor.execute(update_sql, update_values)
                connection.commit()
                print('\nUPDATE SUCCESSFUL!')
            elif option == '2':
                competency_relation = input('Enter competency id: ')
                update_sql = 'UPDATE Assessments SET comp_id = ? WHERE assessment_id = ?'
                update_values = (competency_relation, assessment_id + 1)
                cursor.execute(update_sql, update_values)
                connection.commit()
                print('\nUPDATE SUCCESSFUL!')
            elif option == '3':
                description = input('Enter description: ')
                update_sql = 'UPDATE Assessments SET description = ? WHERE assessment_id = ?'
                update_values = (description, assessment_id + 1)
                cursor.execute(update_sql, update_values)
                connection.commit()
                print('\nUPDATE SUCCESSFUL!')
            continue_updating = input('\nWould you like to update something else? (type Y for Yes, N for No)').upper()
            if continue_updating == 'N':
                run = False
            elif continue_updating != 'Y':
                print('\nerror, command not found. returning to main menu')
            

    def edit_assessment_result(self):

        run = True
        while run:

            assessment_result_list = cursor.execute('SELECT * FROM assessment_results').fetchall()
            print()
            print('     Assessment_id   user_id      score    completion_date    feedback')
            for row in assessment_result_list:
                print(f'[{row[0]}]  {row[1]:<15} {row[2]:<12} {row[3]:<8} {row[5]:<18} {row[4]}')

            assess_result_id = int(input('\nChoose assessment result to edit: ')) - 1

            print('''
    [1] assessment id
    [2] score
    [3] feedback
    [4] completed date
            ''')
            option = input()
            if option == '1':
                assessment_id = input('enter a new assessment_id: ')
                update_sql = 'UPDATE assessment_results SET assessment_id=? WHERE asess_result_id=?'
                update_values = (assessment_id, assess_result_id + 1)
                cursor.execute(update_sql, update_values)
                connection.commit()
                print('\nUPDATE SUCCESSFUL!')
            elif option == '2':
                score = input('enter a new score: ')
                update_sql = 'UPDATE assessment_results SET score=? WHERE asess_result_id=?'
                update_values = (score, assess_result_id + 1)
                cursor.execute(update_sql, update_values)
                connection.commit()
                print('\nUPDATE SUCCESSFUL!')
            elif option == '3':
                feedback = input('enter new feedback: ')
                update_sql = 'UPDATE assessment_results SET feedback=? WHERE asess_result_id=?'
                update_values = (feedback, assess_result_id + 1)
                cursor.execute(update_sql, update_values)
                connection.commit()
                print('\nUPDATE SUCCESSFUL!')
            elif option == '4':
                completed_date = input('enter new completion date: ')
                update_sql = 'UPDATE assessment_results SET completed_date=? WHERE asess_result_id=?'
                update_values = (completed_date, assess_result_id + 1)
                cursor.execute(update_sql, update_values)
                connection.commit()
                print('\nUPDATE SUCCESSFUL!')

            continue_updating = input('\nWould you like to update something else? (type Y for Yes, N for No)').upper()
            if continue_updating == 'N':
                run = False
            elif continue_updating != 'Y':
                print('\nerror, command not found. returning to main menu')
            

    def delete_assessment_result(self):
        run = True
        while run:

            assessment_result_list = cursor.execute('SELECT * FROM assessment_results').fetchall()

            print('     Assessment_id   user_id      score    completion_date    feedback')
            for row in assessment_result_list:
                print(f'[{row[0]}]  {row[1]:<15} {row[2]:<12} {row[3]:<8} {row[5]:<18} {row[4]}')

            assess_result_id = int(input('Choose assessment result to delete: '))
            delete_assess_result = 'DELETE FROM assessment_results WHERE asess_result_id=?'
            cursor.execute(delete_assess_result, str(assess_result_id))
            connection.commit()

            print('\n assessment result DELETED\n')
            print('press <Y> to delete another assessment result, press <ENTER> to return to main menu')

            continue_delete = input().upper()
            
            if continue_delete == '':
                run = False
            elif continue_delete != 'Y':
                print('\nerror, command not found. returning to main menu')
    

    def export_comp_report(self):

        fields = ['first_name', 'last_name', 'user_id', 'comp_id', 'comp_name' 'level', 'report']
        rows = []

        comp_list = cursor.execute('SELECT comp_id, name FROM Competencies ORDER BY comp_id ASC').fetchall()
        print()
        for row in comp_list:
            print(f'[{row[0]}] {row[1]}')

        competency = int(input('\nchoose a competency: '))

        user_list = cursor.execute('SELECT person_id, first_name, last_name FROM Users').fetchall()
        print()
        for row in user_list:
            print(f'[{row[0]}] {row[1]} {row[2]} ') 

        users = input('choose your users (if multiple after each user number add a space ex: 1 3 5): ')

        user_list = users.split()
        for user in user_list:
            data = cursor.execute('SELECT u.first_name, u.last_name, cr.person_id, cr.comp_id, c.name, cr.level, cr.report FROM Users u, Competencies c JOIN competency_results cr ON cr.person_id=u.person_id WHERE cr.comp_id=? AND cr.person_id=? GROUP BY u.person_id', (competency, user,)).fetchone()
            rows.append(data)

        with open('comp_reports.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(fields)
            for row in rows:
                csv_writer.writerow(row)
        print('\nEXPORTED SUCCESSFULLY!')

    def export_single_user_comp(self):
        fields = ['competency name', 'level', 'report']

        users_list = cursor.execute('SELECT person_id, first_name, last_name FROM Users').fetchall()
        print()
        for row in users_list:
            print(f'[{row[0]}] {row[1]} {row[2]}')
        print()
        user_id = int(input('choose a user to export competencies: ')) - 1

        assessment_result_list = cursor.execute('SELECT c.name, cr.level, cr.report FROM Competencies c, competency_results cr WHERE person_id=? AND c.comp_id=cr.comp_id',(user_id+1,)).fetchall()

        with open('comp_report.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(fields)
            for row in assessment_result_list:
                csv_writer.writerow(row)
            print('\nEXPORTED SUCCESSFULLY!')
    
    def import_csv_assessments(self):

        with open('assessment_result.csv', 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                insert_sql = 'INSERT INTO assessment_results (assessment_id,person_id,score,feedback,completed_date) VALUES (?,?,?,?,?)'
                cursor.execute(insert_sql,row)
                connection.commit()
        print('\nFILE IMPORTED SUCCESSFULLY!')
