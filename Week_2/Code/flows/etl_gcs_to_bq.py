from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp.bigquery import GcpCredentials

@task(log_prints=True, retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Extract data from GCS."""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcp_cloud_storage_bucket_block = GcsBucket.load("gcs-de-zoomcamp")
    gcp_cloud_storage_bucket_block.get_directory(from_path= gcs_path, local_path="data/")
    return Path(f"data/{gcs_path}")

@task(log_prints=True)
def transform(path: Path) -> pd.DataFrame:
    """Transform data."""
    df = pd.read_parquet(path)
    print(f"pre: missing passenger_count: {df['passenger_count'].isna().sum()}")
    df["passenger_count"] = df["passenger_count"].fillna(0)
    print(f"post: missing passenger_count: {df['passenger_count'].isna().sum()}")
    return df


@task(log_prints=True)
def write_bq(df: pd.DataFrame) -> None:
    """Write data to BigQuery."""
    gcp_credentials = GcpCredentials.load("de-zoomcamp-gcp-cred")
    df.to_gbq(destination_table="dezoomcamp.rides",
                project_id="dtc-de-course-375011",
                if_exists="append",
                credentials=gcp_credentials.get_credentials_from_service_account(),
                chunksize=500_000)
    return



@flow()
def etl_gcs_to_bq():
    """ETL data from GCS to BigQuery."""
    # Download data from web
    color = "yellow"
    year = 2021
    month = 1

    path = extract_from_gcs(color, year, month)
    df = transform(path)
    write_bq(df)

if __name__ == "__main__":
    etl_gcs_to_bq()