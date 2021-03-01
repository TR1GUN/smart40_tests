from working_directory.Meter_db_data_API import POST, GET
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes
from working_directory.sqlite import deleteMeterTable
from time import sleep
import pytest
# Загружаем тестовые данные
import write_file

# Итак здесь расположим наши тестовые вызовы

ElectricConfig_ArchType_name_list = Template_list_ArchTypes.ElectricConfig_ArchType_name_list
PulseConfig_ArchType_name_list = Template_list_ArchTypes.PulseConfig_ArchType_name_list
DigitalConfig_ArchType_name_list = Template_list_ArchTypes.DigitalConfig_ArchType_name_list
ElecticEnergyValues_ArchType_name_list = Template_list_ArchTypes.ElecticEnergyValues_ArchType_name_list
ElectricQualityValues_ArchType_name_list = Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list
ElectricPowerValues_ArchType_name_list = Template_list_ArchTypes.ElectricPowerValues_ArchType_name_list
PulseValues_ArchType_name_list = Template_list_ArchTypes.PulseValues_ArchType_name_list
DigitalValues_ArchType_name_list = Template_list_ArchTypes.DigitalValues_ArchType_name_list
JournalValues_ArchType_name_list = Template_list_ArchTypes.JournalValues_ArchType_name_list


# ---------------------------------------------------------------------------------------------------------------------
#                                                  ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ---------------------------------------------------------------------------------------------------------------------

def parametrize_by_element(reqest: str, ArchType_name_list: list):
    parametrize_list = []
    # Если у нас гет запрос
    if reqest == 'post':
        template_parametrize = [
            [1, 1, True, True],
            [2, 3, True, True],
            [3, 1, True, True],
            [1, 1, False, False],
            [2, 3, False, False],
            [3, 1, False, False]
        ]
    if reqest == 'get':
        template_parametrize = [
            [0, 1, 1, 2, 0, True, False, False, False, False, False],
            [1, 2, 2, 3, 1, False, True, False, False, False, False],
            [2, 3, 3, 4, 2, False, False, True, False, False, False],
            [4, 4, 4, 5, 3, False, False, False, True, False, False],
            [0, 5, 1, 6, 4, False, False, False, True, False, True],
            [1, 4, 2, 5, 3, False, False, True, False, False, True],
            [2, 5, 3, 6, 2, False, True, False, False, False, True],
            [4, 4, 4, 5, 1, True, False, False, False, False, True],
            [2, 3, 3, 4, 0, True, False, False, False, True, False],
            [2, 2, 3, 3, 0, False, True, False, False, True, True]
        ]
    for i in range(len(ArchType_name_list)):
        ArchType_name = [ArchType_name_list[i]]
        for x in range(len(template_parametrize)):
            element = tuple([ArchType_name] + template_parametrize[x])
            parametrize_list.append(element)
    return parametrize_list


# # итак - начнем прикручивать pytest - для начала - чистим БД
#
# @pytest.fixture(scope='function', autouse=True)
# def delete_metertable():
#     from working_directory.sqlite import execute_command_to_write_return_dict
#     result = execute_command_to_write_return_dict(command='delete from MeterTable ')
#     return result


# import tracemalloc
#
# tracemalloc.start()


# def test_delete_metertable(delete_metertable):
#
#     result = delete_metertable()
#     assert result == []
# ---------------------------------------------------------------------------------------------------------------------
#                                                  POST
# ---------------------------------------------------------------------------------------------------------------------
# list_measure - Список из Тэгов
# count_id - Количество айдишников
# count_ts колличество времени
# generate_unicale_id - сгенерировать уникальные айдишник
# generate_unicale_ts - Сгенерирвоать уникальный таймштамп

# ------------------------------------- ElectricConfig -----------------------------------------------------------------
@pytest.mark.parametrize("list_measure, count_id, count_ts, generate_unicale_id, generate_unicale_ts",
                         [
                             (ElectricConfig_ArchType_name_list, 1, 1, True, True),
                             (ElectricConfig_ArchType_name_list, 2, 3, True, True),
                             (ElectricConfig_ArchType_name_list, 3, 1, True, True),
                             (ElectricConfig_ArchType_name_list, 1, 1, False, False),
                             (ElectricConfig_ArchType_name_list, 2, 3, False, False),
                             (ElectricConfig_ArchType_name_list, 3, 1, False, False)
                         ])
def test_POST_ElectricConfig_meterdata_db(type_connect,
                                          list_measure,
                                          count_id,
                                          count_ts,
                                          generate_unicale_id,
                                          generate_unicale_ts):
    sleep(1)
    meterdata = POST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                count_id=count_id,
                                                                count_ts=count_ts,
                                                                generate_unicale_id=generate_unicale_id,
                                                                generate_unicale_ts=generate_unicale_ts)

    assert meterdata == []


# ------------------------------------- PulseConfig -----------------------------------------------------------------
@pytest.mark.parametrize("list_measure, count_id, count_ts, generate_unicale_id, generate_unicale_ts",
                         [
                             (PulseConfig_ArchType_name_list, 1, 1, True, True),
                             (PulseConfig_ArchType_name_list, 2, 3, True, True),
                             (PulseConfig_ArchType_name_list, 3, 1, True, True),
                             (PulseConfig_ArchType_name_list, 1, 1, False, False),
                             (PulseConfig_ArchType_name_list, 2, 3, False, False),
                             (PulseConfig_ArchType_name_list, 3, 1, False, False)
                         ])
def test_POST_PulseConfig_meterdata_db(type_connect,
                                       list_measure,
                                       count_id,
                                       count_ts,
                                       generate_unicale_id,
                                       generate_unicale_ts):
    sleep(1)
    meterdata = POST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                count_id=count_id,
                                                                count_ts=count_ts,
                                                                generate_unicale_id=generate_unicale_id,
                                                                generate_unicale_ts=generate_unicale_ts)

    assert meterdata == []


