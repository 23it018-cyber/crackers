import pymysql

try:
    conn = pymysql.connect(host='localhost', user='root', password='tiger')
    c = conn.cursor()
    c.execute("CREATE DATABASE IF NOT EXISTS vicky")
    conn.commit()
    conn.close()
    print("Database vicky created/verified successfully as root.")
except Exception as e:
    print(f"Failed as root: {e}")
    try:
        conn = pymysql.connect(host='localhost', user='vicky', password='tiger')
        c = conn.cursor()
        c.execute("CREATE DATABASE IF NOT EXISTS vicky")
        conn.commit()
        conn.close()
        print("Database vicky created/verified successfully as vicky.")
    except Exception as e2:
        print(f"Failed as vicky: {e2}")
