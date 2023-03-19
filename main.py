from collections import defaultdict
from datetime import datetime, timedelta
import re


def get_next_week_start(d: datetime):
    diff_days = 7 - d.weekday()
    return d + timedelta(days=diff_days)

def prepare_date(text: str):
    bsd = datetime.strptime(text, '%d.%m.%Y')
    return bsd.replace(year=datetime.now().year).date()



def get_birthdays_per_week(employees):
    employees_list = []
    birthdays = defaultdict(list)

    with open('colleagues.txt', 'r') as fd:
        line = fd.readline()
        while line:

            k = re.search(r'^\w+', line).group()
            v = re.search(r'\d[0-9.]+', line).group()
            employees_list.append({'name': k, 'birthday': v})
            line = fd.readline()


    today = datetime.now().date()

    n_w_s = get_next_week_start(today)
    start_period = n_w_s - timedelta(2)
    end_period = n_w_s + timedelta(4)

    b_days = [user for user in employees_list if start_period <= prepare_date(user['birthday']) <= end_period]

    for user in b_days:
        current_bd = prepare_date(user['birthday'])
        if current_bd.weekday() in (5,6):
            birthdays['Monday'].append(user['name'])
        else:
            birthdays[current_bd.strftime('%A')].append(user['name'])

    with open('celebrate.txt', 'w') as fd:

        for k, v in birthdays.items():
            fd.write(f'{k}: ')

            for i in v:
                if not v[-1] == i:
                    fd.write(f'{i}, ')
                else:
                    fd.write(f'{i}\n')
    



if __name__ == '__main__':

    get_birthdays_per_week('colleagues.txt')








