To  create container with postgresDB:

sudo docker run --name qurry_db  -d -p 5432:5432 -e POSTGRES_PASSWORD=1234 postgres:alpine


To check whether server is listening on port:

ss -nlt | grep 5432
