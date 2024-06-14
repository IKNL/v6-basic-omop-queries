"""
This file contains all partial algorithm functions, that are normally executed
on all nodes for which the algorithm is executed.

The results in a return statement are sent to the vantage6 server (after
encryption if that is enabled). From there, they are sent to the partial task
or directly to the user (if they requested partial results).
"""
import pandas as pd
import numpy as np
from typing import Any

from vantage6.algorithm.tools.util import info, warn, error, get_env_var
from vantage6.algorithm.tools.decorators import database_connection, OHDSIMetaData

from ohdsi import database_connector
from ohdsi import sqlrender
from ohdsi import common as ohdsi_common

from rpy2.robjects import RS4

from .globals import DEFAULT_BOQ_MIN_RECORDS, DEFAULT_ALLOW_ZERO

@database_connection(types=["OMOP"], include_metadata=True)
def send_sql_person_count(
    connection: RS4,
    metadata: OHDSIMetaData,
) -> Any:

    info("Sending SQL query to get PERSON table count")
    sql_string = "SELECT COUNT(*) FROM @cdm_schema.person"
    sql = sqlrender.render(sql_string, cdm_schema=metadata.cdm_schema)
    sql = sqlrender.translate(sql, target_dialect="postgresql") ##@TODO: How to get this from the node config? Not in OHDSIMetaData
    
    df = database_connector.query_sql(connection, sql)
    df = ohdsi_common.convert_from_r(df)

    # Privacy guards
    # Replace too low values with a privacy-preserving value
    ALLOW_ZERO = _convert_envvar_to_bool("BOQ_ALLOW_ZERO", DEFAULT_ALLOW_ZERO)
    PRIVACY_THRESHOLD = _convert_envvar_to_int(
        "BOQ_MIN_RECORDS", DEFAULT_BOQ_MIN_RECORDS
    )

    replace_value = 1 if ALLOW_ZERO else 0
    replace_condition = (
        np.invert(
            (df < PRIVACY_THRESHOLD) & 
            (~df.isnull()) &
            (df != 0))
        if ALLOW_ZERO
        else np.invert(
            (df < PRIVACY_THRESHOLD)) &
            (~df.isnull())
            
    )

    df.where(replace_condition, replace_value, inplace=True)

    BELOW_THRESHOLD_PLACEHOLDER = _get_threshold_placeholder(
        PRIVACY_THRESHOLD, ALLOW_ZERO
    )

    df = df.astype(str).where(
        replace_condition, BELOW_THRESHOLD_PLACEHOLDER
    )
    
    # Cast results to string to ensure they can be read again
    info("Returning results!")
    return df.astype(str).to_json(orient="records")



@database_connection(types=["OMOP"], include_metadata=True)
def send_sql_table_names(
    connection: RS4,
    metadata: OHDSIMetaData,
) -> Any:

    info("Sending SQL query to get table names")
    sql_string = "SELECT table_catalog, table_schema, table_name FROM information_schema.tables WHERE table_schema = '@cdm_schema'"
    sql = sqlrender.render(sql_string, cdm_schema=metadata.cdm_schema)
    sql = sqlrender.translate(
        sql, target_dialect="postgresql"
    )  ##@TODO: How to get this from the node config? Not in OHDSIMetaData

    result = database_connector.query_sql(connection, sql)
    result = ohdsi_common.convert_from_r(result)

    # Return results to the vantage6 server.
    return result.to_json()


def _create_cohort_query(cohort_definition: dict) -> str:
    """
    Creates a cohort query from a cohort definition in JSON format.

    Parameters
    ----------
    cohort_definition: dict
        The cohort definition in JSON format, for example created from ATLAS.

    Returns
    -------
    str
        The cohort query.
    """
    cohort_expression = circe.cohort_expression_from_json(cohort_definition)
    options = circe.create_generate_options(generate_stats=True)
    return circe.build_cohort_query(cohort_expression, options)[0]


def _convert_envvar_to_int(envvar_name: str, default: str) -> int:
    """
    Convert an environment variable to an integer value.

    Parameters
    ----------
    envvar_name : str
        The environment variable name to convert.
    default : str
        The default value to use if the environment variable is not set.

    Returns
    -------
    int
        The integer value of the environment variable.
    """
    envvar = get_env_var(envvar_name, default)
    error_msg = (
        f"Environment variable '{envvar_name}' has value '{envvar}' which cannot be "
        "converted to a positive integer value."
    )
    try:
        envvar = int(envvar)
    except ValueError as exc:
        raise ValueError(error_msg) from exc
    if envvar < 0:
        raise ValueError(error_msg)
    return envvar


def _get_threshold_placeholder(privacy_threshold: int, allow_zero: bool) -> str:
    """
    Get the below threshold placeholder based on the privacy threshold and allow zero flag.

    Parameters
    ----------
    privacy_threshold : int
        The privacy threshold value.
    allow_zero : bool
        The flag indicating whether zero values are allowed.

    Returns
    -------
    str
        The below threshold placeholder.
    """
    if allow_zero:
        if privacy_threshold > 2:
            return f"1-{privacy_threshold-1}"
        else:
            return "1"
    else:
        if privacy_threshold > 1:
            return f"0-{privacy_threshold-1}"
        else:
            return "0"
        

def _convert_envvar_to_bool(envvar_name: str, default: str) -> bool:
    """
    Convert an environment variable to a boolean value.

    Parameters
    ----------
    envvar_name : str
        The environment variable name to convert.
    default : str
        The default value to use if the environment variable is not set.

    Returns
    -------
    bool
        The boolean value of the environment variable.
    """
    envvar = get_env_var(envvar_name, default).lower()
    if envvar in ["true", "1", "yes", "t"]:
        return True
    elif envvar in ["false", "0", "no", "f"]:
        return False
    else:
        raise ValueError(
            f"Environment variable '{envvar_name}' has value '{envvar}' which cannot be"
            " converted to a boolean value. Please use 'false' or 'true'."
        )