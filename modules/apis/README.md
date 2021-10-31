# Water Level API

- To get data, call API:
```
http://157.245.207.139:8000/api/{camera_id}/history?time={datetime}
```
- Parameters:
  - camera_id = {tvlongdinh, tvmytho}
  - datetime = "%Y-%m-%d-%H-%M-%S"
    

- Json returns
```
{
  "CameraId": {camera_id},
  "Timestamp": "%Y-%m-%dT%H-%M-%S",
  "FTPLink": "...",
  "Reading": {value1},
  "Reading2": {value2},
}
```