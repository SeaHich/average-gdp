from csv import DictWriter, DictReader
import tabulate
from argparse import ArgumentParser
from os import path

parser = ArgumentParser(description='Получить средний ВВП')
parser.add_argument(
    '-f',
    '--files',
    type=str,
    default='economic2.csv',
    help='Путь или имя файла с данными'
)
parser.add_argument(
    '-r',
    '--report',
    default='average-gdp.csv',
    type=str,
    help='Имя отчёта'
)

namespace = parser.parse_args()

CORRECT_REPORT_NAMES = (
    'average-gdp.csv',
    'something_inflation'
    )


def check_report_name():
    if namespace.report not in CORRECT_REPORT_NAMES:
        raise TypeError(f'Неверное имя отчёта {namespace.report}')


def check_file_extension(*agrs):
    for file_name in agrs:
        _, ext = path.splitext(file_name)
        if ext != '.csv':
            raise TypeError(f'Неверное расширение файла {file_name}')


def get_raw_data(file_names):

    raw_country_data = {}
    for file_name in file_names:

        with open(file_name, mode='r', newline='') as csv_file:
            csv_data = DictReader(csv_file)

            for row in csv_data:

                country_name = row['country']

                if country_name not in raw_country_data:
                    raw_country_data[country_name] = {}

                raw_country_data[country_name][int(row['year'])] = {
                    'gdp': float(row['gdp']),
                    'gdp_growth': float(row['gdp_growth']),
                    'inflation': float(row['inflation']),
                    'unemployment': float(row['unemployment']),
                    'population': float(row['population']),
                    'continent': row['continent']
                }

    return raw_country_data


def create_report_file(table_data):
    one_data = table_data[0]
    fieldnames = [key for key in one_data]
    with open(namespace.report, mode='w', newline='') as csv_file:
        report = DictWriter(csv_file, fieldnames=fieldnames)
        report.writeheader()
        report.writerows(table_data)


def report_output(table_data):
    print(
        tabulate.tabulate(
            table_data, headers='keys', tablefmt='grid',
            stralign='center', showindex=range(1, len(table_data)+1)
        )
    )


def create_report_avg_gdp(raw_country_data):

    country_data = {}
    for country_name in raw_country_data:
        gdp = []
        for year in raw_country_data[country_name]:
            gdp.append(raw_country_data[country_name][year]['gdp'])
        country_data[f'{country_name}'] = round(sum(gdp) / len(gdp), 2)

    sorted_gdp = sorted(
        country_data.items(), key=lambda item: item[1], reverse=True
    )
    table_data = []

    for sg in sorted_gdp:
        table_data.append(
            {'country': sg[0],
                'gdp': sg[1]}
            )
    return table_data


def create_something_inflation(raw_country_data):
    """Будующий отчёт"""
    pass


def main():

    check_report_name()
    file_names = namespace.files.split(',')
    check_file_extension(namespace.report, *file_names)
    raw_country_data = get_raw_data(file_names)

    if namespace.report == 'average-gdp.csv':
        table_data = create_report_avg_gdp(raw_country_data)
    elif namespace.report == 'something_inflation':
        table_data = create_something_inflation(raw_country_data)
    else:
        raise TypeError('Некорректное имя отчёта')

    create_report_file(table_data)
    report_output(table_data)


if __name__ == '__main__':
    main()
