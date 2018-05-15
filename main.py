import pymysql, sys, logging, datetime, json
from os import getenv

rds_host = "devlambda-cluster.cluster-cigrydi9davg.eu-west-1.rds.amazonaws.com"
username = "walid"
password = "password123"
dbname = "web"
logger = logging.getLogger()
logger.setLevel(logging.INFO)
try:
    conn = pymysql.connect(rds_host, user=username,
                           passwd=password, db=dbname, connect_timeout=5, autocommit=True)
except:
    logger.error("ERROR: Could not connect to MySql instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")
a = {"requestContext": {"identity": {"sourceIp": "192.158.125", "userAgent": "chrome"}}}


def handler(event,context):
    rs = dict()
    req_time = datetime.datetime.now()
    user_ip = event['requestContext']['identity']['sourceIp']
    user_agent = event['requestContext']['identity']['userAgent']
    with conn.cursor() as cur:
        cur.execute("INSERT INTO Connections (User_ip,User_agent,Request_date) VALUES (%s,%s,%s)",
                    (user_ip, user_agent, req_time))
    rs['user_ip'] = user_ip
    rs['user_agent'] = user_agent
    rs['req_time'] = str(req_time)
    return json.dumps(rs)

def handler2(event, context):
    result = []
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM Connections")
        for row in cur.fetchall():
            rs = {"id": row[0], "user_ip": row[1], "user_agent": row[2], "req_time": str(row[3])}
            result.append(rs)
    return json.dumps(result)

print(handler2(None,None))