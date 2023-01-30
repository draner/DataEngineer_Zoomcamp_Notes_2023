from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect import tasks
from prefect.tasks import task_input_hash
from datetime import timedelta



# @task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
# Test without the cache for now
@task(retries=3)
def fetch(url: str) -> pd.DataFrame:
    """Fetch data from web."""
    df = pd.read_csv(url)
    return df


@task(log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Clean data."""
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    print(df.head(2))
    print(f"shape: {df.shape}")

    return df


@task(log_prints=True)
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write data to local disk as a parquet file."""
    path = Path(f"data/{color}/{dataset_file}.parquet")
    print(f"Writing {path}")
    df.to_parquet(path)
    return path

@task(log_prints=True)
def write_gcs(path: Path) -> None:
    """Write data to GCS."""
    gcp_cloud_storage_bucket_block = GcsBucket.load("gcs-de-zoomcamp")
    print(f"Writing {path} to GCS")
    #path = Path(path).as_posix()
    gcp_cloud_storage_bucket_block.upload_from_path(from_path= path, to_path= path)
    return

@task(log_prints=True)
def test() -> None: 
    tasks.gcp.storage.GCSUpload.run("foobar")

@flow()
def etl_web_to_gcs(year: int, month: int, color: str) -> None:
    """ETL data from web to GCS."""
    # Download data from web
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean, color, dataset_file)
    write_gcs(path)


@flow()
def etl_parent_flow(month: list[int] = [1,2], year: int = 2021, color: str = "yellow") -> None:
    for m in month:
        etl_web_to_gcs(year, m, color)

if __name__ == "__main__":
    color="yellow"
    months = [1,2,3]
    year=2021
    etl_parent_flow(months, year, color)