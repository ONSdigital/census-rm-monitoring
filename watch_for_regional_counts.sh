while [ 1 ]
do
    python -m monitoring.regional_counts
    sleep 30m
    python -m monitoring.skeleton_case_data
    sleep 30m
done