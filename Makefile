run_processor:
	pipenv run python main.py &
	pipenv run python main.py -p 1 &

debug:
	pipenv run python main.py

debug2:
	pipenv run python main.py -p 1
