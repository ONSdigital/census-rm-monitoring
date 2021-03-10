while [ 1 ]
do
    python -m monitoring.find_slow_event_processing
    python -m monitoring.action_worker_database_monitor
    python -m monitoring.find_long_running_db_queries
    sleep 59s
done