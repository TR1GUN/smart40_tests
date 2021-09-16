from working_directory.Connect.JSON_format_coding_decoding import code_JSON
import write_file


# //-------------------------------------------------------------------------------------------------------------------
#                                   Класс Записи в директорию Виртуального счетчика
# //-------------------------------------------------------------------------------------------------------------------


class RecordFromEmulatorMeter:
    """
    Класс который Переводит наш JSON формат который кушает наш эмулятор счетчика
    """

    JSON_record = {}

    def __init__(self, JSON_list):


        self.JSON_record = {"vals":  []}
        # Итак - что мы делаем - Мы составляем огромный JSON о всеми возможными значениями -
        # если значение моментое - делаем на это скидку

        for i in range(len(JSON_list)):
            JSON = JSON_list[i]


            if JSON['data'] is not None:
                vals = JSON['data']['measures'][0]['devices'][0]['vals']

                type_vals = JSON['data']['measures'][0]['type']

                for x in range(len(vals)):
                    vals[x]['type'] = type_vals
                    self.JSON_record["vals"].append(vals[x])

            # А Теперь берем и перезаписываем все наши значения

        JSON_meter_value = self.JSON_record
        # Теперь все это упаковываем в JSON и сохраняем
        JSON_meter_value = code_JSON(JSON_meter_value)

        write_file.write_file_JSON_on_Emulator(writen_text=JSON_meter_value)

    def GET_Record(self):
        """
        метод возращает все
        :return:
        """
        return self.JSON_record
