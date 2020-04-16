# c19-tracker
An online tracker for the treatment of and the economic impact caused by Covid-19.

## Packages
`flask`, `sqlite3`, and `covid` are required

To install the packages run
```bash
pip install <package>
```

The documentation for `covid` can be found [here](https://ahmednafies.github.io/covid/)

## Data
The data presented includes death, recovery and infection numbers and treatment development

#### Death, Recovery and Infection
This data is scaped by the `covid` package in `scraper.py`
The source is [John Hopkins University API](https://coronavirus.jhu.edu/map.html) by default but can be specified to be [worldometers.info](www.worldometers.info)

#### Treatment
This data is taken from [Milken Institute](https://milkeninstitute.org/covid-19-tracker)
