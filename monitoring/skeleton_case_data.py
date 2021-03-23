import json

from utilities.db_helper import execute_sql_query


def get_skeleton_case_data():
    sql_query = """
        SELECT COUNT(*) As TotalCases,
               AVG(DATE_PART('day', NOW()::timestamp - created_date_time::timestamp))::integer As average_days_old,
               LEFT(region, 1) AS region, case_type
        FROM casev2.cases
        WHERE skeleton = 't'
        AND address_invalid = 'f'
        AND receipt_received = 'f'
        AND refusal_received IS NULL
        GROUP BY  LEFT(region, 1), case_type

        UNION ALL

        SELECT COUNT(*) As TotalCases ,
               AVG(DATE_PART('day', NOW()::timestamp - created_date_time::timestamp))::integer As average_days_old,
               'All Regions', case_type
        FROM casev2.cases
        WHERE skeleton = 't'
        AND address_invalid = 'f'
        AND receipt_received = 'f'
        AND refusal_received IS NULL
        GROUP BY case_type

        UNION ALL

        SELECT COUNT(*) As TotalCases ,
               AVG(DATE_PART('day', NOW()::timestamp - created_date_time::timestamp))::integer As average_days_old,
               LEFT(region, 1), 'All Cases'
        FROM casev2.cases
        WHERE skeleton = 't'
        AND address_invalid = 'f'
        AND receipt_received = 'f'
        AND refusal_received IS NULL
        GROUP BY LEFT(region, 1)

        UNION ALL

        SELECT COUNT(*) As TotalCases ,
               AVG(DATE_PART('day', NOW()::timestamp - created_date_time::timestamp))::integer As average_days_old,
               'All regions', 'All Cases'
        FROM casev2.cases
        WHERE skeleton = 't'
        AND address_invalid = 'f'
        AND receipt_received = 'f'
        AND refusal_received IS NULL;
        """

    db_result = execute_sql_query(sql_query)

    for one_result in db_result:
        print(json.dumps({'count': one_result[0], 'average_case_age': one_result[1], 'region': one_result[2],
                          'case_type': one_result[3]}))


if __name__ == "__main__":
    get_skeleton_case_data()
