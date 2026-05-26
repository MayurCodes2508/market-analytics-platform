# Future Improvements

## Roadmap

The platform is intentionally scoped for `prod_v1`. Future releases should expand reliability, analytics capabilities, and source coverage.

### Planned improvements

- Add retries and backoff for API failures
- Add incremental or delta ingestion for source refreshes
- Add BigQuery or dbt transformation integration
- Add alerting and monitoring dashboards
- Add support for additional execution command types (database, file, streaming)
- Add config versioning and change auditing

## `prod_v2` goals

- Harden production reliability
- Automate downstream warehouse loads
- Improve observability with metrics and alerting
- Support multiple data sources beyond CoinGecko

## Current status

`prod_v1` is the first production delivery. Future versions will extend this foundation into a full analytics pipeline.
