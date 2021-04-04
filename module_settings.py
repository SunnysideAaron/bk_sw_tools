class ModuleSettings:
    version = "0.1.0"
    modulePath = "summoners_war_" + version.replace(".", "_") + "/" 
    databasePath = modulePath + "master.db"
    host = "localhost"
    port = 8080
    xlsxDataDump = modulePath + "output/data_dump.xlsx"



    # todo are these still being used?
    #sqlPath = modulePath + "output/sql/"
    #sqlXlsxPath = modulePath + "output/sql_xlsx_results/"