# -------------------------------------DigitalConfig -----------------------------------------------------------------
@pytest.mark.parametrize("list_measure, count_id, count_ts, generate_unicale_id, generate_unicale_ts",
                         [
                             (DigitalConfig_ArchType_name_list, 1, 1, True, True),
                             (DigitalConfig_ArchType_name_list, 2, 3, True, True),
                             (DigitalConfig_ArchType_name_list, 3, 1, True, True),
                             (DigitalConfig_ArchType_name_list, 1, 1, False, False),
                             (DigitalConfig_ArchType_name_list, 2, 3, False, False),
                             (DigitalConfig_ArchType_name_list, 3, 1, False, False)
                         ])
def test_POST_DigitalConfig_meterdata_db(type_connect, list_measure,
                                         count_id,
                                         count_ts,
                                         generate_unicale_id,
                                         generate_unicale_ts):
    sleep(1)
    meterdata = POST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                count_id=count_id,
                                                                count_ts=count_ts,
                                                                generate_unicale_id=generate_unicale_id,
                                                                generate_unicale_ts=generate_unicale_ts)

    assert meterdata == []


# ------------------------------------- ElecticEnergyValues ----------------------------------------------------------
parametrize_ElecticEnergyValues_ArchType_name_list = parametrize_by_element(reqest='post',
                                                                            ArchType_name_list=ElecticEnergyValues_ArchType_name_list)


@pytest.mark.parametrize("list_measure, count_id, count_ts, generate_unicale_id, generate_unicale_ts",
                         parametrize_ElecticEnergyValues_ArchType_name_list)
def test_POST_ElecticEnergyValues_meterdata_db_by_element(type_connect, list_measure,
                                                          count_id,
                                                          count_ts,
                                                          generate_unicale_id,
                                                          generate_unicale_ts):
    sleep(1)
    meterdata = POST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                count_id=count_id,
                                                                count_ts=count_ts,
                                                                generate_unicale_id=generate_unicale_id,
                                                                generate_unicale_ts=generate_unicale_ts)

    assert meterdata == []


@pytest.mark.parametrize("list_measure, count_id, count_ts, generate_unicale_id, generate_unicale_ts",
                         [
                             (ElecticEnergyValues_ArchType_name_list, 1, 1, True, True),
                             (ElecticEnergyValues_ArchType_name_list, 2, 3, True, True),
                             (ElecticEnergyValues_ArchType_name_list, 3, 1, True, True),
                             (ElecticEnergyValues_ArchType_name_list, 1, 1, False, False),
                             (ElecticEnergyValues_ArchType_name_list, 2, 3, False, False),
                             (ElecticEnergyValues_ArchType_name_list, 3, 1, False, False)
                         ])
def test_POST_ElecticEnergyValues_meterdata_db(type_connect, list_measure,
                                               count_id,
                                               count_ts,
                                               generate_unicale_id,
                                               generate_unicale_ts):
    sleep(1)
    meterdata = POST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                count_id=count_id,
                                                                count_ts=count_ts,
                                                                generate_unicale_id=generate_unicale_id,
                                                                generate_unicale_ts=generate_unicale_ts)

    assert meterdata == []


# ------------------------------------- ElectricQualityValues ---------------------------------------------------------
@pytest.mark.parametrize("list_measure, count_id, count_ts, generate_unicale_id, generate_unicale_ts",
                         [
                             (ElectricQualityValues_ArchType_name_list, 1, 1, True, True),
                             (ElectricQualityValues_ArchType_name_list, 2, 3, True, True),
                             (ElectricQualityValues_ArchType_name_list, 3, 1, True, True),
                             (ElectricQualityValues_ArchType_name_list, 1, 1, False, False),
                             (ElectricQualityValues_ArchType_name_list, 2, 3, False, False),
                             (ElectricQualityValues_ArchType_name_list, 3, 1, False, False)
                         ])
def test_POST_ElectricQualityValues_meterdata_db(type_connect, list_measure,
                                                 count_id,
                                                 count_ts,
                                                 generate_unicale_id,
                                                 generate_unicale_ts):
    sleep(1)
    meterdata = POST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                count_id=count_id,
                                                                count_ts=count_ts,
                                                                generate_unicale_id=generate_unicale_id,
                                                                generate_unicale_ts=generate_unicale_ts)

    assert meterdata == []


# ------------------------------------- ElectricPowerValues -----------------------------------------------------------
parametrize_ElectricPowerValues_ArchType_name_list = parametrize_by_element(reqest='post',
                                                                            ArchType_name_list=ElectricPowerValues_ArchType_name_list)


@pytest.mark.parametrize("list_measure, count_id, count_ts, generate_unicale_id, generate_unicale_ts",
                         parametrize_ElectricPowerValues_ArchType_name_list)
def test_POST_ElectricPowerValues_meterdata_db_by_element(type_connect,
                                                          list_measure,
                                                          count_id,
                                                          count_ts,
                                                          generate_unicale_id,
                                                          generate_unicale_ts):
    sleep(1)
    meterdata = POST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                count_id=count_id,
                                                                count_ts=count_ts,
                                                                generate_unicale_id=generate_unicale_id,
                                                                generate_unicale_ts=generate_unicale_ts)

    assert meterdata == []


@pytest.mark.parametrize("list_measure, count_id, count_ts, generate_unicale_id, generate_unicale_ts",
                         [
                             (ElectricPowerValues_ArchType_name_list, 1, 1, True, True),
                             (ElectricPowerValues_ArchType_name_list, 2, 3, True, True),
                             (ElectricPowerValues_ArchType_name_list, 3, 1, True, True),
                             (ElectricPowerValues_ArchType_name_list, 1, 1, False, False),
                             (ElectricPowerValues_ArchType_name_list, 2, 3, False, False),
                             (ElectricPowerValues_ArchType_name_list, 3, 1, False, False)
                         ])
