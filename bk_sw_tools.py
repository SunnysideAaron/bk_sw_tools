import argparse
import sys
from pathlib import Path
from pydoc import locate

from settings_local import SettingsLocal
from bk_db_tools.database import Database
from bk_db_tools.csv_importer import CsvImporter
from bk_db_tools.sql_file_executer import SqlFileExecuter
from bk_db_tools.xlsx_exporter import XlsxExporter
from bk_db_tools.xlsx_importer import XlsxImporter

parser = argparse.ArgumentParser(
    description='Tools for working with Summoners War data.',
    epilog='Enjoy the program! :)')

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument(
    '-es',
    '--executesql',
    type=str,
    metavar='PATH',
    nargs='+',
    help='Executes a sql file, or a folder containing sql files. 2nd argument can be csv or xlsx (default) for SELECT results output.')

group.add_argument(
    '-ic',
    '--importcsv',
    type=str,
    metavar='PATH',
    help='Import csv file, or a folder containing csv files.')

group.add_argument(
    '-ix',
    '--importxlsx',
    type=str,
    metavar='PATH',
    help='Import excel file, or a folder containing xlsx files.')

group.add_argument(
    '-s',
    '--script',
    type=str,
    metavar='FILE',
    nargs='+',
    help='Runs a saved script.')

group.add_argument(
    '-xd',
    '--xlsxdump',
    type=str,
    metavar='TABLE NAME',
    help='Export tables or views to an xlsx data dump file. Uses %% as wildcard. %% for all.')	

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()

if args.executesql:
    db = Database(SettingsLocal)
    sqlFileExecuter = SqlFileExecuter(SettingsLocal, db)
    sqlFileExecuter.do_executions(args.executesql)
    
if args.importcsv:
    db = Database(SettingsLocal)
    csvImporter = CsvImporter(db)
    csvImporter.do_import(args.importcsv)

if args.importxlsx:
    db = Database(SettingsLocal)
    xlsxImporter = XlsxImporter(db)
    xlsxImporter.do_import(args.importxlsx)

if args.script:
    filePath = Path(args.script[0]) 

    if not filePath.is_file():
        print("File not found." )
        sys.exit(1)
    
    #20/80 rule and KISS. simple conversion of file name to class name.
    temp = filePath.stem.split('_')
    className = ''.join(ele.title() for ele in temp)
    
    classLocation = str(filePath.parent).replace('\\', '.')
    classLocation = classLocation + '.' + filePath.stem + '.' + className
    
    scriptClass = locate(classLocation)
    
    #20/80 rule and KISS. Each script will have a runScript method
    if scriptClass is None:
        print('Class not found. Check class name.')
        sys.exit(1)

    db = Database(SettingsLocal)
    script = scriptClass(SettingsLocal, db)
    
    #TODO someday could convert args.script (a list) to actual method paramaters.
    #https://stackoverflow.com/questions/9539921/how-do-i-create-a-python-function-with-optional-arguments
    script.run_script(args.script)
    
if args.xlsxdump:	
    db = Database(SettingsLocal)
    xlsxExporter = XlsxExporter(SettingsLocal, db)
    xlsxExporter.export_tables(args.xlsxdump)
