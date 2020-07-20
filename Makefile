run6:
	DAGSTER_VERSION=0.8.6 DAGSTER_PORT=9091 docker-compose -p dagster-0.8.6 up --build
.PHONY: run6

monitor6:
	docker exec -it dagster-086_postgres_1 bash -c 'while true; do psql -U postgres -d postgres -t -c "SELECT sum(numbackends) FROM pg_stat_database;"; sleep 2; done'
.PHONY: monitor6

run7:
	DAGSTER_VERSION=0.8.7 DAGSTER_PORT=9092 docker-compose -p dagster-0.8.7 up --build
.PHONY: run7

monitor7:
	docker exec -it dagster-087_postgres_1 bash -c 'while true; do psql -U postgres -d postgres -t -c "SELECT sum(numbackends) FROM pg_stat_database;"; sleep 2; done'
.PHONY: monitor7

run8:
	DAGSTER_VERSION=0.8.8 DAGSTER_PORT=9093 docker-compose -p dagster-0.8.8 up --build
.PHONY: run8

monitor8:
	docker exec -it dagster-088_postgres_1 bash -c 'while true; do psql -U postgres -d postgres -t -c "SELECT sum(numbackends) FROM pg_stat_database;"; sleep 2; done'
.PHONY: monitor8

clean_dagster:
	docker-compose kill postgres
	docker-compose rm postgres
.PHONY: clean_dagster
