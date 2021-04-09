from pathlib import Path
from bk_db_tools.csv_importer import CsvImporter
from bk_db_tools.database import Database
from bk_db_tools.sql_file_executer import SqlFileExecuter
from bk_db_tools.xlsx_importer import XlsxImporter
from .import_swarfarm import ImportSwarfarm

class InstallDb: 
    def __init__(self, settings, db):
        self.settings = settings
        self.db = db
    
    def run_script(self, params):
        print ('Deleting current db')
        self.db.close()
        dbPath = Path(self.settings.databasePath)
        dbPath.unlink()
        #and recreate
        self.db = Database(self.settings)        
        
        print ('\nSetting up lookup tabales')
        csvImporter = CsvImporter(self.db)
        csvImporter.do_import('input/csv/lookup_tables')
        
        print ('\nSetting up other sql scripts')
        sqlFileExecuter = SqlFileExecuter(self.settings, self.db)
        sqlFileExecuter.do_executions(['input/sql'])
        
        print ('\nImporting SWARFARM')
        importSwarfarm = ImportSwarfarm(self.settings, self.db)
        importSwarfarm.run_script(params)

        print ('\nSetting up user settings tables')
        xlsxImporter = XlsxImporter(self.db)
        xlsxImporter.do_import('input/settings/s_artifact.xlsx')
        xlsxImporter.do_import('input/settings/s_other.xlsx')
        xlsxImporter.do_import('input/settings/s_tier_list.xlsx')
        