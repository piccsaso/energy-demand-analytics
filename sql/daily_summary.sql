SELECT date(timestamp) AS date_utc,
       COUNT(*) AS observed_hours,
       ROUND(AVG(demand_mw), 2) AS mean_demand_mw,
       ROUND(MAX(demand_mw), 2) AS peak_demand_mw
FROM observations
GROUP BY date_utc
ORDER BY date_utc;
