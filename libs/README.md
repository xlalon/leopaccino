
# build docker image & push to docker hub(can k8s only work this way??)

docker build -f tornado_web_dockerfile --target python-env -t xlalon/python-env .

# docker build -f tornado_web_dockerfile --target tornado_web -t xlalon/tornado_web:`date +%s` .
docker build -f tornado_web_dockerfile --target tornado_web -t xlalon/tornado_web:v0.1.0

docker push xlalon/tornado_web

kubectl apply -f tornado-web-deployment.yaml

kubectl delete deploy/tornado-web-deployment

kubectl get svc

kubectl get pod -n default -o wide