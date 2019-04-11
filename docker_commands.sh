[build]
docker build crawl_service -t crawl_service:0.0.1
docker build templates_service -t templates_service:0.0.1
docker build smarpy -t gateway:0.0.1

[run]
docker run --network dev -d crawl_service:0.0.1
docker run --network dev -d templates_service:0.0.1
docker run  -p 8000:8000 --network dev -d gateway:0.0.1
docker run -d -p 4444:4444 --shm-size=2g selenium/standalone-chrome:3.141.59-mercury
