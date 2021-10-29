# Web Based Map using Folium

## Installation

- git clone https://github.com/kaylode/web-based-map.git
- cd web-based-map
- pip install -r requirements.txt

## How to run

### Run on local machine

- Run the app

```
python app.py
```

- Go to server: http://127.0.0.1:5000/

- To crawl data and save to database: http://127.0.0.1:5000/request

### Run on docker

- Build docker

```bash
cd this-repo
docker build . -t <username>/<image-name>:<tag> --build-arg USERNAME=guest

# Example

docker build . -t nhtlongcs/web-server:latest --build-arg USERNAME=guest
```

- Run docker

Default port forwarding setting is 5000:5000, you could change it by change parameter in `run-console.sh` and `src/configs/config.yaml`

```bash
sh run_console.sh <username>/<image-name>:<tag>
```

## Water Level API

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

## Visualization

![](./assets/demo.png)

## References

- https://github.com/python-visualization/folium
- https://vega.github.io/vega-lite/examples/
