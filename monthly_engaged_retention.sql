SELECT
    registration_month,
    COUNT(time_spent_metrics.user_id) as total_users,
    ROUND(100.0 * SUM(CASE WHEN m1_time_spent >= 30 THEN 1 ELSE 0 END) / COUNT(time_spent_metrics.user_id), 0)::text || '%' AS m1_retention,
    ROUND(100.0 * SUM(CASE WHEN m2_time_spent >= 30 THEN 1 ELSE 0 END) / COUNT(time_spent_metrics.user_id), 0)::text || '%' AS m2_retention,
    ROUND(100.0 * SUM(CASE WHEN m3_time_spent >= 30 THEN 1 ELSE 0 END) / COUNT(time_spent_metrics.user_id), 0)::text || '%' AS m3_retention
FROM
(
    SELECT
        users.user_id,
        TO_CHAR(users.registration_date, 'Mon, YYYY') AS registration_month,
        SUM(CASE WHEN usage_date >= users.registration_date
                 AND usage_date < users.registration_date + INTERVAL '1 month' THEN time_spent ELSE 0 END) AS m1_time_spent,
        SUM(CASE WHEN usage_date >= users.registration_date + INTERVAL '1 month'
                 AND usage_date < users.registration_date + INTERVAL '2 month' THEN time_spent ELSE 0 END) AS m2_time_spent,
        SUM(CASE WHEN usage_date >= users.registration_date + INTERVAL '2 month'
                 AND usage_date < users.registration_date + INTERVAL '3 month' THEN time_spent ELSE 0 END) AS m3_time_spent
    FROM usage
    FULL OUTER JOIN users ON usage.user_id = users.user_id
    GROUP BY users.user_id, users.registration_date
) AS time_spent_metrics
GROUP BY registration_month
ORDER BY TO_DATE(registration_month, 'Mon, YYYY');
