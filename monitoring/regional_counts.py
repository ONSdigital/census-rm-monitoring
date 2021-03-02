import json

from utilities.db_helper import execute_sql_query

if __name__ == "__main__":
    sql_query = """
SELECT CASE counts.region
           WHEN 'E' THEN 'England'
           WHEN 'W' THEN 'Wales'
           WHEN 'N' THEN 'Northern Ireland'
           ELSE 'Unknown Region: ' || counts.region END,
       counts.region_count
FROM (SELECT LEFT(c.region,1) as region, COUNT(*) AS region_count
      FROM casev2.event e, casev2.uac_qid_link q, casev2.cases c
      WHERE e.event_type='RESPONSE_RECEIVED' AND e.uac_qid_link_id = q.id AND q.caze_case_id = c.case_id
      AND c.action_plan_id = 'c4415287-0e37-447b-9c3d-1a011c9fa3db' GROUP BY LEFT(c.region,1)) AS counts
    """

    db_result = execute_sql_query(sql_query)

    regional_counts = dict(db_result)
    regional_counts['Total'] = sum(regional_counts.values())
    print(json.dumps(regional_counts))
