from bk_db_tools.settings import Settings

class SettingsLocal(Settings):
    
    #databasePath = "master.db"
    xlsxDataDump = "output/data_dump.xlsx"
    
    #version = "0.2.0"
    #modulePath = "summoners_war_" + version.replace(".", "_") + "/" 
    #databasePath = modulePath + "master.db"
    host = "localhost"
    port = 8080
    #xlsxDataDump = modulePath + "output/data_dump.xlsx"



    # todo are these still being used?
    #sqlPath = modulePath + "output/sql/"
    #sqlXlsxPath = modulePath + "output/sql_xlsx_results/"