# 1. cluster init images
# 2. install network
# 3. install pv/pvc
# 4. ...
# 5. push image to docker-hub
# 6. deploy app(not finish, service is not finish)

docker build -f tornado_web_dockerfile --target python-env -t xlalon/python-env .

# docker build -f tornado_web_dockerfile --target tornado_web -t xlalon/tornado_web:`date +%s` .
docker build -f tornado_web_dockerfile --target tornado_web -t xlalon/tornado_web:v0.1.0

docker push xlalon/tornado_web

# problem
# 10.0.2.15:10250 is vm2 enp0s3 addr 2020-8-2
Error from server: error dialing backend: dial tcp 10.0.2.15:10250: i/o timeout
