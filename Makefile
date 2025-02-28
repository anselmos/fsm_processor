run_processor:
	pipenv run python main.py -kafka 1 &
	pipenv run python main.py -kafka 1 -p 1 &

debug:
	pipenv run python main.py -kafka 1

debug2:
	pipenv run python main.py -kafka 1 -p 1

kill_processor:
	kill $(ps -afe | egrep -i "fsm_processor" | awk '{print $2}')
is_processor_available:
	ps -afe | egrep -i "fsm_processor"

without_kafka:
	pipenv run python main.py