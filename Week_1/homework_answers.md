# Week 1 Homework

In this homework we'll prepare the environment
and practice with Docker and SQL

## Question 1. Knowing docker tags

- `--iidfile string` Write the image ID to the file

## Question 2. Understanding docker first run

- 3 ( which are pip, setuptools and wheel)

## Question 3. Count records

- 20530

QUERY :

```sql
SELECT count(*) FROM green_taxi_trips gtt
WHERE DATE(lpep_pickup_datetime) = '2019-01-15' 
AND DATE(lpep_dropoff_datetime) = '2019-01-15';
```

## Question 4. Largest trip for each day

- 2019-01-15

QUERY :

```sql
SELECT DATE(lpep_pickup_datetime) as trip_date, MAX(trip_distance) as max_distance
FROM green_taxi_trips gtt 
GROUP BY trip_date
ORDER BY max_distance DESC
LIMIT 1;
```

## Question 5. The number of passengers

- 2: 1282 ; 3: 254

QUERY :

```sql
SELECT COUNT(*)
FROM green_taxi_trips
WHERE DATE(lpep_pickup_datetime) = '2019-01-01'
AND (passenger_count = 2);
```

## Question 6. Largest tip

- Long Island City/Queens Plaza

QUERY :

```sql
SELECT dropoff_zone."Zone", MAX(tip_amount) as max_tip
FROM green_taxi_trips
JOIN zones as pickup_zone ON green_taxi_trips."PULocationID"  = pickup_zone."LocationID" 
JOIN zones as dropoff_zone ON green_taxi_trips."DOLocationID"  = dropoff_zone."LocationID" 
WHERE pickup_zone."Zone" = 'Astoria'
GROUP BY dropoff_zone."Zone" 
ORDER BY max_tip DESC
LIMIT 1;
```
