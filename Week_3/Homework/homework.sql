-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `dtc-de-course-375011.dezoomcamp.fhv-bucket_data`
OPTIONS (
  format = 'CSV',
  uris = ['gs://de_zoomcamp_bucket_vr/fhv data/fhv_tripdata_2019-*.csv.gz']
);

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE `dtc-de-course-375011.dezoomcamp.fhv-bucket_data-non-partitioned` AS
SELECT * FROM `dtc-de-course-375011.dezoomcamp.fhv-bucket_data`;

-- Question 1 : Count the number of records
SELECT COUNT(*) FROM `dezoomcamp.fhv-bucket_data-non-partitioned`;

-- Question 2.1 Count the distinct affiliated_base_number on external table
SELECT COUNT (DISTINCT affiliated_base_number)  FROM `dtc-de-course-375011.dezoomcamp.fhv-bucket_data`;
-- got 0MB

-- Question 2.2 Count the distinct affiliated_base_number on BQ table
SELECT COUNT (DISTINCT affiliated_base_number)  FROM `dezoomcamp.fhv-bucket_data-non-partitioned`;
-- got 317.94MB

-- Question 3 : How many records have both a blank (null) PUlocationID and DOlocationID in the entire dataset
SELECT COUNT(*) FROM `dezoomcamp.fhv-bucket_data-non-partitioned` WHERE PUlocationID IS NULL AND DOlocationID IS NULL;

-- Question 5.1 : Create partition and clustered table
CREATE OR REPLACE TABLE `dezoomcamp.fhv-bucket_data_partitoned_clustered`
PARTITION BY DATE(pickup_datetime)
CLUSTER BY affiliated_base_number AS
SELECT * FROM `dezoomcamp.fhv-bucket_data-non-partitioned`;

-- Question 5.2 : Request with base table
SELECT DISTINCT affiliated_base_number  FROM `dezoomcamp.fhv-bucket_data-non-partitioned` WHERE pickup_datetime BETWEEN '2019-03-01' AND '2020-03-31';
-- got 647,87MB estimated

-- Question 5.2 : Request with partitioned and clustered table
SELECT DISTINCT affiliated_base_number  FROM `dezoomcamp.fhv-bucket_data_partitoned_clustered` WHERE pickup_datetime BETWEEN '2019-03-01' AND '2020-03-31'
-- got 285,21MB estimated