# Здесь расположим тесты на MeterData  многопоточном режиме

from working_directory.Meter_db_data_API import ThreadingPOST, ThreadingGET
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes
from working_directory.sqlite import deleteMeterTable
from time import sleep, time
import pytest

from random import randint
# Загружаем тестовые данные

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
    template_parametrize = []
    # Если у нас гет запрос
    if reqest == 'post':
        template_parametrize = [
            [1, 1, {}, randint(5, 10)],
            [2, 3, {}, randint(5, 10)],
            [3, 1, {}, randint(5, 10)],
            [1, 1, {}, randint(5, 10)],
            [2, 3, {}, randint(5, 10)],
            [3, 1, {}, randint(5, 10)]
        ]
    if reqest == 'get':
        template_parametrize = [
            [0, 1, 1, 2, 0, True, False, False, False, False, False, {}, randint(5, 10)],
            [1, 2, 2, 3, 1, False, True, False, False, False, False, {}, randint(5, 10)],
            [2, 3, 3, 4, 2, False, False, True, False, False, False, {}, randint(5, 10)],
            [4, 4, 4, 5, 3, False, False, False, True, False, False, {}, randint(5, 10)],
            [0, 5, 1, 6, 4, False, False, False, True, False, True, {}, randint(5, 10)],
            [1, 4, 2, 5, 3, False, False, True, False, False, True, {}, randint(5, 10)],
            [2, 5, 3, 6, 2, False, True, False, False, False, True, {}, randint(5, 10)],
            [4, 4, 4, 5, 1, True, False, False, False, False, True, {}, randint(5, 10)],
            [2, 3, 3, 4, 0, True, False, False, False, True, False, {}, randint(5, 10)],
            [2, 2, 3, 3, 0, False, True, False, False, True, True, {}, randint(5, 10)]
        ]
    for i in range(len(ArchType_name_list)):
        ArchType_name = [ArchType_name_list[i]]
        for x in range(len(template_parametrize)):
            element = tuple([ArchType_name] + template_parametrize[x])
            parametrize_list.append(element)
    return parametrize_list


# ---------------------------------------------------------------------------------------------------------------------
#                                                  POST
# ---------------------------------------------------------------------------------------------------------------------
# list_measure - Список из Тэгов
# count_id - Количество айдишников
# count_ts колличество времени
# generate_unicale_id - сгенерировать уникальные айдишник
# generate_unicale_ts - Сгенерирвоать уникальный таймштамп

# ------------------------------------- ElectricConfig -----------------------------------------------------------------
@pytest.mark.parametrize("list_measure, count_id, count_ts, tags, thread",
                         [
                             (ElectricConfig_ArchType_name_list, 1, 1, {}, randint(5, 10)),
                             (ElectricConfig_ArchType_name_list, 2, 3, {}, randint(5, 10)),
                             (ElectricConfig_ArchType_name_list, 3, 1, {}, randint(5, 10)),
                             (ElectricConfig_ArchType_name_list, 1, 1, {}, randint(5, 10)),
                             (ElectricConfig_ArchType_name_list, 2, 3, {}, randint(5, 10)),
                             (ElectricConfig_ArchType_name_list, 3, 1, {}, randint(5, 10))
                         ])
def test_POST_ElectricConfig_meterdata_db(type_connect,
                                          list_measure,
                                          count_id,
                                          count_ts,
                                          tags,
                                          # Количество потоков
                                          thread):
    # Чистим БД
    time_start = time()
    deleteMeterTable()
    sleep(1)
    meterdata = ThreadingPOST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                         count_id=count_id,
                                                                         count_ts=count_ts,
                                                                         tags=tags,
                                                                         thread=thread)
    time_finis = time()
    print('ТЕСТ ПРОХОДИЛ :', time_finis - time_start)

    assert meterdata == []


# ------------------------------------- PulseConfig -----------------------------------------------------------------
@pytest.mark.parametrize("list_measure, count_id, count_ts, tags, thread",
                         [
                             (PulseConfig_ArchType_name_list, 1, 1, {}, randint(5, 10)),
                             (PulseConfig_ArchType_name_list, 2, 3, {}, randint(5, 10)),
                             (PulseConfig_ArchType_name_list, 3, 1, {}, randint(5, 10)),
                             (PulseConfig_ArchType_name_list, 1, 1, {}, randint(5, 10)),
                             (PulseConfig_ArchType_name_list, 2, 3, {}, randint(5, 10)),
                             (PulseConfig_ArchType_name_list, 3, 1, {}, randint(5, 10))
                         ])
