import pytest
from os import remove, path
from contextlib import nullcontext as does_not_raise

from main import *


test_file_name = 'tests/economic1.csv'


@pytest.fixture(scope='session')
def raw_country_data():
    return get_raw_data([test_file_name])


@pytest.fixture(scope='session')
def table_data(raw_country_data):
    return create_report_avg_gdp(raw_country_data)


def country_and_year():
    country_and_year = []
    with open(test_file_name, mode='r', newline='') as csv_file:
        csv_data = DictReader(csv_file)
        for row in csv_data:
            country_name = row['country']
            year = int(row['year'])
            country_and_year.append((country_name, year))
    return country_and_year


@pytest.mark.parametrize(
    'file_name, expectation',
    [
        ('tests/economic1.cs', pytest.raises(TypeError)),
        (test_file_name, does_not_raise()),
    ]
)
def test_check_file_extension(file_name, expectation):
    with expectation:
        assert (
            check_file_extension(file_name) is None
        )


def test_get_raw_data(raw_country_data):
    assert type(raw_country_data) is dict


country_and_year_value = country_and_year()


@pytest.mark.parametrize(
        'country, year',
        country_and_year_value
)
def test_get_raw_data_country_and_year_key(
    raw_country_data, country, year
):
    assert (
       (country in raw_country_data and year in raw_country_data[country])
    ), f'Отсутствует один из обязательных ключей - {country}, {year}'


@pytest.mark.parametrize(
        'key',
        [
            'gdp',
            'gdp_growth',
            'inflation',
            'unemployment',
            'population',
            'continent'
        ]
)
def test_get_raw_data_key(raw_country_data, key):
    result = True
    for country, year in country_and_year_value:
        if key not in raw_country_data[country][year]:
            result = False
            break
    assert result, f'Отсутствует один из обязательных ключей - {key}'


def test_create_report_avg_gdp(table_data):
    assert (
        type(table_data) is list
    ), 'Неверный тип возвращаемых данных'


@pytest.mark.parametrize(
        'key',
        [
           'country',
           'gdp'
        ]
)
def test_create_report_avg_gdp_key(table_data, key):
    result = True
    for i in table_data:
        if key not in i:
            result = False
    assert result, f'Нет обязательного ключа - {key}'


def test_create_report_file_avg_gdp(table_data):
    remove('average-gdp.csv')
    create_report_file(table_data)
    assert path.exists('average-gdp.csv')
