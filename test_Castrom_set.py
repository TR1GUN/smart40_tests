# def add_tag_ElecticEnergyValues(ElecticEnergyValues):
#     # КАЖДОМУ ЭЛМЕНТУ ПРИСВАИВАЕМ нужные ТЭГИ
#     adding_tag = [{
#         'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
#         'A-1': None, 'R+1': None, 'A+1': None, 'R-1': None,
#         'A+2': None, 'A-2': None, 'R+2': None, 'R-2': None,
#         'A+3': None, 'A-3': None, 'R+3': None, 'R-3': None,
#         'A+4': None, 'A-4': None, 'R+4': None, 'R-4': None,
#     }, {
#         'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
#         'A-1': None, 'R+1': None, 'A+1': None, 'R-1': None,
#         'A+2': None, 'A-2': None, 'R+2': None, 'R-2': None,
#         'A+3': None, 'A-3': None, 'R+3': None, 'R-3': None,
#     }, {
#         'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
#         'A-1': None, 'R+1': None, 'A+1': None, 'R-1': None,
#         'A+2': None, 'A-2': None, 'R+2': None, 'R-2': None,
#     }, {
#         'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
#         'A-1': None, 'R+1': None, 'A+1': None, 'R-1': None,
#     }, {
#         'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
#     },
#
#     ]
#     tag_list = []
#     for rewrite_tag in adding_tag:
#         for element in ElecticEnergyValues:
#             element = list(element)
#
#             element_full = tuple(element + [rewrite_tag])
#             # print(element_full, type(element_full))
#             tag_list.append(element_full)
#
#     return tag_list
#
#
# def add_tag_ElectricPowerValues(ElectricPowerValues):
#     # КАЖДОМУ ЭЛМЕНТУ ПРИСВАИВАЕМ нужные ТЭГИ
#     adding_tag = [{
# 'cTime': None, 'P+': None, 'Q+': None, 'P-': None, 'Q-': None, 'isPart': None, 'isOvfl': None, 'isSummer': None
#                   },
#         {
#             'cTime': None,  'isPart': None, 'isOvfl': None,
#             'isSummer': None
#         },
#         {
#              'P+': None, 'Q+': None, 'P-': None, 'Q-': None
#         }
#
#     ]
#     tag_list = []
#     for rewrite_tag in adding_tag:
#         for element in ElectricPowerValues:
#             element = list(element)
#
#             element_full = tuple(element + [rewrite_tag])
#             # print(element_full, type(element_full))
#             tag_list.append(element_full)
#
#     return tag_list
#
#
# def add_tag_PulseValues(PulseValues):
#     # КАЖДОМУ ЭЛМЕНТУ ПРИСВАИВАЕМ нужные ТЭГИ
#     adding_tag = [{}]
#     tag_list = []
#     for rewrite_tag in adding_tag:
#         for element in PulseValues:
#             element = list(element)
#
#             element_full = tuple(element + [rewrite_tag])
#             # print(element_full, type(element_full))
#             tag_list.append(element_full)
#
#     return tag_list
#
#
# def add_tag_DigitalValues(DigitalValues):
#     # КАЖДОМУ ЭЛМЕНТУ ПРИСВАИВАЕМ нужные ТЭГИ
#     adding_tag = [{}]
#     tag_list = []
#     for rewrite_tag in adding_tag:
#         for element in DigitalValues:
#             element = list(element)
#
#             element_full = tuple(element + [rewrite_tag])
#             # print(element_full, type(element_full))
#             tag_list.append(element_full)
#
#     return tag_list
#
# def add_tag_JournalValues(JournalValues):
#     # КАЖДОМУ ЭЛМЕНТУ ПРИСВАИВАЕМ нужные ТЭГИ
#     adding_tag = [{}]
#     tag_list = []
#     for rewrite_tag in adding_tag:
#         for element in JournalValues:
#             element = list(element)
#
#             element_full = tuple(element + [rewrite_tag])
#             # print(element_full, type(element_full))
#             tag_list.append(element_full)
#
#     return tag_list