def test_POST_PulseConfig_meterdata_db(type_connect,
                                       list_measure,
                                       count_id,
                                       count_ts,
                                       tags,
                                       # Количество потоков
                                       thread):
    # Чистим БД

    deleteMeterTable()
    sleep(1)
    meterdata = ThreadingPOST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                         count_id=count_id,
                                                                         count_ts=count_ts,
                                                                         tags=tags,
                                                                         thread=thread)

    assert meterdata == []


# -------------------------------------DigitalConfig -----------------------------------------------------------------
@pytest.mark.parametrize("list_measure, count_id, count_ts, tags, thread",
                         [
                             (DigitalConfig_ArchType_name_list, 1, 1, {}, randint(5, 10)),
                             (DigitalConfig_ArchType_name_list, 2, 3, {}, randint(5, 10)),
                             (DigitalConfig_ArchType_name_list, 3, 1, {}, randint(5, 10)),
                             (DigitalConfig_ArchType_name_list, 1, 1, {}, randint(5, 10)),
                             (DigitalConfig_ArchType_name_list, 2, 3, {}, randint(5, 10)),
                             (DigitalConfig_ArchType_name_list, 3, 1, {}, randint(5, 10))
                         ])
def test_POST_DigitalConfig_meterdata_db(type_connect, list_measure,
                                         count_id,
                                         count_ts,
                                         tags,
                                         # Количество потоков
                                         thread):
    # Чистим БД

    deleteMeterTable()
    sleep(1)
    meterdata = ThreadingPOST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                         count_id=count_id,
                                                                         count_ts=count_ts,
                                                                         tags=tags,
                                                                         thread=thread)

    assert meterdata == []


# ------------------------------------- ElecticEnergyValues ----------------------------------------------------------


parametrize_ElecticEnergyValues_ArchType_name_list = parametrize_by_element(
                                                            reqest='post',
                                                            ArchType_name_list=ElecticEnergyValues_ArchType_name_list
                                                                            )


@pytest.mark.parametrize("list_measure, count_id, count_ts, tags, thread",
                         parametrize_ElecticEnergyValues_ArchType_name_list)
def test_POST_ElecticEnergyValues_meterdata_db_by_element(type_connect, list_measure,
                                                          count_id,
                                                          count_ts,
                                                          tags,
                                                          # Количество потоков
                                                          thread):
    # Чистим БД

    deleteMeterTable()
    sleep(1)
    meterdata = ThreadingPOST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                         count_id=count_id,
                                                                         count_ts=count_ts,
                                                                         tags=tags,
                                                                         thread=thread)

    assert meterdata == []


@pytest.mark.parametrize("list_measure, count_id, count_ts, tags, thread",
                         [
                             (ElecticEnergyValues_ArchType_name_list, 1, 1, {}, randint(5, 50)),
                             (ElecticEnergyValues_ArchType_name_list, 2, 3, {}, randint(5, 50)),
                             (ElecticEnergyValues_ArchType_name_list, 3, 1, {}, randint(5, 50)),
                             (ElecticEnergyValues_ArchType_name_list, 1, 1, {}, randint(5, 50)),
                             (ElecticEnergyValues_ArchType_name_list, 2, 3, {}, randint(5, 50)),
                             (ElecticEnergyValues_ArchType_name_list, 3, 1, {}, randint(5, 50))
                         ])
def test_POST_ElecticEnergyValues_meterdata_db(type_connect, list_measure,
                                               count_id,
                                               count_ts,
                                               tags,
                                               # Количество потоков
                                               thread):
    # Чистим БД

    deleteMeterTable()
    sleep(1)
    meterdata = ThreadingPOST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                         count_id=count_id,
                                                                         count_ts=count_ts,
                                                                         tags=tags,
                                                                         thread=thread)

    assert meterdata == []


