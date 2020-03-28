import credentials
import mysql.connector

connection = mysql.connector.connect(host=credentials.database_host_ip,
                                     database=credentials.database_name,
                                     user=credentials.database_username,
                                     password=credentials.database_password,
                                     autocommit=True)
cursor = connection.cursor()


def insert_new_data_to_table(date, name, department, role, manager):
    converted_data = '.'.join(date.split('.')[::-1])
    sql_query = 'INSERT INTO new_employees(date, name, department , role, manager) ' \
                'VALUES("{}","{}","{}","{}","{}")'.format(converted_data, name, department, role, manager)
    cursor.execute(sql_query)


def get_data_from_table():
    sql_query = 'SELECT DISTINCT date, name, department, role, manager FROM new_employees ORDER BY date;'
    cursor.execute(sql_query)
    result = cursor.fetchall()
    return result


def get_date_of_new_employees(date_now):
    sql_query = 'SELECT DISTINCT date, name, department, role, manager FROM new_employees ' \
                'WHERE date>=("{}") ORDER BY date;'.format(date_now)
    cursor.execute(sql_query)
    result = cursor.fetchall()
    return result