def test_POST_ElectricPowerValues_meterdata_db(type_connect,
                                               list_measure,
                                               count_id,
                                               count_ts,
                                               generate_unicale_id,
                                               generate_unicale_ts):
    sleep(1)
    meterdata = POST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                count_id=count_id,
                                                                count_ts=count_ts,
                                                                generate_unicale_id=generate_unicale_id,
                                                                generate_unicale_ts=generate_unicale_ts)

    assert meterdata == []


# ------------------------------------- PulseValues -----------------------------------------------------------------
parametrize_PulseValues_ArchType_name = parametrize_by_element(reqest='post',
                                                               ArchType_name_list=PulseValues_ArchType_name_list)


@pytest.mark.parametrize("list_measure, count_id, count_ts, generate_unicale_id, generate_unicale_ts",
                         parametrize_PulseValues_ArchType_name
                         )
def test_POST_PulseValues_meterdata_db_by_element(type_connect,
                                                  list_measure,
                                                  count_id,
                                                  count_ts,
                                                  generate_unicale_id,
                                                  generate_unicale_ts):
    sleep(1)
    meterdata = POST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                count_id=count_id,
                                                                count_ts=count_ts,
                                                                generate_unicale_id=generate_unicale_id,
                                                                generate_unicale_ts=generate_unicale_ts)

    assert meterdata == []


@pytest.mark.parametrize("list_measure, count_id, count_ts, generate_unicale_id, generate_unicale_ts",
                         [
                             (PulseValues_ArchType_name_list, 1, 1, True, True),
                             (PulseValues_ArchType_name_list, 2, 3, True, True),
                             (PulseValues_ArchType_name_list, 3, 1, True, True),
                             (PulseValues_ArchType_name_list, 1, 1, False, False),
                             (PulseValues_ArchType_name_list, 2, 3, False, False),
                             (PulseValues_ArchType_name_list, 3, 1, False, False)
                         ]
                         )
def test_POST_PulseValues_meterdata_db(type_connect,
                                       list_measure,
                                       count_id,
                                       count_ts,
                                       generate_unicale_id,
                                       generate_unicale_ts):
    sleep(1)
    meterdata = POST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                count_id=count_id,
                                                                count_ts=count_ts,
                                                                generate_unicale_id=generate_unicale_id,
                                                                generate_unicale_ts=generate_unicale_ts)

    assert meterdata == []


# ------------------------------------- DigitalValues -----------------------------------------------------------------
parametrize_DigitalValues_ArchType_name = parametrize_by_element(reqest='post',
                                                                 ArchType_name_list=DigitalValues_ArchType_name_list)


@pytest.mark.parametrize("list_measure, count_id, count_ts, generate_unicale_id, generate_unicale_ts",
                         parametrize_DigitalValues_ArchType_name
                         )
def test_POST_DigitalValues_meterdata_db_by_element(type_connect,
                                                    list_measure,
                                                    count_id,
                                                    count_ts,
                                                    generate_unicale_id,
                                                    generate_unicale_ts):
    sleep(1)
    meterdata = POST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                count_id=count_id,
                                                                count_ts=count_ts,
                                                                generate_unicale_id=generate_unicale_id,
                                                                generate_unicale_ts=generate_unicale_ts)

    assert meterdata == []


@pytest.mark.parametrize("list_measure, count_id, count_ts, generate_unicale_id, generate_unicale_ts",
                         [
                             (DigitalValues_ArchType_name_list, 1, 1, True, True),
                             (DigitalValues_ArchType_name_list, 2, 3, True, True),
                             (DigitalValues_ArchType_name_list, 3, 1, True, True),
                             (DigitalValues_ArchType_name_list, 1, 1, False, False),
                             (DigitalValues_ArchType_name_list, 2, 3, False, False),
                             (DigitalValues_ArchType_name_list, 3, 1, False, False)
                         ]
                         )
def test_POST_DigitalValues_meterdata_db(type_connect,
                                         list_measure,
                                         count_id,
                                         count_ts,
                                         generate_unicale_id,
                                         generate_unicale_ts):
    sleep(1)
    meterdata = POST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                count_id=count_id,
                                                                count_ts=count_ts,
                                                                generate_unicale_id=generate_unicale_id,
                                                                generate_unicale_ts=generate_unicale_ts)

    assert meterdata == []


# ------------------------------------- JournalValues -----------------------------------------------------------------
parametrize_JournalValues_ArchType_name = parametrize_by_element(reqest='post',
                                                                 ArchType_name_list=JournalValues_ArchType_name_list)


@pytest.mark.parametrize("list_measure, count_id, count_ts, generate_unicale_id, generate_unicale_ts",
                         parametrize_JournalValues_ArchType_name)
def test_POST_JournalValues_meterdata_db_by_element(type_connect,
                                                    list_measure,
                                                    count_id,
                                                    count_ts,
                                                    generate_unicale_id,
                                                    generate_unicale_ts):
    sleep(1)
    meterdata = POST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                count_id=count_id,
                                                                count_ts=count_ts,
                                                                generate_unicale_id=generate_unicale_id,
                                                                generate_unicale_ts=generate_unicale_ts)

    assert meterdata == []


@pytest.mark.parametrize("list_measure, count_id, count_ts, generate_unicale_id, generate_unicale_ts",
                         [
                             (JournalValues_ArchType_name_list, 1, 1, True, True),
                             (JournalValues_ArchType_name_list, 2, 3, True, True),
                             (JournalValues_ArchType_name_list, 3, 1, True, True),
                             (JournalValues_ArchType_name_list, 1, 1, False, False),
                             (JournalValues_ArchType_name_list, 2, 3, False, False),
                             (JournalValues_ArchType_name_list, 3, 1, False, False)
                         ])
def test_POST_JournalValues_meterdata_db(type_connect,
                                         list_measure,
                                         count_id,
                                         count_ts,
                                         generate_unicale_id,
                                         generate_unicale_ts):
    sleep(1)
    meterdata = POST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                count_id=count_id,
                                                                count_ts=count_ts,
                                                                generate_unicale_id=generate_unicale_id,
                                                                generate_unicale_ts=generate_unicale_ts)

    assert meterdata == []


