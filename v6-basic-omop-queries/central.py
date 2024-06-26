"""
This file contains all central algorithm functions. It is important to note
that the central method is executed on a node, just like any other method.

The results in a return statement are sent to the vantage6 server (after
encryption if that is enabled).
"""

import os
import pandas as pd
from typing import Any

from vantage6.algorithm.tools.util import info, warn
from vantage6.algorithm.tools.decorators import algorithm_client
from vantage6.algorithm.client import AlgorithmClient


""" The algorithm has multiple central functions """


@algorithm_client
def get_person_table_count_http(
    client: AlgorithmClient,
    organizations_to_include="ALL",
) -> list[pd.DataFrame]:
    """
    Retrieves PERSON table count from the OMOP database of participating
    organizations.

    Parameters
    ----------
    client : AlgorithmClient
        Interface to the central server. This is supplied by the wrapper.
    organizations_to_include : list[int], optional
        Specifies the organizations to include. If "ALL", includes all
        organizations; otherwise, provide a list of organization IDs.
        Defaults to "ALL".

    Returns
    -------
    list[pd.DataFrame]
        A list of pandas DataFrames containing the results.
    """
    # obtain organizations for which to run the algorithm
    info("Collecting participating organizations")
    organizations = client.organization.list()
    ids = [org["id"] for org in organizations]
    if organizations_to_include != "ALL":
        # check that organizations_to_include is a subset of ids, so we can return
        # a nice error message. The server can also return an error, but this is
        # more user friendly.
        if not set(organizations_to_include).issubset(set(ids)):
            return {
                "msg": "You specified an organization that is not part of the "
                "collaboration"
            }
        ids = organizations_to_include

    # define input parameters for a subtask
    info("Defining input parameters")
    input_ = {"method": "send_http_person_count"}

    # create a subtask for all organizations in the collaboration.
    info("Creating subtask for all organizations in the collaboration")
    task = client.task.create(input_=input_, organizations=ids)
    info(f'Task assigned, id: {task.get("id")}')

    # wait for node to return results of the subtask.
    info("Waiting for results")
    results = client.wait_for_results(task_id=task.get("id"))
    global_count = sum([int(float(result["count"])) for result in results])
    info("Results obtained!")

    # return the final results of the algorithm
    return pd.DataFrame([{"global_count": global_count}], index=["value"]).to_json()


@algorithm_client
def get_person_table_count(
    client: AlgorithmClient,
    organizations_to_include="ALL",
) -> list[pd.DataFrame]:
    """
    Retrieves PERSON table count from the OMOP database of participating
    organizations.

    Parameters
    ----------
    client : AlgorithmClient)
        Interface to the central server. This is supplied by the wrapper.
    organizations_to_include : list[int], optional
        Specifies the organizations to include. If "ALL", includes all
        organizations; otherwise, provide a list of organization IDs.
        Defaults to "ALL".

    Returns
    -------
    list[pd.DataFrame]
        A list of pandas DataFrames containing the results.
    """

    # obtain organizations for which to run the algorithm
    info("Collecting participating organizations")
    organizations = client.organization.list()
    ids = [org["id"] for org in organizations]
    if organizations_to_include != "ALL":
        # check that organizations_to_include is a subset of ids, so we can return
        # a nice error message. The server can also return an error, but this is
        # more user friendly.
        if not set(organizations_to_include).issubset(set(ids)):
            return {
                "msg": "You specified an organization that is not part of the "
                "collaboration"
            }
        ids = organizations_to_include

    # define input parameters for a subtask
    info("Defining input parameters")
    input_ = {"method": "send_sql_person_count"}

    # create a subtask for all organizations in the collaboration.
    info("Creating subtask for all organizations in the collaboration")
    task = client.task.create(input_=input_, organizations=ids)
    info(f'Task assigned, id: {task.get("id")}')

    # wait for node to return results of the subtask.
    info("Waiting for results")
    results = client.wait_for_results(task_id=task.get("id"))
    info("Results obtained!")

    info("Combining results")
    df_per_node = [pd.read_json(result) for result in results]
    count_per_organization = pd.concat(df_per_node, ignore_index=True)
    global_count = count_per_organization["person_count"].sum()

    # return the final results of the algorithm
    return {
        "count_per_organization": count_per_organization.to_json(),
        "global_count": pd.DataFrame(
            [global_count], columns=["global_count"]
        ).to_json(),
    }


@algorithm_client
def get_table_names(
    client: AlgorithmClient,
    organizations_to_include="ALL",
) -> list[pd.DataFrame]:
    """
    Retrieves table names from the OMOP database of participating
    organizations.

    Parameters
    ----------
    client : AlgorithmClient)
        Interface to the central server. This is supplied by the wrapper.
    organizations_to_include : list[int], optional
        Specifies the organizations to include. If "ALL", includes all
        organizations; otherwise, provide a list of organization IDs.
        Defaults to "ALL".

    Returns
    -------
    list[pd.DataFrame]
        A list of pandas DataFrames containing the results.
    """

    # obtain organizations for which to run the algorithm
    info("Collecting participating organizations")
    organizations = client.organization.list()
    ids = [org["id"] for org in organizations]
    if organizations_to_include != "ALL":
        # check that organizations_to_include is a subset of ids, so we can return
        # a nice error message. The server can also return an error, but this is
        # more user friendly.
        if not set(organizations_to_include).issubset(set(ids)):
            return {
                "msg": "You specified an organization that is not part of the "
                "collaboration"
            }
        ids = organizations_to_include

    # define input parameters for a subtask
    info("Defining input parameters")
    input_ = {"method": "send_sql_table_names"}

    # create a subtask for all organizations in the collaboration.
    info("Creating subtask for all organizations in the collaboration")
    task = client.task.create(input_=input_, organizations=ids)
    info(f'Task assigned, id: {task.get("id")}')

    # wait for node to return results of the subtask.
    info("Waiting for results")
    results = client.wait_for_results(task_id=task.get("id"))
    info("Results obtained!")

    df_per_node = [pd.read_json(result) for result in results]
    combined_result = pd.concat(df_per_node, ignore_index=True).to_json()

    table_names_match = all(
        x["TABLE_NAME"]
        .sort_values(ignore_index=True)
        .equals(df_per_node[0]["TABLE_NAME"].sort_values(ignore_index=True))
        for x in df_per_node
    )

    if not table_names_match:
        warn("Table names do not match across organizations")
        for i, df_node in enumerate(df_per_node):
            node_result_sorted = df_node["TABLE_NAME"].sort_values(ignore_index=True)
            result0_sorted = df_per_node[0]["TABLE_NAME"].sort_values(ignore_index=True)
            print(f"Result {i}:")
            print((node_result_sorted == result0_sorted).all())

    # return the final results of the algorithm
    return {
        "table_names": combined_result,
        "table_names_match": pd.DataFrame(
            [table_names_match], columns=["table_names_match"]
        ).to_json(),
    }
