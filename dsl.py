import subprocess
from influxdb import InfluxDBClient

output = subprocess.run(
    [
        'ssh',
        '-i',
        '/Users/danielthorpe/.ssh/id_rsa',
        'root@10.187.0.8',
        '/etc/init.d/dsl_control lucistat'
    ],
    capture_output=True
)

metrics = output.stdout.splitlines()

metricdict = {
    "measurement": "DSL",
    "tags": {
        "modem_identifier": "Cambridge"
    },
    "fields": {}
}

for metric in metrics:
    try:
        splitmetric = str(
            metric
        ).replace(
            'b', '', 1
        ).replace(
            "'", ""
        ).split(
            "="
        )
        try:
            metricdict["fields"][splitmetric[0]] = float(
                splitmetric[1].replace(
                    '"',
                    ''
                )
            )
        except:
            metricdict["fields"][splitmetric[0]] =\
                splitmetric[1].replace('"', '')
    except:
        pass


client = InfluxDBClient(
    host='grafana.ad.dantho.xyz',
    port=8086,
    database='modem'
)


client.write_points([metricdict])

