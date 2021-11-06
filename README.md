# Vietnam Hydrometeorology Observation Map

|  |  |
|:-------------------------:|:-------------------------:|
|<img width="900" alt="screen" src="assets/demo1.png"> | <img width="900" alt="screen" src="assets/demo2.png"> |


## **Installation**
- Download and install postgresql from https://www.postgresql.org/download/
- git clone https://github.com/kaylode/web-based-map.git
- cd web-based-map
- pip install -r requirements.txt

## **How to run**
### **Setup database**
- Follow [this instruction](./src/modules/database/README.md)

### **Start server**
- Configure the server using ```configs/configs.yaml```
- Run server
```
cd src
python app.py
```
- Go to host: http://192.168.100.9:5000/, server will automatically request data from API server when initiated
- Log files will be saved in ```modules/logger/app.log```

## **References**
- https://github.com/python-visualization/folium
- https://vega.github.io/vega-lite/examples/
- https://www.postgresqltutorial.com/postgresql-python/
