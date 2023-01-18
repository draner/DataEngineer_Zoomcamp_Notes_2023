# Week 1 Homework

In this homework we'll prepare the environment
and practice with Docker and SQL

## Question 1. Knowing docker tags

Run the command to get information on Docker

```docker --help```

Now run the command to get help on the "docker build" command

Which tag has the following text? - *Write the image ID to the file*

- `--iidfile string`

## Question 2. Understanding docker first run

Run docker with the python:3.9 image in an iterative mode and the entrypoint of bash.
Now check the python modules that are installed ( use pip list).
How many python packages/modules are installed?

- 3

## Question 3. Count records

How many taxi trips were totally made on January 15?

Tip: started and finished on 2019-01-15.

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 20530

QUERY :

```sql
SELECT count(*) FROM green_taxi_trips gtt
WHERE DATE(lpep_pickup_datetime) = '2019-01-15' 
AND DATE(lpep_dropoff_datetime) = '2019-01-15';
```

## Question 4. Largest trip for each day

Which was the day with the largest trip distance
Use the pick up time for your calculations.

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

In 2019-01-01 how many trips had 2 and 3 passengers?

- 2: 1282 ; 3: 254

QUERY :

```sql
SELECT COUNT(*)
FROM green_taxi_trips
WHERE DATE(lpep_pickup_datetime) = '2019-01-01'
AND (passenger_count = 2);
```

## Question 6. Largest tip

For the passengers picked up in the Astoria Zone which was the drop up zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

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
