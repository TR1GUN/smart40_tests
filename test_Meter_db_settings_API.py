# Здесь расположены все тесты к test_Meter_db_settings_API которые запускаются через Pytest
import pytest

from working_directory import Meter_db_settings_API
from working_directory.sqlite import deleteMeterTable
from time import sleep

@pytest.mark.parametrize("generate, delete",[(11, 0), (11, 11), (20, 10), (10, 1)])
def test_delete_MeterTable(type_connect,generate, delete):
    """
    Тестовая функция для команды delete к таблице MeterTable
    """
    sleep(1)
    MeterTable = Meter_db_settings_API.DELETE(type_connect=type_connect).MeterTable(count_settings_generate=generate, count_settings_delete=delete)
    assert MeterTable == []


@pytest.mark.parametrize("settings", [11, 22, 1, 47])
def test_post_MeterTable(type_connect,settings):
    """
    Тестовая функция для команды post к таблице MeterTable
    """
    deleteMeterTable()
    sleep(1)
    MeterTable = Meter_db_settings_API.POST(type_connect=type_connect).MeterTable(count_settings=settings)
    assert MeterTable == []


@pytest.mark.parametrize("settings", [1, 2, 59, 23, 33])
def test_put_ArchInfo(type_connect,settings):
    """
    Тестовая функция для команды put к таблице ArchInfo
    """
    sleep(1)
    ArchInfo = Meter_db_settings_API.PUT(type_connect=type_connect).ArchInfo(count_settings=settings)
    assert ArchInfo == []


def test_get_MeterTypes(type_connect):
    """
    Тестовая функция для команды get к таблице MeterTypes
    """
    sleep(1)
    MeterTypes = Meter_db_settings_API.GET(type_connect=type_connect).MeterTypes()
    assert MeterTypes == []


def test_get_ArchInfo(type_connect):
    """
    Тестовая функция для команды get к таблице ArchInfo
    """
    sleep(1)
    ArchInfo = Meter_db_settings_API.GET(type_connect=type_connect).ArchInfo()
    assert ArchInfo == []


def test_get_MeterIfaces(type_connect):
    """
    Тестовая функция для команды get к таблице MeterIfaces
    """
    sleep(1)
    MeterIfaces = Meter_db_settings_API.GET(type_connect=type_connect).MeterIfaces()
    assert MeterIfaces == []


def test_get_ArchTypes(type_connect):
    """
    Тестовая функция для команды get к таблице ArchTypes
    """
    sleep(1)
    ArchTypes = Meter_db_settings_API.GET(type_connect=type_connect).ArchTypes()
    assert ArchTypes == []

@pytest.mark.parametrize("generate_ids, get_ids", [(22, 0), (11, 11), (1, 1), (10, 5)])
def test_get_MeterTable(type_connect,generate_ids, get_ids):
    """
    Тестовая функция для команды get к таблице MeterTable
    """
    deleteMeterTable()
    sleep(1)
    MeterTable = Meter_db_settings_API.GET(type_connect=type_connect).MeterTable(count_get_ids= get_ids, count_generate_ids=generate_ids)
    assert MeterTable == []