# ------------------------------------- ElectricQualityValues ---------------------------------------------------------
@pytest.mark.parametrize("list_measure, count_id, count_ts, tags, thread",
                         [
                             (ElectricQualityValues_ArchType_name_list, 1, 1, {}, randint(5, 10)),
                             (ElectricQualityValues_ArchType_name_list, 2, 3, {}, randint(5, 10)),
                             (ElectricQualityValues_ArchType_name_list, 3, 1, {}, randint(5, 10)),
                             (ElectricQualityValues_ArchType_name_list, 1, 1, {}, randint(5, 10)),
                             (ElectricQualityValues_ArchType_name_list, 2, 3, {}, randint(5, 10)),
                             (ElectricQualityValues_ArchType_name_list, 3, 1, {}, randint(5, 10))
                         ])
def test_POST_ElectricQualityValues_meterdata_db(type_connect, list_measure,
                                                 count_id,
                                                 count_ts,
                                                 tags,
                                                 # Количество потоков
                                                 thread):
    # Чистим БД

    deleteMeterTable()
    sleep(1)
    meterdata = ThreadingPOST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                         count_id=count_id,
                                                                         count_ts=count_ts,
                                                                         tags=tags,
                                                                         thread=thread)

    assert meterdata == []


# ------------------------------------- ElectricPowerValues -----------------------------------------------------------
parametrize_ElectricPowerValues_ArchType_name_list = parametrize_by_element(
                                                            reqest='post',
                                                            ArchType_name_list=ElectricPowerValues_ArchType_name_list
                                                                            )


@pytest.mark.parametrize("list_measure, count_id, count_ts, tags, thread",
                         parametrize_ElectricPowerValues_ArchType_name_list)
def test_POST_ElectricPowerValues_meterdata_db_by_element(type_connect,
                                                          list_measure,
                                                          count_id,
                                                          count_ts,
                                                          tags,
                                                          # Количество потоков
                                                          thread):
    # Чистим БД

    deleteMeterTable()
    sleep(1)
    meterdata = ThreadingPOST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                         count_id=count_id,
                                                                         count_ts=count_ts,
                                                                         tags=tags,
                                                                         thread=thread
                                                                         )

    assert meterdata == []


@pytest.mark.parametrize("list_measure, count_id, count_ts, tags, thread",
                         [
                             (ElectricPowerValues_ArchType_name_list, 1, 1, {}, randint(5, 50)),
                             (ElectricPowerValues_ArchType_name_list, 2, 3, {}, randint(5, 50)),
                             (ElectricPowerValues_ArchType_name_list, 3, 1, {}, randint(5, 50)),
                             (ElectricPowerValues_ArchType_name_list, 1, 1, {}, randint(5, 50)),
                             (ElectricPowerValues_ArchType_name_list, 2, 3, {}, randint(5, 50)),
                             (ElectricPowerValues_ArchType_name_list, 3, 1, {}, randint(5, 50))
                         ])
def test_POST_ElectricPowerValues_meterdata_db(type_connect,
                                               list_measure,
                                               count_id,
                                               count_ts,
                                               tags,
                                               # Количество потоков
                                               thread):
    # Чистим БД

    deleteMeterTable()
    sleep(1)
    meterdata = ThreadingPOST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                         count_id=count_id,
                                                                         count_ts=count_ts,
                                                                         tags=tags,
                                                                         thread=thread)

    assert meterdata == []


# ------------------------------------- PulseValues -----------------------------------------------------------------
parametrize_PulseValues_ArchType_name = parametrize_by_element(reqest='post',
                                                               ArchType_name_list=PulseValues_ArchType_name_list)


@pytest.mark.parametrize("list_measure, count_id, count_ts, tags, thread",
                         parametrize_PulseValues_ArchType_name
                         )
def test_POST_PulseValues_meterdata_db_by_element(type_connect,
                                                  list_measure,
                                                  count_id,
                                                  count_ts,
                                                  tags,
                                                  # Количество потоков
                                                  thread):
    # Чистим БД

    deleteMeterTable()
    sleep(1)
    meterdata = ThreadingPOST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                         count_id=count_id,
                                                                         count_ts=count_ts,
                                                                         tags=tags,
                                                                         thread=thread)

    assert meterdata == []


