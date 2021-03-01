# Здесь у нас храняться функции которые мы будем дергать для получения settings
from working_directory.Template.Template_MeterTable_db_API import Template_formation_of_settings


# ----------------------------------------------------------------------------------------------------------------------
#                                                   GET
# ----------------------------------------------------------------------------------------------------------------------
def settings_GET_all_table(setting):
    return Template_formation_of_settings.form_settings_request_empty(setting)


# ----------------------------------------------------------------------------------------------------------------------
#                                              GET from MeterTable
# ----------------------------------------------------------------------------------------------------------------------

def ids_GET_MeterTable(ids):
    return Template_formation_of_settings.form_ids_request_MeterTable(ids)

# ----------------------------------------------------------------------------------------------------------------------
#                                              POST from MeterTable
# ----------------------------------------------------------------------------------------------------------------------

def settings_POST_MeterTable(settings):
    return Template_formation_of_settings.form_settings_request_POST_MeterTable(settings)




# ----------------------------------------------------------------------------------------------------------------------
#                                                   PUT from ArchInfo
# ----------------------------------------------------------------------------------------------------------------------

def settings_PUT_ArchInfo(settings):
    return Template_formation_of_settings.form_settings_request_PUT_ArchInfo(settings)


# ----------------------------------------------------------------------------------------------------------------------
#                                             DELETE from MeterTable
# ----------------------------------------------------------------------------------------------------------------------

def ids_DELETE_MeterTable(ids):
    return Template_formation_of_settings.form_ids_request_MeterTable(ids)