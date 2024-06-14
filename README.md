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

I can run these queries using the OMOP SQL connection or using the [OHDSI API](https://ohdsi-api.readthedocs.org).

This package has been developed in contect of the [BlueBerry](https://euracan.eu/registries/blueberry/) and [IDEA4RC](https://www.idea4rc.eu/) projects.

This algorithm is designed to be run with the [vantage6](https://vantage6.ai)
infrastructure for distributed analysis and learning.

The base code for this algorithm has been created via the
[v6-algorithm-template](https://github.com/vantage6/v6-algorithm-template)
template generator.

## Build
In order to build its best to use the makefile.

```bash
make image VANTAGE6_VERSION=4.5.3
```