# -------------------------------------   AllTAGS ---------------------------------------------------------------------
all_ArchType_name_list = ElectricConfig_ArchType_name_list + PulseConfig_ArchType_name_list + DigitalConfig_ArchType_name_list + ElecticEnergyValues_ArchType_name_list + ElectricQualityValues_ArchType_name_list + ElectricPowerValues_ArchType_name_list + PulseValues_ArchType_name_list + DigitalValues_ArchType_name_list + JournalValues_ArchType_name_list


@pytest.mark.parametrize("list_measure, count_id, count_ts, generate_unicale_id, generate_unicale_ts",
                         [
                             (all_ArchType_name_list, 1, 1, True, True),
                             (all_ArchType_name_list, 2, 3, True, True),
                             (all_ArchType_name_list, 3, 1, True, True),
                             (all_ArchType_name_list, 1, 1, False, False),
                             (all_ArchType_name_list, 2, 3, False, False),
                             (all_ArchType_name_list, 3, 1, False, False)
                         ])
def test_POST_all_meterdata_db(type_connect,
                               list_measure,
                               count_id,
                               count_ts,
                               generate_unicale_id,
                               generate_unicale_ts):
    sleep(1)
    meterdata = POST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                count_id=count_id,
                                                                count_ts=count_ts,
                                                                generate_unicale_id=generate_unicale_id,
                                                                generate_unicale_ts=generate_unicale_ts)

    assert meterdata == []


# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------
#                                                  GET
# ---------------------------------------------------------------------------------------------------------------------

# ------------------------------------- ElectricConfig ----------------------------------------------------------------
# ElectricConfig
@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds",
    [

        (ElectricConfig_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False),
        (ElectricConfig_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False),
        (ElectricConfig_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False),
        (ElectricConfig_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False),
        (ElectricConfig_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True),
        (ElectricConfig_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True),
        (ElectricConfig_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True),
        (ElectricConfig_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True),
        (ElectricConfig_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False),
        (ElectricConfig_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True)

    ]
)
def test_GET_ElectricConfig_meterdata_db(
        type_connect,
        # Список из типов данных
        list_measure,
        # Сколько таймштампов выбираем
        select_count_ts,
        # Сколько айдишников выбираем
        select_count_id,
        # Сколько таймштампов генерируем в БД
        generate_count_ts,
        # Сколько айдишников генерируем в БД
        generate_count_id,
        # Число выбираемых тэгов
        count_tags,
        # Булевый маркер -  Селект по внутренему айдишнику
        select_device_idx,
        # Булевый маркер - Селект по внешнему айдишнику
        select_meter_id,
        # Булевый маркер - Селект по серийнику
        serial,
        # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
        select_id_all,
        # Булевый маркер - Селект только последнего времени
        select_last_time,
        # Булевый маркер - Выход за границы времени что сгенерировали
        out_of_bounds
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                               select_count_ts=select_count_ts,
                                                               select_count_id=select_count_id,
                                                               generate_count_ts=generate_count_ts,
                                                               generate_count_id=generate_count_id,
                                                               count_tags=count_tags,
                                                               select_device_idx=select_device_idx,
                                                               select_meter_id=select_meter_id,
                                                               serial=serial,
                                                               select_id_all=select_id_all,
                                                               select_last_time=select_last_time,
                                                               out_of_bounds=out_of_bounds
                                                               )

    assert meterdata == []


# ------------------------------------- PulseConfig -----------------------------------------------------------------
# PulseConfig

@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds",
    [
        (PulseConfig_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False),
        (PulseConfig_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False),
        (PulseConfig_ArchType_name_list, 2, 3, 3, 4, 2, False, False, False, True, False, False),
        (PulseConfig_ArchType_name_list, 4, 4, 4, 5, 3, True, False, False, False, False, False),
        (PulseConfig_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True),
        (PulseConfig_ArchType_name_list, 1, 4, 2, 5, 3, False, False, False, True, False, True),
        (PulseConfig_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True),
        (PulseConfig_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True),
        (PulseConfig_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False),
        (PulseConfig_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True)

    ]
)
def test_GET_PulseConfig_meterdata_db(
        type_connect,
        # Список из типов данных
        list_measure,
        # Сколько таймштампов выбираем
        select_count_ts,
        # Сколько айдишников выбираем
        select_count_id,
        # Сколько таймштампов генерируем в БД
        generate_count_ts,
        # Сколько айдишников генерируем в БД
        generate_count_id,
        # Число выбираемых тэгов
        count_tags,
        # Булевый маркер -  Селект по внутренему айдишнику
        select_device_idx,
        # Булевый маркер - Селект по внешнему айдишнику
        select_meter_id,
        # Булевый маркер - Селект по серийнику
        serial,
        # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
        select_id_all,
        # Булевый маркер - Селект только последнего времени
        select_last_time,
        # Булевый маркер - Выход за границы времени что сгенерировали
        out_of_bounds
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                               select_count_ts=select_count_ts,
                                                               select_count_id=select_count_id,
                                                               generate_count_ts=generate_count_ts,
                                                               generate_count_id=generate_count_id,
                                                               count_tags=count_tags,
                                                               select_device_idx=select_device_idx,
                                                               select_meter_id=select_meter_id,
                                                               serial=serial,
                                                               select_id_all=select_id_all,
                                                               select_last_time=select_last_time,
                                                               out_of_bounds=out_of_bounds
                                                               )

    assert meterdata == []


# # -------------------------------------DigitalConfig -----------------------------------------------------------------
# # DigitalConfig


