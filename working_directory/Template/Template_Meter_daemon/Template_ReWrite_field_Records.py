# ---------------------------------------------------------------------------------------------------------------------
#                         Здесь расположем класс для реадактирвоания поля RECORDS!!
# ---------------------------------------------------------------------------------------------------------------------
from working_directory.sqlite import execute_command_values_to_write_return_dict, execute_command_to_write_return_dict


class ReWriteFieldRecords:
    """
    ПАМ ПАМ - Здесь расположим наш редактор поля Records в таблице ArchInfo
    """
    measure = ''
    count_records = 0

    def __init__(self, measure: str, count_records: int):
        self.count_records = count_records
        self.measure = measure
        result = self.__rewrite_data_base(self.__select_RecordType_Id_by_measure_name())

    def __rewrite_data_base(self, record_type_id):
        command = 'UPDATE ArchInfo SET Records = ( ? ) WHERE RecordTypeId = ' + str(record_type_id)
        values = []
        values.append(str(int(self.count_records)))
        values = tuple(values)
        result = execute_command_values_to_write_return_dict(command=command,
                                                             values=values)
        return result

    def __select_RecordType_Id_by_measure_name(self):
        # Получаем record_type_id
        record_type_id = execute_command_to_write_return_dict(
            command='SELECT Id FROM ArchTypes WHERE Name = ( ' + str('\'' + self.measure + '\'') + ')'
                                                             )
        return record_type_id[0]['Id']

