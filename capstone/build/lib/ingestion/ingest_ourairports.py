import io
import requests
import pandas as pd
from google.cloud import bigquery

PROJECT_ID = "saudi-aviation-infrastructure"
DATASET_ID = "bronze"

DATASET_URLS = {
    "airports": "https://davidmegginson.github.io/ourairports-data/airports.csv",
    "runways": "https://davidmegginson.github.io/ourairports-data/runways.csv",
    "navaids": "https://davidmegginson.github.io/ourairports-data/navaids.csv",
    "frequencies": "https://davidmegginson.github.io/ourairports-data/airport-frequencies.csv",
    "regions": "https://davidmegginson.github.io/ourairports-data/regions.csv",
    "countries": "https://davidmegginson.github.io/ourairports-data/countries.csv",
}

def get_bigquery_client() -> bigquery.Client:
    return bigquery.Client(project=PROJECT_ID)

def ensure_dataset_exists(client: bigquery.Client, dataset_name: str, location: str = "EU"):
    full_dataset_id = f"{client.project}.{dataset_name}"
    dataset = bigquery.Dataset(full_dataset_id)
    dataset.location = location
    dataset = client.create_dataset(dataset, exists_ok=True)
    print(f" Dataset '{dataset.dataset_id}' ready in location '{location}'.")

def load_table_from_url(client: bigquery.Client, table_name: str, url: str):
    print(f"\n Fetching '{table_name}' from: {url}")
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    # قراءة البيانات مع low_memory=False لضمان عدم وجود تحذيرات على الأعمدة الكبيرة
    df = pd.read_csv(io.StringIO(response.text), low_memory=False)
    print(f"   Downloaded {len(df):,} rows and {len(df.columns)} columns.")

    table_id = f"{client.project}.{DATASET_ID}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        autodetect=True,
    )

    print(f"  ⬆️ Uploading to BigQuery table: {table_id} ...")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()  # انتظار اكتمال الرفع

    table = client.get_table(table_id)
    print(f" Loaded {table.num_rows:,} rows into {table_id}")

def main():
    client = get_bigquery_client()
    print(f"Connected to BigQuery project: {client.project}")
    print(f"Target dataset: {DATASET_ID}")

    ensure_dataset_exists(client, DATASET_ID)

    for table_name, url in DATASET_URLS.items():
        try:
            load_table_from_url(client, table_name, url)
        except Exception as e:
            print(f"❌ Failed to load {table_name}: {e}")

    print("\n Bronze layer ingestion completed successfully!")

if __name__ == "__main__":
    main()
