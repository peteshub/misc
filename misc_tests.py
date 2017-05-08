import pandas as pd
from sqlalchemy import create_engine

if __name__ == '__main__':

    f = open("/home/peter/PycharmProjects/misc/test.txt", 'rb')

    header = f.readlines()[3:4][0].split("|")
    l = map(len, header)

    col_tuples = []
    end = 0
    start = 0
    for elem in l:
        end = start + elem
        col_tuples.append((start, end))
        start = end + 1

    df = pd.read_fwf("/home/peter/PycharmProjects/misc/test.txt", colspecs=col_tuples, skiprows=4, names=header,
                     header=None, converters={h: str for h in header})

    # Parameters
    ServerName = "DAVID-THINK"
    Database = "Boost"
    Driver = "driver=SQL Server Native Client 11.0"

    # Create the connection
    engine = create_engine('mssql+pyodbc://' + ServerName + '/' + Database + "?" + Driver)

    df = pd.read_sql_query("SELECT top 5 * FROM data", engine)

