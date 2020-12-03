# uk_tier_data
Scrape data from Wikipedia on the tier of Local Authority interventions in the UK.

** Please note: this routine has been archived and will no longer be updated. 03_12_2020 **

**Data source:** https://en.wikipedia.org/wiki/COVID-19_tier_regulations_in_England

Data and processing logs are located in `output`.

Currently scheduled to scrape data daily (8 AM UTC).

## Using this repository

To access data locally, read data directly from the `output` folder or clone this repository and pull new data updates.

## Local development

Local development requires [`docker`](https://www.docker.com/get-started) and (optionally) [`make`](https://www.gnu.org/software/make/).

This project is based on the [python 3.8.0-slim](https://hub.docker.com/_/python) docker image.

To develop this repository locally, clone and `cd` into the repository.

```{shell}
git clone https://github.com/hamishgibbs/uk_tier_data.git
cd uk_tier_data
```

Build the development image locally with:

```{shell}
make build
```

Enter the container interactively with:

```{shell}
make bash
```

To develop this repository out of the box, please create a `.env` file with the environment variable `PWD`.

```{shell}
# .env
PWD=/path/to/this/repo
```

## Contributions

See a problem with this repo? Please [open an issue](https://github.com/hamishgibbs/uk_tier_data/issues/new). Contributions are welcome.