from working_directory.Meter_db_data_API import POST, GET
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes
from working_directory.sqlite import deleteMeterTable
from time import sleep
import pytest
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
            [1, 1, {}],
            [2, 3, {}],
            [3, 1, {}],
            [1, 1, {}],
            [2, 3, {}],
            [3, 1, {}]
        ]
    if reqest == 'get':
        template_parametrize = [
            [0, 1, 1, 2, 0, True, False, False, False, False, False, {}],
            [1, 2, 2, 3, 1, False, True, False, False, False, False, {}],
            [2, 3, 3, 4, 2, False, False, True, False, False, False, {}],
            [4, 4, 4, 5, 3, False, False, False, True, False, False, {}],
            [0, 5, 1, 6, 4, False, False, False, True, False, True, {}],
            [1, 4, 2, 5, 3, False, False, True, False, False, True, {}],
            [2, 5, 3, 6, 2, False, True, False, False, False, True, {}],
            [4, 4, 4, 5, 1, True, False, False, False, False, True, {}],
            [2, 3, 3, 4, 0, True, False, False, False, True, False, {}],
            [2, 2, 3, 3, 0, False, True, False, False, True, True, {}]
        ]
    for i in range(len(ArchType_name_list)):
        ArchType_name = [ArchType_name_list[i]]
        for x in range(len(template_parametrize)):
            element = tuple([ArchType_name] + template_parametrize[x])
            parametrize_list.append(element)
    return parametrize_list


# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------
#                                                  GET
# ---------------------------------------------------------------------------------------------------------------------
#
#
# # # ------------------------------------- ElectricQualityValues ---------------------------------------------------------
# # ElectricQualityValues
#
# @pytest.mark.parametrize(
#     "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
#     "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags",
#     [
#         (ElectricQualityValues_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False, {}),
#         (ElectricQualityValues_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False, {}),
#         (ElectricQualityValues_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False, {}),
#         (ElectricQualityValues_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False, {}),
#         (ElectricQualityValues_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True, {}),
#         (ElectricQualityValues_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True, {}),
#         (ElectricQualityValues_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True, {}),
#         (ElectricQualityValues_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True, {}),
#         (ElectricQualityValues_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False, {}),
#         (ElectricQualityValues_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True, {})
#
#     ]
# )
# def test_GET_ElectricQualityValues_meterdata_db(
#         type_connect,
#         # Список из типов данных
#         list_measure,
#         # Сколько таймштампов выбираем
#         select_count_ts,
#         # Сколько айдишников выбираем
#         select_count_id,
#         # Сколько таймштампов генерируем в БД
#         generate_count_ts,
#         # Сколько айдишников генерируем в БД
#         generate_count_id,
#         # Число выбираемых тэгов
#         count_tags,
#         # Булевый маркер -  Селект по внутренему айдишнику
#         select_device_idx,
#         # Булевый маркер - Селект по внешнему айдишнику
#         select_meter_id,
#         # Булевый маркер - Селект по серийнику
#         serial,
#         # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
#         select_id_all,
#         # Булевый маркер - Селект только последнего времени
#         select_last_time,
#         # Булевый маркер - Выход за границы времени что сгенерировали
#         out_of_bounds,
#         # Переопределенные тэги
#         tags
# ):
#     # Чистим БД
#
#     deleteMeterTable()
#     sleep(2)
#     meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
#                                                                select_count_ts=select_count_ts,
#                                                                select_count_id=select_count_id,
#                                                                generate_count_ts=generate_count_ts,
#                                                                generate_count_id=generate_count_id,
#                                                                count_tags=count_tags,
#                                                                select_device_idx=select_device_idx,
#                                                                select_meter_id=select_meter_id,
#                                                                serial=serial,
#                                                                select_id_all=select_id_all,
#                                                                select_last_time=select_last_time,
#                                                                out_of_bounds=out_of_bounds,
#                                                                tags=tags
#                                                                )
#
#     assert meterdata == []
#
#
# #
#
#
# # # ------------------------------------- ElectricPowerValues -----------------------------------------------------------
# parametrize_ElectricPowerValues_ArchType_name_list = parametrize_by_element(
#     reqest='get',
#     ArchType_name_list=ElectricPowerValues_ArchType_name_list)
#
#
# @pytest.mark.parametrize(
#     "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
#     "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags",
#     parametrize_ElectricPowerValues_ArchType_name_list)
# def test_GET_ElectricPowerValues_meterdata_db_by_element(
#         type_connect,
#         # Список из типов данных
#         list_measure,
#         # Сколько таймштампов выбираем
#         select_count_ts,
#         # Сколько айдишников выбираем
#         select_count_id,
#         # Сколько таймштампов генерируем в БД
#         generate_count_ts,
#         # Сколько айдишников генерируем в БД
#         generate_count_id,
#         # Число выбираемых тэгов
#         count_tags,
#         # Булевый маркер -  Селект по внутренему айдишнику
#         select_device_idx,
#         # Булевый маркер - Селект по внешнему айдишнику
#         select_meter_id,
#         # Булевый маркер - Селект по серийнику
#         serial,
#         # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
#         select_id_all,
#         # Булевый маркер - Селект только последнего времени
#         select_last_time,
#         # Булевый маркер - Выход за границы времени что сгенерировали
#         out_of_bounds,
#         # Переопределенные тэги
#         tags
# ):
#     # Чистим БД
#
#     deleteMeterTable()
#     sleep(2)
#     meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
#                                                                select_count_ts=select_count_ts,
#                                                                select_count_id=select_count_id,
#                                                                generate_count_ts=generate_count_ts,
#                                                                generate_count_id=generate_count_id,
#                                                                count_tags=count_tags,
#                                                                select_device_idx=select_device_idx,
#                                                                select_meter_id=select_meter_id,
#                                                                serial=serial,
#                                                                select_id_all=select_id_all,
#                                                                select_last_time=select_last_time,
#                                                                out_of_bounds=out_of_bounds,
#                                                                tags=tags
#                                                                )
#
#     assert meterdata == []
#
#
# # ElectricPowerValues
#
#
# @pytest.mark.parametrize(
#     "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
#     "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags",
#     [
#         (ElectricPowerValues_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False, {}),
#         (ElectricPowerValues_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False, {}),
#         (ElectricPowerValues_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False, {}),
#         (ElectricPowerValues_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False, {}),
#         (ElectricPowerValues_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True, {}),
#         (ElectricPowerValues_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True, {}),
#         (ElectricPowerValues_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True, {}),
#         (ElectricPowerValues_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True, {}),
#         (ElectricPowerValues_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False, {}),
#         (ElectricPowerValues_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True, {})
#
#     ]
# )
# def test_GET_ElectricPowerValues_meterdata_db(
#         type_connect,
#         # Список из типов данных
#         list_measure,
#         # Сколько таймштампов выбираем
#         select_count_ts,
#         # Сколько айдишников выбираем
#         select_count_id,
#         # Сколько таймштампов генерируем в БД
#         generate_count_ts,
#         # Сколько айдишников генерируем в БД
#         generate_count_id,
#         # Число выбираемых тэгов
#         count_tags,
#         # Булевый маркер -  Селект по внутренему айдишнику
#         select_device_idx,
#         # Булевый маркер - Селект по внешнему айдишнику
#         select_meter_id,
#         # Булевый маркер - Селект по серийнику
#         serial,
#         # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
#         select_id_all,
#         # Булевый маркер - Селект только последнего времени
#         select_last_time,
#         # Булевый маркер - Выход за границы времени что сгенерировали
#         out_of_bounds,
#         # Переопределенные тэги
#         tags
# ):
#     # Чистим БД
#
#     deleteMeterTable()
#     sleep(2)
#     meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
#                                                                select_count_ts=select_count_ts,
#                                                                select_count_id=select_count_id,
#                                                                generate_count_ts=generate_count_ts,
#                                                                generate_count_id=generate_count_id,
#                                                                count_tags=count_tags,
#                                                                select_device_idx=select_device_idx,
#                                                                select_meter_id=select_meter_id,
#                                                                serial=serial,
#                                                                select_id_all=select_id_all,
#                                                                select_last_time=select_last_time,
#                                                                out_of_bounds=out_of_bounds,
#                                                                tags=tags
#                                                                )
#
#     assert meterdata == []
#
#
# # # ------------------------------------- PulseValues -----------------------------------------------------------------
# parametrize_PulseValues_ArchType_name = parametrize_by_element(reqest='get',
#                                                                ArchType_name_list=PulseValues_ArchType_name_list)
#
#
# @pytest.mark.parametrize("list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
#     "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags",
#                          parametrize_PulseValues_ArchType_name
#                          )
# def test_GET_PulseValues_meterdata_db_by_element(
#         type_connect,
#         # Список из типов данных
#         list_measure,
#         # Сколько таймштампов выбираем
#         select_count_ts,
#         # Сколько айдишников выбираем
#         select_count_id,
#         # Сколько таймштампов генерируем в БД
#         generate_count_ts,
#         # Сколько айдишников генерируем в БД
#         generate_count_id,
#         # Число выбираемых тэгов
#         count_tags,
#         # Булевый маркер -  Селект по внутренему айдишнику
#         select_device_idx,
#         # Булевый маркер - Селект по внешнему айдишнику
#         select_meter_id,
#         # Булевый маркер - Селект по серийнику
#         serial,
#         # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
#         select_id_all,
#         # Булевый маркер - Селект только последнего времени
#         select_last_time,
#         # Булевый маркер - Выход за границы времени что сгенерировали
#         out_of_bounds,
#         # Переопределенные тэги
#         tags
# ):
#     # Чистим БД
#
#     deleteMeterTable()
#     sleep(2)
#     meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
#                                                                select_count_ts=select_count_ts,
#                                                                select_count_id=select_count_id,
#                                                                generate_count_ts=generate_count_ts,
#                                                                generate_count_id=generate_count_id,
#                                                                count_tags=count_tags,
#                                                                select_device_idx=select_device_idx,
#                                                                select_meter_id=select_meter_id,
#                                                                serial=serial,
#                                                                select_id_all=select_id_all,
#                                                                select_last_time=select_last_time,
#                                                                out_of_bounds=out_of_bounds,
#                                                                tags=tags
#                                                                )
#
#     assert meterdata == []
#
#
# # PulseValues
#
#
# @pytest.mark.parametrize(
#     "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
#     "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags",
#     [
#         (PulseValues_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False, {}),
#         (PulseValues_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False, {}),
#         (PulseValues_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False, {}),
#         (PulseValues_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False, {}),
#         (PulseValues_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True, {}),
#         (PulseValues_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True, {}),
#         (PulseValues_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True, {}),
#         (PulseValues_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True, {}),
#         (PulseValues_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False, {}),
#         (PulseValues_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True, {})
#
#     ]
# )
# def test_GET_PulseValues_meterdata_db(
#         type_connect,
#         # Список из типов данных
#         list_measure,
#         # Сколько таймштампов выбираем
#         select_count_ts,
#         # Сколько айдишников выбираем
#         select_count_id,
#         # Сколько таймштампов генерируем в БД
#         generate_count_ts,
#         # Сколько айдишников генерируем в БД
#         generate_count_id,
#         # Число выбираемых тэгов
#         count_tags,
#         # Булевый маркер -  Селект по внутренему айдишнику
#         select_device_idx,
#         # Булевый маркер - Селект по внешнему айдишнику
#         select_meter_id,
#         # Булевый маркер - Селект по серийнику
#         serial,
#         # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
#         select_id_all,
#         # Булевый маркер - Селект только последнего времени
#         select_last_time,
#         # Булевый маркер - Выход за границы времени что сгенерировали
#         out_of_bounds,
#         # Переопределенные тэги
#         tags
# ):
#     # Чистим БД
#
#     deleteMeterTable()
#     sleep(2)
#     meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
#                                                                select_count_ts=select_count_ts,
#                                                                select_count_id=select_count_id,
#                                                                generate_count_ts=generate_count_ts,
#                                                                generate_count_id=generate_count_id,
#                                                                count_tags=count_tags,
#                                                                select_device_idx=select_device_idx,
#                                                                select_meter_id=select_meter_id,
#                                                                serial=serial,
#                                                                select_id_all=select_id_all,
#                                                                select_last_time=select_last_time,
#                                                                out_of_bounds=out_of_bounds,
#                                                                tags=tags
#                                                                )
#
#     assert meterdata == []
#
#
# # ------------------------------------- DigitalValues -----------------------------------------------------------------
# parametrize_DigitalValues_ArchType_name = parametrize_by_element(reqest='get',
#                                                                  ArchType_name_list=DigitalValues_ArchType_name_list)
#
#
# @pytest.mark.parametrize("list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
#     "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags",
#                          parametrize_DigitalValues_ArchType_name
#                          )
# def test_GET_DigitalValues_meterdata_db_by_element(
#         type_connect,
#         # Список из типов данных
#         list_measure,
#         # Сколько таймштампов выбираем
#         select_count_ts,
#         # Сколько айдишников выбираем
#         select_count_id,
#         # Сколько таймштампов генерируем в БД
#         generate_count_ts,
#         # Сколько айдишников генерируем в БД
#         generate_count_id,
#         # Число выбираемых тэгов
#         count_tags,
#         # Булевый маркер -  Селект по внутренему айдишнику
#         select_device_idx,
#         # Булевый маркер - Селект по внешнему айдишнику
#         select_meter_id,
#         # Булевый маркер - Селект по серийнику
#         serial,
#         # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
#         select_id_all,
#         # Булевый маркер - Селект только последнего времени
#         select_last_time,
#         # Булевый маркер - Выход за границы времени что сгенерировали
#         out_of_bounds,
#         # Переопределенные тэги
#         tags
# ):
#     # Чистим БД
#
#     deleteMeterTable()
#     sleep(2)
#     meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
#                                                                select_count_ts=select_count_ts,
#                                                                select_count_id=select_count_id,
#                                                                generate_count_ts=generate_count_ts,
#                                                                generate_count_id=generate_count_id,
#                                                                count_tags=count_tags,
#                                                                select_device_idx=select_device_idx,
#                                                                select_meter_id=select_meter_id,
#                                                                serial=serial,
#                                                                select_id_all=select_id_all,
#                                                                select_last_time=select_last_time,
#                                                                out_of_bounds=out_of_bounds,
#                                                                tags=tags
#                                                                )
#
#     assert meterdata == []
#
#
# # DigitalValues
#
#
# @pytest.mark.parametrize(
#     "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
#     "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags",
#     [
#         (DigitalValues_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False, {}),
#         (DigitalValues_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False, {}),
#         (DigitalValues_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False, {}),
#         (DigitalValues_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False, {}),
#         (DigitalValues_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True, {}),
#         (DigitalValues_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True, {}),
#         (DigitalValues_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True, {}),
#         (DigitalValues_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True, {}),
#         (DigitalValues_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False, {}),
#         (DigitalValues_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True, {})
#
#     ]
# )
# def test_GET_DigitalValues_meterdata_db(
#         type_connect,
#         # Список из типов данных
#         list_measure,
#         # Сколько таймштампов выбираем
#         select_count_ts,
#         # Сколько айдишников выбираем
#         select_count_id,
#         # Сколько таймштампов генерируем в БД
#         generate_count_ts,
#         # Сколько айдишников генерируем в БД
#         generate_count_id,
#         # Число выбираемых тэгов
#         count_tags,
#         # Булевый маркер -  Селект по внутренему айдишнику
#         select_device_idx,
#         # Булевый маркер - Селект по внешнему айдишнику
#         select_meter_id,
#         # Булевый маркер - Селект по серийнику
#         serial,
#         # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
#         select_id_all,
#         # Булевый маркер - Селект только последнего времени
#         select_last_time,
#         # Булевый маркер - Выход за границы времени что сгенерировали
#         out_of_bounds,
#         # Переопределенные тэги
#         tags
# ):
#     # Чистим БД
#
#     deleteMeterTable()
#     sleep(2)
#     meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
#                                                                select_count_ts=select_count_ts,
#                                                                select_count_id=select_count_id,
#                                                                generate_count_ts=generate_count_ts,
#                                                                generate_count_id=generate_count_id,
#                                                                count_tags=count_tags,
#                                                                select_device_idx=select_device_idx,
#                                                                select_meter_id=select_meter_id,
#                                                                serial=serial,
#                                                                select_id_all=select_id_all,
#                                                                select_last_time=select_last_time,
#                                                                out_of_bounds=out_of_bounds,
#                                                                tags=tags
#                                                                )
#
#     assert meterdata == []
#

