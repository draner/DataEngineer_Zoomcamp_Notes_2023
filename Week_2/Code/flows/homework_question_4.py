from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect import tasks



@task(retries=3)
def fetch(url: str) -> pd.DataFrame:
    """Fetch data from web."""
    df = pd.read_csv(url)
    return df


@task(log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Clean data."""
    df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
    df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
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
    path = Path(path).as_posix()
    gcp_cloud_storage_bucket_block.upload_from_path(from_path= path, to_path= path)
    return

@task(log_prints=True)
def test() -> None: 
    tasks.gcp.storage.GCSUpload.run("foobar")

@flow()
def etl_web_to_gcs_q4() -> None:
    """ETL data from web to GCS."""
    # Download data from web
    color = "green"
    year = 2019
    month = 4
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean, color, dataset_file)
    write_gcs(path)

if __name__ == "__main__":
    etl_web_to_gcs()