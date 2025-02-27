run_processor:
	pipenv run python main.py &
	pipenv run python main.py -p 1 &

debug:
	pipenv run python main.py

debug2:
	pipenv run python main.py -p 1

kill_processor:
	kill $(ps -afe | egrep -i "fsm_processor" | awk '{print $2}')
is_processor_available:
	ps -afe | egrep -i "fsm_processor"
