import configparser
import pyodbc
from datetime import date
from datetime import datetime
from datetime import timedelta


class DataExport:

    def __init__(self):
        config = configparser.ConfigParser()
        config.sections()
        config.read('auto.ini')

        database = config.get("db", "database")
        host = config.get("db", "host")
        username = config.get("db", "user")
        password = config.get("db", "pwd")
        machine_code = config.get("export", 'machine_code')
        output_suffix = config.get("export", 'output_suffix')
        start_hour = config.getint("export", "start_hour")

        print("%s,%s,%s,%s" % (database, host, username, password))
        d = timedelta(days=1)
        today = date.today()
        yesterday = today - d
        start_date = datetime(yesterday.year, yesterday.month, yesterday.day, start_hour, 0, 0)
        end_date = datetime(today.year, today.month, today.day, start_hour, 0, 0)
        print("[INFO] Start to export records. {} -> {}".format(start_date, end_date))

        connection_url = 'DRIVER={SQL Server};DATABASE=%s;SERVER=%s;UID=%s;PWD=%s' % (
            database, host, username, password)
        connection = pyodbc.connect(connection_url)
        cursor = connection.cursor()
        result = cursor.execute('''select cardNumber,inTime,outTime from PassRecord where 
        reserve4!='临时车牌' and (intime between  ? and ? or outTime between  ? and ?)''', start_date, end_date, start_date,
                                end_date)

        output_file = output_suffix + today.strftime("%Y%m%d") + ".txt"
        f = open(output_file, 'w')
        output_format = "{}{}{}"
        for row in result:
            print(row)
            card_number = row[0]
            in_time = row[1]
            # format 02201803071001380001602237
            if in_time:
                in_time_str = in_time.strftime("%Y%m%d%H%M%S")
                out = output_format.format(machine_code, in_time_str, card_number)
                f.write(out)
                f.write("\n")

            out_time = row[2]
            if out_time:
                out_time_str = out_time.strftime("%Y%m%d%H%M%S")
                out = output_format.format(machine_code, out_time_str, card_number)
                f.write(out)
                f.write("\n")

        f.close()
        print("[INFO] end to export records....")


if __name__ == '__main__':
    export = DataExport()
