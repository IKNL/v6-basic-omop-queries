<h1 align="center">
  <br>
  <a href="https://vantage6.ai"><img src="https://github.com/IKNL/guidelines/blob/master/resources/logos/vantage6.png?raw=true" alt="vantage6" width="400"></a>
</h1>

<h3 align=center>
    A Privacy Enhancing Technologies Operations (PETOps) platform
</h3>

--------------------
# Basic OMOP Queries

This vantage6 algorithm sends basic SQL queries to an OMOP database at the node(s). This algorithm can be used to test the infrastructure of your vantage6 network after setting up an OMOP database.

These queries are used to test the database connection from a vantage6 node to verify that the installation is correct and there is some data in the database.

The queries are:
- Count the number of persons in the database
- Return the table names in the database

You can run these queries using the OMOP SQL connection or using the [OHDSI API](https://ohdsi-api.readthedocs.org).

This package has been developed in context of the [BlueBerry](https://euracan.eu/registries/blueberry/) and [IDEA4RC](https://www.idea4rc.eu/) projects.

This algorithm is designed to be run with the [vantage6](https://vantage6.ai)
infrastructure for distributed analysis and learning.

The base code for this algorithm has been created via the
[v6-algorithm-template](https://github.com/vantage6/v6-algorithm-template)
template generator.

## Privacy Gaurds

### Minimum number of records
For the count query, the algorithm can be configured to only return the result if the number of records is above a certain threshold. This is done by setting the `BOQ_MIN_RECORDS` environment variable.

In case the number of records is below the threshold, the algorithm will return a range between 1 and the threshold. Or the range will be 0 to the threshold if the `BOQ_ALLOW_ZERO` environment variable is set.

Default value: 5

### Allow zero to be returned
By default if the number of records is zero, the value zero is returned. This can be changed by setting the `BOQ_ALLOW_ZERO` environment variable.

In case there are zero records in the PERSON table, the algorithm will return a range between 1 and the threshold when `BOQ_ALLOW_ZERO` is set to `false`.

Default value: true

## Build
In order to build its best to use the makefile.

```bash
make image VANTAGE6_VERSION=4.5.3
```