@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds",
    [
        (DigitalConfig_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False),
        (DigitalConfig_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False),
        (DigitalConfig_ArchType_name_list, 2, 3, 3, 4, 2, True, False, False, False, False, False),
        (DigitalConfig_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False),
        (DigitalConfig_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True),
        (DigitalConfig_ArchType_name_list, 1, 4, 2, 5, 3, True, False, False, False, False, True),
        (DigitalConfig_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True),
        (DigitalConfig_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True),
        (DigitalConfig_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False),
        (DigitalConfig_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True)

    ]
)
def test_GET_DigitalConfig_meterdata_db(
        type_connect,
        # Список из типов данных
        list_measure,
        # Сколько таймштампов выбираем
        select_count_ts,
        # Сколько айдишников выбираем
        select_count_id,
        # Сколько таймштампов генерируем в БД
        generate_count_ts,
        # Сколько айдишников генерируем в БД
        generate_count_id,
        # Число выбираемых тэгов
        count_tags,
        # Булевый маркер -  Селект по внутренему айдишнику
        select_device_idx,
        # Булевый маркер - Селект по внешнему айдишнику
        select_meter_id,
        # Булевый маркер - Селект по серийнику
        serial,
        # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
        select_id_all,
        # Булевый маркер - Селект только последнего времени
        select_last_time,
        # Булевый маркер - Выход за границы времени что сгенерировали
        out_of_bounds
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                               select_count_ts=select_count_ts,
                                                               select_count_id=select_count_id,
                                                               generate_count_ts=generate_count_ts,
                                                               generate_count_id=generate_count_id,
                                                               count_tags=count_tags,
                                                               select_device_idx=select_device_idx,
                                                               select_meter_id=select_meter_id,
                                                               serial=serial,
                                                               select_id_all=select_id_all,
                                                               select_last_time=select_last_time,
                                                               out_of_bounds=out_of_bounds
                                                               )

    assert meterdata == []


# # ------------------------------------- ElecticEnergyValues ----------------------------------------------------------
parametrize_ElecticEnergyValues_ArchType_name_list = parametrize_by_element(reqest='get',
                                                                            ArchType_name_list=ElecticEnergyValues_ArchType_name_list)


@pytest.mark.parametrize("list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , "
                         "count_tags , select_device_idx , select_meter_id , serial, select_id_all , select_last_time"
                         " , out_of_bounds",
                         parametrize_ElecticEnergyValues_ArchType_name_list)
def test_GET_ElecticEnergyValues_meterdata_db_by_element(
        type_connect,
        # Список из типов данных
        list_measure,
        # Сколько таймштампов выбираем
        select_count_ts,
        # Сколько айдишников выбираем
        select_count_id,
        # Сколько таймштампов генерируем в БД
        generate_count_ts,
        # Сколько айдишников генерируем в БД
        generate_count_id,
        # Число выбираемых тэгов
        count_tags,
        # Булевый маркер -  Селект по внутренему айдишнику
        select_device_idx,
        # Булевый маркер - Селект по внешнему айдишнику
        select_meter_id,
        # Булевый маркер - Селект по серийнику
        serial,
        # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
        select_id_all,
        # Булевый маркер - Селект только последнего времени
        select_last_time,
        # Булевый маркер - Выход за границы времени что сгенерировали
        out_of_bounds
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                               select_count_ts=select_count_ts,
                                                               select_count_id=select_count_id,
                                                               generate_count_ts=generate_count_ts,
                                                               generate_count_id=generate_count_id,
                                                               count_tags=count_tags,
                                                               select_device_idx=select_device_idx,
                                                               select_meter_id=select_meter_id,
                                                               serial=serial,
                                                               select_id_all=select_id_all,
                                                               select_last_time=select_last_time,
                                                               out_of_bounds=out_of_bounds
                                                               )

    assert meterdata == []


# ElecticEnergyValues

@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds",
    [
        (ElecticEnergyValues_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False),
        (ElecticEnergyValues_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False),
        (ElecticEnergyValues_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False),
        (ElecticEnergyValues_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False),
        (ElecticEnergyValues_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True),
        (ElecticEnergyValues_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True),
        (ElecticEnergyValues_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True),
        (ElecticEnergyValues_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True),
        (ElecticEnergyValues_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False),
        (ElecticEnergyValues_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True)

    ]
)
def test_GET_ElecticEnergyValues_meterdata_db(
        type_connect,
        # Список из типов данных
        list_measure,
        # Сколько таймштампов выбираем
        select_count_ts,
        # Сколько айдишников выбираем
        select_count_id,
        # Сколько таймштампов генерируем в БД
        generate_count_ts,
        # Сколько айдишников генерируем в БД
        generate_count_id,
        # Число выбираемых тэгов
        count_tags,
        # Булевый маркер -  Селект по внутренему айдишнику
        select_device_idx,
        # Булевый маркер - Селект по внешнему айдишнику
        select_meter_id,
        # Булевый маркер - Селект по серийнику
        serial,
        # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
        select_id_all,
        # Булевый маркер - Селект только последнего времени
        select_last_time,
        # Булевый маркер - Выход за границы времени что сгенерировали
        out_of_bounds
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                               select_count_ts=select_count_ts,
                                                               select_count_id=select_count_id,
                                                               generate_count_ts=generate_count_ts,
                                                               generate_count_id=generate_count_id,
                                                               count_tags=count_tags,
                                                               select_device_idx=select_device_idx,
                                                               select_meter_id=select_meter_id,
                                                               serial=serial,
                                                               select_id_all=select_id_all,
                                                               select_last_time=select_last_time,
                                                               out_of_bounds=out_of_bounds
                                                               )

    assert meterdata == []


# # ------------------------------------- ElectricQualityValues ---------------------------------------------------------
# ElectricQualityValues

