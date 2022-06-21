compose_file := docker-compose.yml
compose := docker compose -f $(compose_file)
tail := 1000
service := web     # defaul service is web

up:
	sudo $(compose) up -d

up_build:
	sudo $(compose) up --build -d

up_web:
	sudo $(compose) up -d web

up_service:
	sudo $(compose) up -d $(service)

up_service_build:
	sudo $(compose) up --build -d $(service)

stop:
	sudo $(compose) stop

down:
	sudo $(compose) down

ps:
	sudo $(compose) ps

logs:
	sudo $(compose) logs --timestamps --tail $(tail) -f $(service)

shell:
	sudo $(compose) exec web python manage.py shell_plus


make_all_migrations:
	sudo $(compose) exec web python manage.py makemigrations payments rates wallet_generator payment_requests

migrate_all:
	sudo $(compose) exec web python manage.py migrate

pull:
	sudo $(compose) pull