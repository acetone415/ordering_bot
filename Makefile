.SILENT:
.DEFAULT_GOAL: help

help:
	echo "USAGE"
	echo "  make <commands>"
	echo ""
	echo "AVAILABLE COMMANDS"
	echo "  run		Start the bot"
	echo "  install	Install dependencies"
	echo "  flake		Run flake8"
	echo "  isort		Run isort"

install:
	pip3 install -r requirements.txt

run:
	echo "Bot is running\nTo stop Bot press CTRL-C"
	python3 bot/main.py

isort:
	isort .

flake:
	flake8 .
