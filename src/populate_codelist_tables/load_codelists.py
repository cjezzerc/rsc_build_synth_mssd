import re, sys, time, pyodbc, tomllib

sql_string="""
TRUNCATE TABLE dbo.$(TABLE_NAME);
BULK INSERT dbo.$(TABLE_NAME) 
FROM '$(CODELIST_FILE)' 
WITH (
FIRSTROW = 2,
FIELDTERMINATOR = '\t',
ROWTERMINATOR = '0x0a',
ERRORFILE = '$(ERROR_FILE)',
TABLOCK
);
"""

def run_sql_file(
    cursor=None, sql_text=None, table_name=None, codelist_file=None, error_file=None
):
    sql_text = re.sub(r"\$\(TABLE_NAME\)", table_name, sql_text)
    sql_text = re.sub(r"\$\(CODELIST_FILE\)", codelist_file, sql_text)
    sql_text = re.sub(r"\$\(ERROR_FILE\)", error_file, sql_text)
    print(f"Executing processed version of sql_string:\n{sql_text}")

    t0 = time.time()
    cursor.execute(sql_text)
    print(f"That took {time.time()-t0} seconds")

config = tomllib.load(open(sys.argv[1], "rb"))

connection_string=config["connection_string"]
connection=pyodbc.connect(connection_string)
cursor = connection.cursor()
cursor.execute("SET NOCOUNT ON; SET XACT_ABORT ON;")

run_sql_file(
    cursor=cursor,
    sql_text=sql_string,
    table_name="DiseaseCodelist",
    codelist_file=f"{config["reference_file_directory"]}/{config["disease_codelist_file"]}",
    error_file="/tmp/load_disease_codelist_errors.txt",
)

connection.commit()
connection.close()