@pytest.mark.parametrize("list_measure, count_id, count_ts, tags, thread",
                         [
                             (PulseValues_ArchType_name_list, 1, 1, {}, randint(5, 50)),
                             (PulseValues_ArchType_name_list, 2, 3, {}, randint(5, 50)),
                             (PulseValues_ArchType_name_list, 3, 1, {}, randint(5, 50)),
                             (PulseValues_ArchType_name_list, 1, 1, {}, randint(5, 50)),
                             (PulseValues_ArchType_name_list, 2, 3, {}, randint(5, 50)),
                             (PulseValues_ArchType_name_list, 3, 1, {}, randint(5, 50))
                         ]
                         )
def test_POST_PulseValues_meterdata_db(type_connect,
                                       list_measure,
                                       count_id,
                                       count_ts,
                                       tags,
                                       # Количество потоков
                                       thread):
    # Чистим БД

    deleteMeterTable()
    sleep(1)
    meterdata = ThreadingPOST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                         count_id=count_id,
                                                                         count_ts=count_ts,
                                                                         tags=tags,
                                                                         thread=thread)

    assert meterdata == []


# ------------------------------------- DigitalValues -----------------------------------------------------------------

parametrize_DigitalValues_ArchType_name = parametrize_by_element(reqest='post',
                                                                 ArchType_name_list=DigitalValues_ArchType_name_list)


@pytest.mark.parametrize("list_measure, count_id, count_ts,tags, thread",
                         parametrize_DigitalValues_ArchType_name
                         )
def test_POST_DigitalValues_meterdata_db_by_element(type_connect,
                                                    list_measure,
                                                    count_id,
                                                    count_ts,
                                                    tags,
                                                    # Количество потоков
                                                    thread):
    # Чистим БД

    deleteMeterTable()
    sleep(1)
    meterdata = ThreadingPOST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                         count_id=count_id,
                                                                         count_ts=count_ts,
                                                                         tags=tags,
                                                                         thread=thread)

    assert meterdata == []


@pytest.mark.parametrize("list_measure, count_id, count_ts, tags, thread",
                         [
                             (DigitalValues_ArchType_name_list, 1, 1, {}, randint(5, 50)),
                             (DigitalValues_ArchType_name_list, 2, 3, {}, randint(5, 50)),
                             (DigitalValues_ArchType_name_list, 3, 1, {}, randint(5, 50)),
                             (DigitalValues_ArchType_name_list, 1, 1, {}, randint(5, 50)),
                             (DigitalValues_ArchType_name_list, 2, 3, {}, randint(5, 50)),
                             (DigitalValues_ArchType_name_list, 3, 1, {}, randint(5, 50))
                         ]
                         )
def test_POST_DigitalValues_meterdata_db(type_connect,
                                         list_measure,
                                         count_id,
                                         count_ts,
                                         tags,
                                         # Количество потоков
                                         thread):
    # Чистим БД

    deleteMeterTable()
    sleep(1)
    meterdata = ThreadingPOST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                         count_id=count_id,
                                                                         count_ts=count_ts,
                                                                         tags=tags,
                                                                         thread=thread)

    assert meterdata == []


# ------------------------------------- JournalValues -----------------------------------------------------------------
parametrize_JournalValues_ArchType_name = parametrize_by_element(reqest='post',
                                                                 ArchType_name_list=JournalValues_ArchType_name_list)


@pytest.mark.parametrize("list_measure, count_id, count_ts, tags, thread",
                         parametrize_JournalValues_ArchType_name)
def test_POST_JournalValues_meterdata_db_by_element(type_connect,
                                                    list_measure,
                                                    count_id,
                                                    count_ts,
                                                    tags,
                                                    # Количество потоков
                                                    thread):
    # Чистим БД

    deleteMeterTable()
    sleep(1)
    meterdata = ThreadingPOST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                         count_id=count_id,
                                                                         count_ts=count_ts,
                                                                         tags=tags,
                                                                         thread=thread)

    assert meterdata == []


