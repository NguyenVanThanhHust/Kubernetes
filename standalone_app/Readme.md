This is a sample to deploy standalone app in Kubernetes

docker build -t fast_api_img .

docker run -p 8000:80 fast_api_img:latest