"""
This file contains all partial algorithm functions, that are normally executed
on all nodes for which the algorithm is executed.

The results in a return statement are sent to the vantage6 server (after
encryption if that is enabled). From there, they are sent to the partial task
or directly to the user (if they requested partial results).
"""
import pandas as pd
from typing import Any

from vantage6.algorithm.tools.util import info, warn, error
from vantage6.algorithm.tools.decorators import database_connection, OHDSIMetaData

from ohdsi import database_connector
from ohdsi import sqlrender
from ohdsi import common as ohdsi_common

from rpy2.robjects import RS4

@database_connection(types=["OMOP"], include_metadata=True)
def send_sql_person_count(
    connection: RS4, 
    metadata: OHDSIMetaData,
) -> pd.DataFrame:

    info("Sending SQL query to get PERSON table count")
    sql_string = "SELECT COUNT(*) FROM @cdm_schema.person"
    sql = sqlrender.render(sql_string, cdm_schema=metadata.cdm_schema)
    sql = sqlrender.translate(sql, target_dialect="postgresql") ##@TODO: How to get this from the node config? Not in OHDSIMetaData
    
    result = database_connector.query_sql(connection, sql)
    result = ohdsi_common.convert_from_r(result)

    # Return results to the vantage6 server.
    return result.to_json()

@database_connection(types=["OMOP"], include_metadata=True)
def send_sql_table_names(
    connection: RS4, 
    metadata: OHDSIMetaData,
) -> pd.DataFrame:

    info("Sending SQL query to get table names")
    sql_string = "SELECT table_catalog, table_schema, table_name FROM information_schema.tables WHERE table_schema = '@cdm_schema'"
    sql = sqlrender.render(sql_string, cdm_schema=metadata.cdm_schema)
    sql = sqlrender.translate(sql, target_dialect="postgresql") ##@TODO: How to get this from the node config? Not in OHDSIMetaData
    
    result = database_connector.query_sql(connection, sql)
    result = ohdsi_common.convert_from_r(result)

    # Return results to the vantage6 server.
    return result.to_json()