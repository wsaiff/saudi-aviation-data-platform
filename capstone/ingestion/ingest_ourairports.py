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

client = bigquery.Client(project=PROJECT_ID)

print(f"Connected to BigQuery project: {client.project}")
print(f"Target dataset: {DATASET_ID}")
