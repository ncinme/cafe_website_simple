# cafe_website_simple
There are two Flask apps. First, app_api will run at port 5000. Second, app_web will run at port 5800, and will access APIS defined in app_api.

Added Dockerfile and docker-compose.yml - this is an example where two flask apps talks to each other in multi-container set-up through docker network.