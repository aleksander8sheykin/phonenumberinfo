rebuild-postgres:
	docker-compose build postgres && docker-compose stop postgres && docker-compose rm -f postgres && docker-compose up -d --force-recreate --no-deps postgres

rebuild-back:
	docker-compose build back && docker-compose stop back && docker-compose rm -f back && docker-compose up -d --force-recreate --no-deps back

rebuild-nginx:
	docker-compose build nginx && docker-compose stop nginx && docker-compose rm -f nginx && docker-compose up -d --force-recreate --no-deps nginx