@pytest.mark.parametrize("list_measure, count_id, count_ts, tags, thread",
                         [
                             (JournalValues_ArchType_name_list, 1, 1, {}, randint(5, 50)),
                             (JournalValues_ArchType_name_list, 2, 3, {}, randint(5, 50)),
                             (JournalValues_ArchType_name_list, 3, 1, {}, randint(5, 50)),
                             (JournalValues_ArchType_name_list, 1, 1, {}, randint(5, 50)),
                             (JournalValues_ArchType_name_list, 2, 3, {}, randint(5, 50)),
                             (JournalValues_ArchType_name_list, 3, 1, {}, randint(5, 50))
                         ])
def test_POST_JournalValues_meterdata_db(type_connect,
                                         list_measure,
                                         count_id,
                                         count_ts,
                                         tags,
                                         # Количество потоков
                                         thread):
    # Чистим БД

    deleteMeterTable()
    sleep(1)
    meterdata = ThreadingPOST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                         count_id=count_id,
                                                                         count_ts=count_ts,
                                                                         tags=tags,
                                                                         thread=thread)

    assert meterdata == []


# -------------------------------------   AllTAGS ---------------------------------------------------------------------
all_ArchType_name_list = ElectricConfig_ArchType_name_list + PulseConfig_ArchType_name_list + \
                         DigitalConfig_ArchType_name_list + ElecticEnergyValues_ArchType_name_list + \
                         ElectricQualityValues_ArchType_name_list + ElectricPowerValues_ArchType_name_list + \
                         PulseValues_ArchType_name_list + DigitalValues_ArchType_name_list + \
                         JournalValues_ArchType_name_list


@pytest.mark.parametrize("list_measure, count_id, count_ts, tags, thread",
                         [
                             (all_ArchType_name_list, 1, 1, {}, randint(5, 50)),
                             (all_ArchType_name_list, 2, 3, {}, randint(5, 50)),
                             (all_ArchType_name_list, 3, 1, {}, randint(5, 50)),
                             (all_ArchType_name_list, 1, 1, {}, randint(5, 50)),
                             (all_ArchType_name_list, 2, 3, {}, randint(5, 50)),
                             (all_ArchType_name_list, 3, 1, {}, randint(5, 50))
                         ])
def test_POST_all_meterdata_db(type_connect,
                               list_measure,
                               count_id,
                               count_ts,
                               tags,
                               # Количество потоков
                               thread):
    # Чистим БД

    deleteMeterTable()
    sleep(1)
    meterdata = ThreadingPOST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                         count_id=count_id,
                                                                         count_ts=count_ts,
                                                                         tags=tags,
                                                                         thread=thread)

    assert meterdata == []


# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------
#                                                  GET
# ---------------------------------------------------------------------------------------------------------------------

# ------------------------------------- ElectricConfig ----------------------------------------------------------------
# ElectricConfig
@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds , tags, thread",
    [

        (ElectricConfig_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False, {}, randint(5, 50)),
        (ElectricConfig_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False, {}, randint(5, 50)),
        (ElectricConfig_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False, {}, randint(5, 50)),
        (ElectricConfig_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False, {}, randint(5, 50)),
        (ElectricConfig_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True, {}, randint(5, 50)),
        (ElectricConfig_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True, {}, randint(5, 50)),
        (ElectricConfig_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True, {}, randint(5, 50)),
        (ElectricConfig_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True, {}, randint(5, 50)),
        (ElectricConfig_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False, {}, randint(5, 50)),
        (ElectricConfig_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True, {}, randint(5, 50))

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
        out_of_bounds,
        # Переопределенные тэги
        tags,
        # Количество потоков
        thread
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = ThreadingGET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
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
                                                                        out_of_bounds=out_of_bounds,
                                                                        tags=tags,
                                                                        thread=thread
                                                                        )

    assert meterdata == []


# ------------------------------------- PulseConfig -----------------------------------------------------------------
# PulseConfig