@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds",
    [
        (ElectricQualityValues_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False),
        (ElectricQualityValues_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False),
        (ElectricQualityValues_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False),
        (ElectricQualityValues_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False),
        (ElectricQualityValues_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True),
        (ElectricQualityValues_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True),
        (ElectricQualityValues_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True),
        (ElectricQualityValues_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True),
        (ElectricQualityValues_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False),
        (ElectricQualityValues_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True)

    ]
)
def test_GET_ElectricQualityValues_meterdata_db(
        type_connect,
        # Список из типов данных
        list_measure,
        # Сколько таймштампов выбираем
        select_count_ts,
        # Сколько айдишников выбираем
        select_count_id,
        # Сколько таймштампов генерируем в БД
        generate_count_ts,
        # Сколько айдишников генерируем в БД
        generate_count_id,
        # Число выбираемых тэгов
        count_tags,
        # Булевый маркер -  Селект по внутренему айдишнику
        select_device_idx,
        # Булевый маркер - Селект по внешнему айдишнику
        select_meter_id,
        # Булевый маркер - Селект по серийнику
        serial,
        # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
        select_id_all,
        # Булевый маркер - Селект только последнего времени
        select_last_time,
        # Булевый маркер - Выход за границы времени что сгенерировали
        out_of_bounds
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                               select_count_ts=select_count_ts,
                                                               select_count_id=select_count_id,
                                                               generate_count_ts=generate_count_ts,
                                                               generate_count_id=generate_count_id,
                                                               count_tags=count_tags,
                                                               select_device_idx=select_device_idx,
                                                               select_meter_id=select_meter_id,
                                                               serial=serial,
                                                               select_id_all=select_id_all,
                                                               select_last_time=select_last_time,
                                                               out_of_bounds=out_of_bounds
                                                               )

    assert meterdata == []


#


# # ------------------------------------- ElectricPowerValues -----------------------------------------------------------
parametrize_ElectricPowerValues_ArchType_name_list = parametrize_by_element(
    reqest='get',
    ArchType_name_list=ElectricPowerValues_ArchType_name_list)


@pytest.mark.parametrize("list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , "
                         "count_tags , select_device_idx , select_meter_id , serial, select_id_all , select_last_time"
                         " , out_of_bounds",
                         parametrize_ElectricPowerValues_ArchType_name_list)
def test_GET_ElectricPowerValues_meterdata_db_by_element(
        type_connect,
        # Список из типов данных
        list_measure,
        # Сколько таймштампов выбираем
        select_count_ts,
        # Сколько айдишников выбираем
        select_count_id,
        # Сколько таймштампов генерируем в БД
        generate_count_ts,
        # Сколько айдишников генерируем в БД
        generate_count_id,
        # Число выбираемых тэгов
        count_tags,
        # Булевый маркер -  Селект по внутренему айдишнику
        select_device_idx,
        # Булевый маркер - Селект по внешнему айдишнику
        select_meter_id,
        # Булевый маркер - Селект по серийнику
        serial,
        # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
        select_id_all,
        # Булевый маркер - Селект только последнего времени
        select_last_time,
        # Булевый маркер - Выход за границы времени что сгенерировали
        out_of_bounds
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                               select_count_ts=select_count_ts,
                                                               select_count_id=select_count_id,
                                                               generate_count_ts=generate_count_ts,
                                                               generate_count_id=generate_count_id,
                                                               count_tags=count_tags,
                                                               select_device_idx=select_device_idx,
                                                               select_meter_id=select_meter_id,
                                                               serial=serial,
                                                               select_id_all=select_id_all,
                                                               select_last_time=select_last_time,
                                                               out_of_bounds=out_of_bounds
                                                               )

    assert meterdata == []


# ElectricPowerValues


@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds",
    [
        (ElectricPowerValues_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False),
        (ElectricPowerValues_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False),
        (ElectricPowerValues_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False),
        (ElectricPowerValues_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False),
        (ElectricPowerValues_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True),
        (ElectricPowerValues_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True),
        (ElectricPowerValues_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True),
        (ElectricPowerValues_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True),
        (ElectricPowerValues_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False),
        (ElectricPowerValues_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True)

    ]
)
def test_GET_ElectricPowerValues_meterdata_db(
        type_connect,
        # Список из типов данных
        list_measure,
        # Сколько таймштампов выбираем
        select_count_ts,
        # Сколько айдишников выбираем
        select_count_id,
        # Сколько таймштампов генерируем в БД
        generate_count_ts,
        # Сколько айдишников генерируем в БД
        generate_count_id,
        # Число выбираемых тэгов
        count_tags,
        # Булевый маркер -  Селект по внутренему айдишнику
        select_device_idx,
        # Булевый маркер - Селект по внешнему айдишнику
        select_meter_id,
        # Булевый маркер - Селект по серийнику
        serial,
        # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
        select_id_all,
        # Булевый маркер - Селект только последнего времени
        select_last_time,
        # Булевый маркер - Выход за границы времени что сгенерировали
        out_of_bounds
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                               select_count_ts=select_count_ts,
                                                               select_count_id=select_count_id,
                                                               generate_count_ts=generate_count_ts,
                                                               generate_count_id=generate_count_id,
                                                               count_tags=count_tags,
                                                               select_device_idx=select_device_idx,
                                                               select_meter_id=select_meter_id,
                                                               serial=serial,
                                                               select_id_all=select_id_all,
                                                               select_last_time=select_last_time,
                                                               out_of_bounds=out_of_bounds
                                                               )

    assert meterdata == []


# # ------------------------------------- PulseValues -----------------------------------------------------------------
parametrize_PulseValues_ArchType_name = parametrize_by_element(reqest='get',
                                                               ArchType_name_list=PulseValues_ArchType_name_list)


@pytest.mark.parametrize("list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , "
                         "count_tags , select_device_idx , select_meter_id , serial, select_id_all , select_last_time"
                         " , out_of_bounds",
                         parametrize_PulseValues_ArchType_name
                         )
