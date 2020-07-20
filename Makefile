run_good:
	VARIANT=good DAGSTER_PORT=9091 docker-compose -p dagster-good up --build
.PHONY: run_good

monitor_good:
	docker exec -it dagster-good_postgres_1 bash -c 'while true; do psql -U postgres -d postgres -t -c "SELECT sum(numbackends) FROM pg_stat_database;"; sleep 2; done'
.PHONY: monitor_good

run_bad:
	VARIANT=bad DAGSTER_PORT=9092 docker-compose -p dagster-bad up --build
.PHONY: run7

monitor_bad:
	docker exec -it dagster-bad_postgres_1 bash -c 'while true; do psql -U postgres -d postgres -t -c "SELECT sum(numbackends) FROM pg_stat_database;"; sleep 2; done'
.PHONY: monitor7

clean_dagster:
	docker-compose kill postgres
	docker-compose rm postgres
.PHONY: clean_dagster
