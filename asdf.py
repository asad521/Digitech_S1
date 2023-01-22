import argparse
from dotenv import load_dotenv
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
load_dotenv()

token = os.getenv("TOKEN")
org = os.getenv("ORG")
url = os.getenv("URL")
bucket = os.getenv("BUCKET")
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
def main(url=url, org=org, bucket=bucket, token=token):
    write_api = client.write_api(write_options=SYNCHRONOUS)
    for value in range(8):
        point = (
            Point("sensor1")
            .tag("type", "temperature")
            .field("reading", value)
        )
    write_api.write(bucket=bucket, org="masadali98@yahoo.com", record=point)
    time.sleep(1)  # separate points by 1 second
    query_api = client.query_api()
    query = """from(bucket: "smart-iot9")
     |> range(start: -10m)
     |> filter(fn: (r) => r._measurement == "sensor1")"""
    tables = query_api.query(query, org="masadali98@yahoo.com")
    # print(tables)
    for table in tables:
        for record in table.records:
            print(record)