def test_GET_PulseValues_meterdata_db_by_element(
        type_connect,
        # Список из типов данных
        list_measure,
        # Сколько таймштампов выбираем
        select_count_ts,
        # Сколько айдишников выбираем
        select_count_id,
        # Сколько таймштампов генерируем в БД
        generate_count_ts,
        # Сколько айдишников генерируем в БД
        generate_count_id,
        # Число выбираемых тэгов
        count_tags,
        # Булевый маркер -  Селект по внутренему айдишнику
        select_device_idx,
        # Булевый маркер - Селект по внешнему айдишнику
        select_meter_id,
        # Булевый маркер - Селект по серийнику
        serial,
        # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
        select_id_all,
        # Булевый маркер - Селект только последнего времени
        select_last_time,
        # Булевый маркер - Выход за границы времени что сгенерировали
        out_of_bounds
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                               select_count_ts=select_count_ts,
                                                               select_count_id=select_count_id,
                                                               generate_count_ts=generate_count_ts,
                                                               generate_count_id=generate_count_id,
                                                               count_tags=count_tags,
                                                               select_device_idx=select_device_idx,
                                                               select_meter_id=select_meter_id,
                                                               serial=serial,
                                                               select_id_all=select_id_all,
                                                               select_last_time=select_last_time,
                                                               out_of_bounds=out_of_bounds
                                                               )

    assert meterdata == []


# PulseValues


@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds",
    [
        (PulseValues_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False),
        (PulseValues_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False),
        (PulseValues_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False),
        (PulseValues_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False),
        (PulseValues_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True),
        (PulseValues_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True),
        (PulseValues_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True),
        (PulseValues_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True),
        (PulseValues_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False),
        (PulseValues_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True)

    ]
)
def test_GET_PulseValues_meterdata_db(
        type_connect,
        # Список из типов данных
        list_measure,
        # Сколько таймштампов выбираем
        select_count_ts,
        # Сколько айдишников выбираем
        select_count_id,
        # Сколько таймштампов генерируем в БД
        generate_count_ts,
        # Сколько айдишников генерируем в БД
        generate_count_id,
        # Число выбираемых тэгов
        count_tags,
        # Булевый маркер -  Селект по внутренему айдишнику
        select_device_idx,
        # Булевый маркер - Селект по внешнему айдишнику
        select_meter_id,
        # Булевый маркер - Селект по серийнику
        serial,
        # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
        select_id_all,
        # Булевый маркер - Селект только последнего времени
        select_last_time,
        # Булевый маркер - Выход за границы времени что сгенерировали
        out_of_bounds
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                               select_count_ts=select_count_ts,
                                                               select_count_id=select_count_id,
                                                               generate_count_ts=generate_count_ts,
                                                               generate_count_id=generate_count_id,
                                                               count_tags=count_tags,
                                                               select_device_idx=select_device_idx,
                                                               select_meter_id=select_meter_id,
                                                               serial=serial,
                                                               select_id_all=select_id_all,
                                                               select_last_time=select_last_time,
                                                               out_of_bounds=out_of_bounds
                                                               )

    assert meterdata == []


# ------------------------------------- DigitalValues -----------------------------------------------------------------
parametrize_DigitalValues_ArchType_name = parametrize_by_element(reqest='get',
                                                                 ArchType_name_list=DigitalValues_ArchType_name_list)


@pytest.mark.parametrize("list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , "
                         "count_tags , select_device_idx , select_meter_id , serial, select_id_all , select_last_time"
                         " , out_of_bounds",
                         parametrize_DigitalValues_ArchType_name
                         )
def test_GET_DigitalValues_meterdata_db_by_element(
        type_connect,
        # Список из типов данных
        list_measure,
        # Сколько таймштампов выбираем
        select_count_ts,
        # Сколько айдишников выбираем
        select_count_id,
        # Сколько таймштампов генерируем в БД
        generate_count_ts,
        # Сколько айдишников генерируем в БД
        generate_count_id,
        # Число выбираемых тэгов
        count_tags,
        # Булевый маркер -  Селект по внутренему айдишнику
        select_device_idx,
        # Булевый маркер - Селект по внешнему айдишнику
        select_meter_id,
        # Булевый маркер - Селект по серийнику
        serial,
        # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
        select_id_all,
        # Булевый маркер - Селект только последнего времени
        select_last_time,
        # Булевый маркер - Выход за границы времени что сгенерировали
        out_of_bounds
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                               select_count_ts=select_count_ts,
                                                               select_count_id=select_count_id,
                                                               generate_count_ts=generate_count_ts,
                                                               generate_count_id=generate_count_id,
                                                               count_tags=count_tags,
                                                               select_device_idx=select_device_idx,
                                                               select_meter_id=select_meter_id,
                                                               serial=serial,
                                                               select_id_all=select_id_all,
                                                               select_last_time=select_last_time,
                                                               out_of_bounds=out_of_bounds
                                                               )

    assert meterdata == []


# DigitalValues


@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds",
    [
        (DigitalValues_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False),
        (DigitalValues_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False),
        (DigitalValues_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False),
        (DigitalValues_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False),
        (DigitalValues_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True),
        (DigitalValues_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True),
        (DigitalValues_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True),
        (DigitalValues_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True),
        (DigitalValues_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False),
        (DigitalValues_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True)

    ]
)
def test_GET_DigitalValues_meterdata_db(
        type_connect,
        # Список из типов данных
        list_measure,
        # Сколько таймштампов выбираем
        select_count_ts,
        # Сколько айдишников выбираем
        select_count_id,
        # Сколько таймштампов генерируем в БД
        generate_count_ts,
        # Сколько айдишников генерируем в БД
        generate_count_id,
        # Число выбираемых тэгов
        count_tags,
        # Булевый маркер -  Селект по внутренему айдишнику
        select_device_idx,
        # Булевый маркер - Селект по внешнему айдишнику
        select_meter_id,
        # Булевый маркер - Селект по серийнику
        serial,
        # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
        select_id_all,
        # Булевый маркер - Селект только последнего времени
        select_last_time,
        # Булевый маркер - Выход за границы времени что сгенерировали
        out_of_bounds
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                               select_count_ts=select_count_ts,
                                                               select_count_id=select_count_id,
                                                               generate_count_ts=generate_count_ts,
                                                               generate_count_id=generate_count_id,
                                                               count_tags=count_tags,
                                                               select_device_idx=select_device_idx,
                                                               select_meter_id=select_meter_id,
                                                               serial=serial,
                                                               select_id_all=select_id_all,
                                                               select_last_time=select_last_time,
                                                               out_of_bounds=out_of_bounds
                                                               )

    assert meterdata == []