@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags, thread",
    [
        (PulseConfig_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False, {}, randint(5, 50)),
        (PulseConfig_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False, {}, randint(5, 50)),
        (PulseConfig_ArchType_name_list, 2, 3, 3, 4, 2, False, False, False, True, False, False, {}, randint(5, 50)),
        (PulseConfig_ArchType_name_list, 4, 4, 4, 5, 3, True, False, False, False, False, False, {}, randint(5, 50)),
        (PulseConfig_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True, {}, randint(5, 50)),
        (PulseConfig_ArchType_name_list, 1, 4, 2, 5, 3, False, False, False, True, False, True, {}, randint(5, 50)),
        (PulseConfig_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True, {}, randint(5, 50)),
        (PulseConfig_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True, {}, randint(5, 50)),
        (PulseConfig_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False, {}, randint(5, 50)),
        (PulseConfig_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True, {}, randint(5, 50))

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
        out_of_bounds,
        # Переопределенные тэги
        tags,
        # Количество потоков
        thread
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = ThreadingGET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
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
                                                                        out_of_bounds=out_of_bounds,
                                                                        tags=tags,
                                                                        thread=thread
                                                                        )

    assert meterdata == []


# # -------------------------------------DigitalConfig -----------------------------------------------------------------
# # DigitalConfig


@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds , tags, thread",
    [
        (DigitalConfig_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False, {}, randint(5, 50)),
        (DigitalConfig_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False, {}, randint(5, 50)),
        (DigitalConfig_ArchType_name_list, 2, 3, 3, 4, 2, True, False, False, False, False, False, {}, randint(5, 50)),
        (DigitalConfig_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False, {}, randint(5, 50)),
        (DigitalConfig_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True, {}, randint(5, 50)),
        (DigitalConfig_ArchType_name_list, 1, 4, 2, 5, 3, True, False, False, False, False, True, {}, randint(5, 50)),
        (DigitalConfig_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True, {}, randint(5, 50)),
        (DigitalConfig_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True, {}, randint(5, 50)),
        (DigitalConfig_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False, {}, randint(5, 50)),
        (DigitalConfig_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True, {}, randint(5, 50))

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
        out_of_bounds,
        # Переопределенные тэги
        tags,
        # Количество потоков
        thread
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = ThreadingGET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
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
                                                                        out_of_bounds=out_of_bounds,
                                                                        tags=tags,
                                                                        thread=thread
                                                                        )

    assert meterdata == []


# # ------------------------------------- ElecticEnergyValues ----------------------------------------------------------
parametrize_ElecticEnergyValues_ArchType_name_list = parametrize_by_element(
    reqest='get',
    ArchType_name_list=ElecticEnergyValues_ArchType_name_list
)


@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags, thread",
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
        out_of_bounds,
        # Переопределенные тэги
        tags,
        # Количество потоков
        thread
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = ThreadingGET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
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
                                                                        out_of_bounds=out_of_bounds,
                                                                        tags=tags,
                                                                        thread=thread
                                                                        )

    assert meterdata == []


# ElecticEnergyValues

@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags, thread",
    [
        (ElecticEnergyValues_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False, {},
         randint(5, 50)),
        (ElecticEnergyValues_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False, {},
         randint(5, 50)),
        (ElecticEnergyValues_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False, {},
         randint(5, 50)),
        (ElecticEnergyValues_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False, {},
         randint(5, 50)),
        (ElecticEnergyValues_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True, {},
         randint(5, 50)),
        (ElecticEnergyValues_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True, {},
         randint(5, 50)),
        (ElecticEnergyValues_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True, {},
         randint(5, 50)),
        (ElecticEnergyValues_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True, {},
         randint(5, 50)),
        (ElecticEnergyValues_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False, {},
         randint(5, 50)),
        (ElecticEnergyValues_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True, {},
         randint(5, 50))

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
        out_of_bounds,
        # Переопределенные тэги
        tags,
        # Количество потоков
        thread
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = ThreadingGET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
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
                                                                        out_of_bounds=out_of_bounds,
                                                                        tags=tags,
                                                                        thread=thread
                                                                        )

    assert meterdata == []


# # ------------------------------------- ElectricQualityValues ------------------------------------------------------
# ElectricQualityValues

