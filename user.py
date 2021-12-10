import datetime
import sqlite3
import bcrypt

connection = sqlite3.connect('competency_tracker.db')
cursor = connection.cursor()

class User:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.current_date = datetime.date.today().strftime('%m-%d-%Y')
        self.user_id = cursor.execute('SELECT person_id FROM Users WHERE username = ?', (self.username,)).fetchone()

    def check_credentials(self):

        rows = cursor.execute('SELECT username, password FROM Users').fetchall()

        for row in rows:
            print(type(row[1]))
            if self.username == row[0] and self.password == row[1]:
                return True
        return False

    def change_credentials(self):

        run = True
        while run:
            print('''
what would you like to change:
[1] firstname
[2] lastname
[3] username
[4] password
    ''')
            option = input()

            if option == '1':
                first_name = input('Enter new first name: ')
                update_sql = 'UPDATE Users SET first_name = ? WHERE username = ?'
                update_values = (first_name, self.username)
                cursor.execute(update_sql, update_values)
                connection.commit()
            elif option == '2':
                last_name = input('Enter new last name: ')
                update_sql = 'UPDATE Users SET last_name = ? WHERE username = ?'
                update_values = (last_name, self.username)
                cursor.execute(update_sql, update_values)
                connection.commit()
            elif option == '3':
                username = input('Enter new username: ')
                update_sql = 'UPDATE Users SET username = ? WHERE username = ?'
                update_values = (username, self.username)
                cursor.execute(update_sql, update_values)
                connection.commit()
                self.username = username
            elif option == '4':
                password = input('Enter new password:').encode('utf-8')
                salt = b'$2b$12$hXV7K881YN/7dmizgNoyL.'
                hashed = bcrypt.hashpw(password, salt)
                update_sql = 'UPDATE Users SET password = ? WHERE username = ?'
                update_values = (hashed, self.username)
                cursor.execute(update_sql, update_values)
                connection.commit()
            continue_updating = input(
                '\nWould you like to update something else? (type Y for Yes, N for No)').upper()
            print(continue_updating)
            if continue_updating == 'N':
                run = False