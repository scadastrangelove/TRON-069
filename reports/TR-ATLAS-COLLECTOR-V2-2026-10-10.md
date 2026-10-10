# Collector redesign

Public summary, 10 October 2026.

Stable IDs and explicit service roles replaced name-derived assumptions. A data-driven query catalog, frozen resume plans, selective line refresh and new-snapshot inheritance were added. The shared Count client uses existing Shodan CLI credentials, paces requests, retries transient failures and records errors without substituting zero. Fresh full runs keep timestamped history and synchronize current facts after validation.

Run the current offline test commands in [README.md](../README.md) for reproducible validation.