@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags, thread",
    [
        (ElectricQualityValues_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False, {},
         randint(5, 50)),
        (ElectricQualityValues_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False, {},
         randint(5, 50)),
        (ElectricQualityValues_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False, {},
         randint(5, 50)),
        (ElectricQualityValues_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False, {},
         randint(5, 50)),
        (ElectricQualityValues_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True, {},
         randint(5, 50)),
        (ElectricQualityValues_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True, {},
         randint(5, 50)),
        (ElectricQualityValues_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True, {},
         randint(5, 50)),
        (ElectricQualityValues_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True, {},
         randint(5, 50)),
        (ElectricQualityValues_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False, {},
         randint(5, 50)),
        (ElectricQualityValues_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True, {},
         randint(5, 50))

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
        out_of_bounds,
        # Переопределенные тэги
        tags,
        # Количество потоков
        thread
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = ThreadingGET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
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
                                                                        out_of_bounds=out_of_bounds,
                                                                        tags=tags,
                                                                        thread=thread
                                                                        )

    assert meterdata == []


#


# # ------------------------------------- ElectricPowerValues --------------------------------------------------------
parametrize_ElectricPowerValues_ArchType_name_list = parametrize_by_element(
    reqest='get',
    ArchType_name_list=ElectricPowerValues_ArchType_name_list)


@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags, thread",
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
        out_of_bounds,
        # Переопределенные тэги
        tags,
        # Количество потоков
        thread
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = ThreadingGET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
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
                                                                        out_of_bounds=out_of_bounds,
                                                                        tags=tags,
                                                                        thread=thread
                                                                        )

    assert meterdata == []


# ElectricPowerValues


@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags, thread",
    [
        (ElectricPowerValues_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False, {},
         randint(5, 50)),
        (ElectricPowerValues_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False, {},
         randint(5, 50)),
        (ElectricPowerValues_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False, {},
         randint(5, 50)),
        (ElectricPowerValues_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False, {},
         randint(5, 50)),
        (ElectricPowerValues_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True, {},
         randint(5, 50)),
        (ElectricPowerValues_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True, {},
         randint(5, 50)),
        (ElectricPowerValues_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True, {},
         randint(5, 50)),
        (ElectricPowerValues_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True, {},
         randint(5, 50)),
        (ElectricPowerValues_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False, {},
         randint(5, 50)),
        (ElectricPowerValues_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True, {},
         randint(5, 50))

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
        out_of_bounds,
        # Переопределенные тэги
        tags,
        # Количество потоков
        thread
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = ThreadingGET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
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
                                                                        out_of_bounds=out_of_bounds,
                                                                        tags=tags,
                                                                        thread=thread
                                                                        )

    assert meterdata == []


# # ------------------------------------- PulseValues -----------------------------------------------------------------
parametrize_PulseValues_ArchType_name = parametrize_by_element(reqest='get',
                                                               ArchType_name_list=PulseValues_ArchType_name_list)


@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags, thread",
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
        out_of_bounds,
        # Переопределенные тэги
        tags,
        # Количество потоков
        thread
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = ThreadingGET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
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
                                                                        out_of_bounds=out_of_bounds,
                                                                        tags=tags,
                                                                        thread=thread
                                                                        )

    assert meterdata == []


# PulseValues


@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags, thread",
    [
        (PulseValues_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False, {}, randint(5, 50)),
        (PulseValues_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False, {}, randint(5, 50)),
        (PulseValues_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False, {}, randint(5, 50)),
        (PulseValues_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False, {}, randint(5, 50)),
        (PulseValues_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True, {}, randint(5, 50)),
        (PulseValues_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True, {}, randint(5, 50)),
        (PulseValues_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True, {}, randint(5, 50)),
        (PulseValues_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True, {}, randint(5, 50)),
        (PulseValues_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False, {}, randint(5, 50)),
        (PulseValues_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True, {}, randint(5, 50))

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
        out_of_bounds,
        # Переопределенные тэги
        tags,
        # Количество потоков
        thread
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = ThreadingGET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
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
                                                                        out_of_bounds=out_of_bounds,
                                                                        tags=tags,
                                                                        thread=thread
                                                                        )

    assert meterdata == []


# ------------------------------------- DigitalValues -----------------------------------------------------------------
parametrize_DigitalValues_ArchType_name = parametrize_by_element(reqest='get',
                                                                 ArchType_name_list=DigitalValues_ArchType_name_list)