# ------------------------------------- JournalValues -----------------------------------------------------------------
parametrize_JournalValues_ArchType_name = parametrize_by_element(reqest='get',
                                                                 ArchType_name_list=JournalValues_ArchType_name_list)


@pytest.mark.parametrize("list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , "
                         "count_tags , select_device_idx , select_meter_id , serial, select_id_all , select_last_time"
                         " , out_of_bounds",
                         parametrize_JournalValues_ArchType_name)
def test_GET_JournalValues_meterdata_db_by_element(
        type_connect,
        # Список из типов данных
        list_measure,
        # Сколько таймштампов выбираем
        select_count_ts,
        # Сколько айдишников выбираем
        select_count_id,
        # Сколько таймштампов генерируем в БД
        generate_count_ts,
        # Сколько айдишников генерируем в БД
        generate_count_id,
        # Число выбираемых тэгов
        count_tags,
        # Булевый маркер -  Селект по внутренему айдишнику
        select_device_idx,
        # Булевый маркер - Селект по внешнему айдишнику
        select_meter_id,
        # Булевый маркер - Селект по серийнику
        serial,
        # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
        select_id_all,
        # Булевый маркер - Селект только последнего времени
        select_last_time,
        # Булевый маркер - Выход за границы времени что сгенерировали
        out_of_bounds
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                               select_count_ts=select_count_ts,
                                                               select_count_id=select_count_id,
                                                               generate_count_ts=generate_count_ts,
                                                               generate_count_id=generate_count_id,
                                                               count_tags=count_tags,
                                                               select_device_idx=select_device_idx,
                                                               select_meter_id=select_meter_id,
                                                               serial=serial,
                                                               select_id_all=select_id_all,
                                                               select_last_time=select_last_time,
                                                               out_of_bounds=out_of_bounds
                                                               )

    assert meterdata == []


# JournalValues

@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds",
    [
        (JournalValues_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False),
        (JournalValues_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False),
        (JournalValues_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False),
        (JournalValues_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False),
        (JournalValues_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True),
        (JournalValues_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True),
        (JournalValues_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True),
        (JournalValues_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True),
        (JournalValues_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False),
        (JournalValues_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True)

    ]
)
def test_GET_JournalValues_meterdata_db(
        type_connect,
        # Список из типов данных
        list_measure,
        # Сколько таймштампов выбираем
        select_count_ts,
        # Сколько айдишников выбираем
        select_count_id,
        # Сколько таймштампов генерируем в БД
        generate_count_ts,
        # Сколько айдишников генерируем в БД
        generate_count_id,
        # Число выбираемых тэгов
        count_tags,
        # Булевый маркер -  Селект по внутренему айдишнику
        select_device_idx,
        # Булевый маркер - Селект по внешнему айдишнику
        select_meter_id,
        # Булевый маркер - Селект по серийнику
        serial,
        # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
        select_id_all,
        # Булевый маркер - Селект только последнего времени
        select_last_time,
        # Булевый маркер - Выход за границы времени что сгенерировали
        out_of_bounds
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                               select_count_ts=select_count_ts,
                                                               select_count_id=select_count_id,
                                                               generate_count_ts=generate_count_ts,
                                                               generate_count_id=generate_count_id,
                                                               count_tags=count_tags,
                                                               select_device_idx=select_device_idx,
                                                               select_meter_id=select_meter_id,
                                                               serial=serial,
                                                               select_id_all=select_id_all,
                                                               select_last_time=select_last_time,
                                                               out_of_bounds=out_of_bounds
                                                               )

    assert meterdata == []


# # -------------------------------------   AllTAGS ---------------------------------------------------------------------
all_ArchType_name_list = ElectricConfig_ArchType_name_list + ElecticEnergyValues_ArchType_name_list + ElectricQualityValues_ArchType_name_list + ElectricPowerValues_ArchType_name_list + PulseValues_ArchType_name_list + DigitalValues_ArchType_name_list + JournalValues_ArchType_name_list


@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds",
    [
        (all_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False),
        (all_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False),
        (all_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False),
        (all_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False),
        (all_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True),
        (all_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True),
        (all_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True),
        (all_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True),
        (all_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False),
        (all_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True)

    ]
)
def test_GET_all_ArchType_name_meterdata_db(
        type_connect,
        # Список из типов данных
        list_measure,
        # Сколько таймштампов выбираем
        select_count_ts,
        # Сколько айдишников выбираем
        select_count_id,
        # Сколько таймштампов генерируем в БД
        generate_count_ts,
        # Сколько айдишников генерируем в БД
        generate_count_id,
        # Число выбираемых тэгов
        count_tags,
        # Булевый маркер -  Селект по внутренему айдишнику
        select_device_idx,
        # Булевый маркер - Селект по внешнему айдишнику
        select_meter_id,
        # Булевый маркер - Селект по серийнику
        serial,
        # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
        select_id_all,
        # Булевый маркер - Селект только последнего времени
        select_last_time,
        # Булевый маркер - Выход за границы времени что сгенерировали
        out_of_bounds
):
    deleteMeterTable()
    sleep(2)
    meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                               select_count_ts=select_count_ts,
                                                               select_count_id=select_count_id,
                                                               generate_count_ts=generate_count_ts,
                                                               generate_count_id=generate_count_id,
                                                               count_tags=count_tags,
                                                               select_device_idx=select_device_idx,
                                                               select_meter_id=select_meter_id,
                                                               serial=serial,
                                                               select_id_all=select_id_all,
                                                               select_last_time=select_last_time,
                                                               out_of_bounds=out_of_bounds
                                                               )

    assert meterdata == []
