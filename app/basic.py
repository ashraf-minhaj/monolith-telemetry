""" basic steps for a salary disbursement system

author: ashraf minhaj
mail  : ashraf_minhaj@yahoo.com
"""


def send_salary():
    print("Salary Sending steps initialized")
    employee_data = get_employee_data()
    to_disburse = determine_salary(current_salary=employee_data['salary'], id=employee_data['id'])
    print(to_disburse)
    send_to_bank(to_disburse)
    

def get_employee_data():
    data = { 
        'id': 7,
        'salary': 20,
        'last_note': 'you will miss me when I am gone'
            }
    return data

def determine_salary(current_salary, id):
    salary = current_salary
    salary += add_bonus(id=7)
    salary -= deduct_loan(id=7)
    
    return salary

def add_bonus(id):
    if id == 7:
        print('adding bonus')
        return 10
    return 1

def deduct_loan(id):
    to_deduct = 0

    if id == 7:
        to_deduct = 10
        print('deducting loan')
        return to_deduct
    return to_deduct

def send_to_bank(to_disburse):
    print(f'disbursing salary {to_disburse} Taka')


if __name__ == '__main__':
    send_salary()