# ------------------------------------- JournalValues -----------------------------------------------------------------
parametrize_JournalValues_ArchType_name = parametrize_by_element(reqest='get',
                                                                 ArchType_name_list=JournalValues_ArchType_name_list)


@pytest.mark.parametrize("list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags",
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
        tags
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
                                                               out_of_bounds=out_of_bounds,
                                                               tags=tags
                                                               )

    assert meterdata == []


# JournalValues

@pytest.mark.parametrize(
    "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
    "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags",
    [
        (JournalValues_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False, {}),
        (JournalValues_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False, {}),
        (JournalValues_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False, {}),
        (JournalValues_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False, {}),
        (JournalValues_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True, {}),
        (JournalValues_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True, {}),
        (JournalValues_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True, {}),
        (JournalValues_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True, {}),
        (JournalValues_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False, {}),
        (JournalValues_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True, {})

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
        tags
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
                                                               out_of_bounds=out_of_bounds,
                                                               tags=tags
                                                               )

    assert meterdata == []

#
# # # -------------------------------------   AllTAGS ---------------------------------------------------------------------
# all_ArchType_name_list = ElectricConfig_ArchType_name_list + ElecticEnergyValues_ArchType_name_list + ElectricQualityValues_ArchType_name_list + ElectricPowerValues_ArchType_name_list + PulseValues_ArchType_name_list + DigitalValues_ArchType_name_list + JournalValues_ArchType_name_list
#
#
# @pytest.mark.parametrize(
#     "list_measure , select_count_ts , select_count_id , generate_count_ts , generate_count_id , count_tags , "
#     "select_device_idx , select_meter_id , serial, select_id_all , select_last_time , out_of_bounds, tags",
#     [
#         (all_ArchType_name_list, 0, 1, 1, 2, 0, True, False, False, False, False, False, {}),
#         (all_ArchType_name_list, 1, 2, 2, 3, 1, False, True, False, False, False, False, {}),
#         (all_ArchType_name_list, 2, 3, 3, 4, 2, False, False, True, False, False, False, {}),
#         (all_ArchType_name_list, 4, 4, 4, 5, 3, False, False, False, True, False, False, {}),
#         (all_ArchType_name_list, 0, 5, 1, 6, 4, False, False, False, True, False, True, {}),
#         (all_ArchType_name_list, 1, 4, 2, 5, 3, False, False, True, False, False, True, {}),
#         (all_ArchType_name_list, 2, 5, 3, 6, 2, False, True, False, False, False, True, {}),
#         (all_ArchType_name_list, 4, 4, 4, 5, 1, True, False, False, False, False, True, {}),
#         (all_ArchType_name_list, 2, 3, 3, 4, 0, True, False, False, False, True, False, {}),
#         (all_ArchType_name_list, 2, 2, 3, 3, 0, False, True, False, False, True, True, {})
#
#     ]
# )
# def test_GET_all_ArchType_name_meterdata_db(
#         type_connect,
#         # Список из типов данных
#         list_measure,
#         # Сколько таймштампов выбираем
#         select_count_ts,
#         # Сколько айдишников выбираем
#         select_count_id,
#         # Сколько таймштампов генерируем в БД
#         generate_count_ts,
#         # Сколько айдишников генерируем в БД
#         generate_count_id,
#         # Число выбираемых тэгов
#         count_tags,
#         # Булевый маркер -  Селект по внутренему айдишнику
#         select_device_idx,
#         # Булевый маркер - Селект по внешнему айдишнику
#         select_meter_id,
#         # Булевый маркер - Селект по серийнику
#         serial,
#         # Булевый маркер - Селект с тэгом - все айдишники. Взаимоисключающий
#         select_id_all,
#         # Булевый маркер - Селект только последнего времени
#         select_last_time,
#         # Булевый маркер - Выход за границы времени что сгенерировали
#         out_of_bounds,
#         # Переопределенные тэги
#         tags
#
# ):
#     deleteMeterTable()
#     sleep(2)
#     meterdata = GET(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
#                                                                select_count_ts=select_count_ts,
#                                                                select_count_id=select_count_id,
#                                                                generate_count_ts=generate_count_ts,
#                                                                generate_count_id=generate_count_id,
#                                                                count_tags=count_tags,
#                                                                select_device_idx=select_device_idx,
#                                                                select_meter_id=select_meter_id,
#                                                                serial=serial,
#                                                                select_id_all=select_id_all,
#                                                                select_last_time=select_last_time,
#                                                                out_of_bounds=out_of_bounds,
#                                                                tags=tags
#                                                                )
#
#     assert meterdata == []
