# elysium
Project Management

brew install flyctl
fly launch
fly deploy
https://fly.io/apps/elysium-sparkling-fire-215
https://elysium-sparkling-fire-215.fly.dev
https://elysium-sparkling-fire-215.fly.dev/docs

sudo docker build -t elysium .
docker run -d --name elysium_cont -p 80:80 elysium

http://127.0.0.1
http://127.0.0.1/docs

Create Github repo
Make app on FastAPI https://fastapi.tiangolo.com/deployment/docker/#deploy-the-container-image
Deploy on fly.io
Make db on AWS
Make .env, add `python-dotenv` into `requirements.txt` https://pypi.org/project/python-dotenv/
Make .gitignore
Bc deploying on file, use fly secrets CLI `fly secrets set DB_USER=xxx DB_PASSWORD=xxx DB_HOST=xxx DB_PORT=xxx DB_NAME=xxx`
Import `psycopg` package to connect to DB
Add security rule on AWS