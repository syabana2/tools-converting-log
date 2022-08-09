# Convert Log Elasticsearch
CLI apps for convert log elasticsearch to text or json.
Was built using python version 3.9.2.

## Usage
Show a list of flags that can be used:
```
ptyhon main.py -h
```
Output from above command:
```
usage: main.py [-h] [-o [OUTPUT_FILE]] [-t [TYPE_FILE]] log_file_path

positional arguments:
  log_file_path         location filename log, example=var/log/elasticsearch.log

optional arguments:
  -h, --help            show this help message and exit
  -o [OUTPUT_FILE], --output-file [OUTPUT_FILE]
                        output path file, default current path.
  -t [TYPE_FILE], --type-file [TYPE_FILE]
                        type output file, default type Text. option: json|text
```

Convert log elasticsearch to text:
```
python main.py var/log/elasticsearch/elasticsearch-mid.log
```
If log file exist and log successfully converted, the return will be like below:
```
Converting var/log/elasticsearch/elasticsearch-mid.log in output.txt success..
```
The contents of the output.txt file are like this:
```
=========================================================================================================================================================
id: 1
timestamp: 2022-05-14 11:32:21,520
level: DEBUG
component: action.search
server_name: Shinobi Shaw
message: [client_eleeo][0], node[QtbVlmtvQm22lYrGHxylFA], [P], v[2], s[STARTED], a[id=rPcVNBkvQwWOfey6kWwP4A]: Failed to execute [org.elasticsearch.action.search.SearchRequest@4bd744a0] lastShard [true]
error_message: RemoteTransportException[[Shinobi Shaw][172.18.0.2:9300][indices:data/read/search[phase/query]]]; nested: EsRejectedExecutionException[rejected execution of org.elasticsearch.transport.TransportService$4@53b0748e on EsThreadPoolExecutor[search, queue capacity = 1000, org.elasticsearch.common.util.concurrent.EsThreadPoolExecutor@462df1ab[Running, pool size = 7, active threads = 7, queued tasks = 1000, completed tasks = 22126]]];
=========================================================================================================================================================
id: 2
timestamp: 2022-06-19 07:45:07,060
level: WARN
component: transport.netty
server_name: Crimson and the Raven
message: exception caught on transport layer [[id: 0x7634a556, /167.248.133.62:50354 :> /172.18.0.2:9300]], closing connection
error_message: java.io.StreamCorruptedException: invalid internal transport message format, got (5a,47,0,0)
=========================================================================================================================================================
id: 3
timestamp: 2022-06-20 07:26:24,541
level: INFO
component: cluster.metadata
server_name: Crimson and the Raven
message: [read_me] creating index, cause [auto(index api)], templates [], shards [5]/[1], mappings []
error_message:
=========================================================================================================================================================
```
If we want to convert to json and spesific output path, using this command:
```
python main.py var/log/elasticsearch/elasticsearch-mid.log -t json -o var/elasticsearch.json
```
Result if process converting success:
```
Converting var/log/elasticsearch/elasticsearch-mid.log in var/elasticsearch.json success..
```
The contents of the var/elasticsearch.json file are like this:
```
[
    {
        "id": 1,
        "timestamp": "2022-05-14 11:32:21,520",
        "level": "DEBUG",
        "component": "action.search",
        "server_name": "Shinobi Shaw",
        "message": "[client_eleeo][0], node[QtbVlmtvQm22lYrGHxylFA], [P], v[2], s[STARTED], a[id=rPcVNBkvQwWOfey6kWwP4A]: Failed to execute [org.elasticsearch.action.search.SearchRequest@4bd744a0] lastShard [true]",
        "error_message": "RemoteTransportException[[Shinobi Shaw][172.18.0.2:9300][indices:data/read/search[phase/query]]]; nested: EsRejectedExecutionException[rejected execution of org.elasticsearch.transport.TransportService$4@53b0748e on EsThreadPoolExecutor[search, queue capacity = 1000, org.elasticsearch.common.util.concurrent.EsThreadPoolExecutor@462df1ab[Running, pool size = 7, active threads = 7, queued tasks = 1000, completed tasks = 22126]]];"
    },
    {
        "id": 2,
        "timestamp": "2022-06-19 07:45:07,060",
        "level": "WARN",
        "component": "transport.netty",
        "server_name": "Crimson and the Raven",
        "message": "exception caught on transport layer [[id: 0x7634a556, /167.248.133.62:50354 :> /172.18.0.2:9300]], closing connection",
        "error_message": "java.io.StreamCorruptedException: invalid internal transport message format, got (5a,47,0,0)"
    },
    {
        "id": 3,
        "timestamp": "2022-06-20 07:26:24,541",
        "level": "INFO",
        "component": "cluster.metadata",
        "server_name": "Crimson and the Raven",
        "message": "[read_me] creating index, cause [auto(index api)], templates [], shards [5]/[1], mappings []",
        "error_message": ""
    }
]
```

You can see the example elasticsearch log file in var/log/elasticsearch.log and output.txt and output.json it's a result converted log file.