@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags, thread",
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
        out_of_bounds,
        # Переопределенные тэги
        tags,
        # Количество потоков
        thread
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = ThreadingGET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
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
                                                                        out_of_bounds=out_of_bounds,
                                                                        tags=tags,
                                                                        thread=thread
                                                                        )

    assert meterdata == []


# DigitalValues


@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags, thread",
    [
        (DigitalValues_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False, {}, randint(5, 50)),
        (DigitalValues_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False, {}, randint(5, 50)),
        (DigitalValues_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False, {}, randint(5, 50)),
        (DigitalValues_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False, {}, randint(5, 50)),
        (DigitalValues_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True, {}, randint(5, 50)),
        (DigitalValues_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True, {}, randint(5, 50)),
        (DigitalValues_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True, {}, randint(5, 50)),
        (DigitalValues_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True, {}, randint(5, 50)),
        (DigitalValues_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False, {}, randint(5, 50)),
        (DigitalValues_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True, {}, randint(5, 50))

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
        out_of_bounds,
        # Переопределенные тэги
        tags,
        # Количество потоков
        thread
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = ThreadingGET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
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
                                                                        out_of_bounds=out_of_bounds,
                                                                        tags=tags,
                                                                        thread=thread
                                                                        )

    assert meterdata == []


# ------------------------------------- JournalValues -----------------------------------------------------------------
parametrize_JournalValues_ArchType_name = parametrize_by_element(reqest='get',
                                                                 ArchType_name_list=JournalValues_ArchType_name_list)


@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags, thread",
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
        out_of_bounds,
        # Переопределенные тэги
        tags,
        # Количество потоков
        thread
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = ThreadingGET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
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
                                                                        out_of_bounds=out_of_bounds,
                                                                        tags=tags,
                                                                        thread=thread
                                                                        )

    assert meterdata == []


# JournalValues

@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags, thread",
    [
        (JournalValues_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False, {}, randint(5, 50)),
        (JournalValues_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False, {}, randint(5, 50)),
        (JournalValues_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False, {}, randint(5, 50)),
        (JournalValues_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False, {}, randint(5, 50)),
        (JournalValues_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True, {}, randint(5, 50)),
        (JournalValues_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True, {}, randint(5, 50)),
        (JournalValues_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True, {}, randint(5, 50)),
        (JournalValues_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True, {}, randint(5, 50)),
        (JournalValues_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False, {}, randint(5, 50)),
        (JournalValues_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True, {}, randint(5, 50))

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
        out_of_bounds,
        # Переопределенные тэги
        tags,
        # Количество потоков
        thread
):
    # Чистим БД

    deleteMeterTable()
    sleep(2)
    meterdata = ThreadingGET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
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
                                                                        out_of_bounds=out_of_bounds,
                                                                        tags=tags,
                                                                        thread=thread
                                                                        )

    assert meterdata == []


#
# # # -------------------------------------   AllTAGS ----------------------------------------------------------------
all_ArchType_name_list = ElectricConfig_ArchType_name_list + ElecticEnergyValues_ArchType_name_list +\
                         ElectricQualityValues_ArchType_name_list + ElectricPowerValues_ArchType_name_list +\
                         PulseValues_ArchType_name_list + DigitalValues_ArchType_name_list + \
                         JournalValues_ArchType_name_list


@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags, thread",
    [
        (all_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False, {}, randint(5, 10)),
        (all_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False, {}, randint(5, 10)),
        (all_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False, {}, randint(5, 10)),
        (all_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False, {}, randint(5, 10)),
        (all_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True, {}, randint(5, 10)),
        (all_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True, {}, randint(5, 10)),
        (all_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True, {}, randint(5, 10)),
        (all_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True, {}, randint(5, 10)),
        (all_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False, {}, randint(5, 10)),
        (all_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True, {}, randint(5, 10))

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
        out_of_bounds,
        # Переопределенные тэги
        tags,
        # Количество потоков
        thread

):
    import time
    time_start = time.time()
    deleteMeterTable()
    sleep(2)
    meterdata = ThreadingGET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
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
                                                                        out_of_bounds=out_of_bounds,
                                                                        tags=tags,
                                                                        thread=thread
                                                                        )

    time_finis = time.time()
    print('ТЕСТ ПРОХОДИЛ :', time_finis - time_start)

    assert meterdata == []
