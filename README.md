## Installation
```
#Build the image
docker build -t predict-travel-cancelled .
```
```
#Run the container
docker run -it -p 8000:8000  predict-travel-cancelled