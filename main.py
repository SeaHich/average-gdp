import csv
import tabulate
import argparse

parser = argparse.ArgumentParser(description='Получить срединй ВВП')
parser.add_argument(
    '-f',
    '--files',
    type=str,
    default='economic1.csv',
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


def get_raw_data(file_names):

    raw_country_data = {}
    for file_name in file_names:

        with open(file_name, mode='r', newline='') as csv_file:
            csv_data = csv.DictReader(csv_file)

            for row in csv_data:
                country_name = row['country']
                gdp = int(row['gdp'])

                if country_name in raw_country_data:
                    raw_country_data[country_name]['gdp'].append(gdp)
                else:
                    raw_country_data[country_name] = {'gdp': [gdp]}

    return raw_country_data


def create_report(table_data):
    fieldnames = ['country', 'gdp']
    with open(namespace.report, mode='w', newline='') as csv_file:
        report = csv.DictWriter(csv_file, fieldnames=fieldnames)
        report.writeheader()
        report.writerows(table_data)


def report_output(table_data):
    print(
        tabulate.tabulate(
            table_data, headers='keys', tablefmt='grid',
            stralign='center', showindex=range(1, len(table_data)+1)
        )
    )


def main():

    file_names = namespace.files.split(',')
    raw_country_data = get_raw_data(file_names)

    country_data = {}
    for country_name in raw_country_data:
        gdp = raw_country_data[country_name]['gdp']
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

    create_report(table_data)
    report_output(table_data)



main()