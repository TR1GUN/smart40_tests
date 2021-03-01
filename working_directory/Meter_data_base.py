# Здесь расположим тест для проверки поля records  и других проверок дял компонента базы данных
from working_directory.sqlite import execute_command_values_to_write_return_dict, execute_command_to_read_return_dict



# from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes
# ArchTypes_full_list = \
#     Template_list_ArchTypes.JournalValues_ArchType_name_list + \
#     Template_list_ArchTypes.DigitalValues_ArchType_name_list + \
#     Template_list_ArchTypes.PulseValues_ArchType_name_list + \
#     Template_list_ArchTypes.ElectricPowerValues_ArchType_name_list + \
#     Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list + \
#     Template_list_ArchTypes.ElecticEnergyValues_ArchType_name_list + \
#     Template_list_ArchTypes.DigitalConfig_ArchType_name_list + \
#     Template_list_ArchTypes.PulseConfig_ArchType_name_list + \
#     Template_list_ArchTypes.ElectricConfig_ArchType_name_list

class Service:

    def __init__(self):
        pass

    def RecordsCheckUp(self, ArchType_Name: str, Count_records: int):
        """
        Этот Метод нужен для проверки Коректности обработки значений в поле  Records
        :param ArchType_Name:
        :return:
        """
        error = []
        ArchType_Name_tuple = [ArchType_Name]
        # Получаем record_type_id
        record_type_id = execute_command_values_to_write_return_dict(
            command='SELECT Id FROM ArchTypes WHERE Name = (?) ', values=tuple(ArchType_Name_tuple))

        # record_type_id = execute_command_to_read_return_dict(command='SELECT Id FROM ArchTypes WHERE Name = ')
        # Очищаем - Если нет - то выбрасываем ошибку
        try:
            record_type_id = record_type_id[0]['Id']
        except:
            error.append({'error': 'Такого типа данных не существует'})

        # Теперь основная часть тестов:
        if len(error) == 0:
            # # для начала - изменяем нужное количество рекордов
            Count_records_list = [Count_records]
            result = execute_command_values_to_write_return_dict(command='UPDATE ArchInfo SET Records = ( ? ) WHERE '
                                                                         'RecordTypeId = ' + str(record_type_id),
                                                                 values=tuple(Count_records_list))

            # Теперь Генерируем JSON И Получем что нужно

#
# type_list = ArchTypes_full_list
# for i in range (len(type_list)):
#     a = Service().RecordsCheckUp(ArchType_Name=type_list[i], Count_records=10000)
