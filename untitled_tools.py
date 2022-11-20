import pandas as pd
import easygui

global __passwd__


########################################################################################
# Helper Functions
########################################################################################


def _datatype_mapper_(string: str) -> str:
    """
    Mapping Python Data Types to Teradata Data Types

    :param string: Python Data Type
    :return: Teradata Data Type
    """
    string = string.lower()

    if "int" in string or "bool" in string:
        result = "bigint"

    elif "date" in string:
        result = "date"

    elif "float" in string:
        result = "decimal(32,8)"

    else:
        result = "varchar(32)"

    return result.upper()


########################################################################################
# Actual toolkit functions
########################################################################################


def generate_create_query(
    input_dataframe: pd.DataFrame, schema: str, table_name: str
) -> str:
    """
    Generates the SQL-query based on a DataFrame.

    :param input_dataframe: DataFrame for upload
    :param schema: Target schema in Teradata
    :param table_name: Target table name in Teradata
    :return: The Create Query
    """
    df_meta = pd.DataFrame(input_dataframe.dtypes).reset_index().astype(str)
    df_meta.columns = ["columnname", "python_dtype"]

    df_meta.loc[:, "teradata_dtype"] = df_meta.python_dtype.str.lower().map(
        lambda x: _datatype_mapper_(x)
    )
    print(df_meta)

    primary_index = ", ".join(
        [x for x in df_meta.columnname if "id" in x or "class" in x]
    )
    print(f"\nPrimary Index: {primary_index}")

    query = (
        f"create set table {schema}.{table_name} , no fallback ("
        + ", ".join(list(df_meta.columnname + " as " + df_meta.teradata_dtype))
        + f") primary index({primary_index});"
    )
    return query


########################################################################################
def run_sql_query(user: str, query: str) -> None:
    pass


########################################################################################


def insert_dataframe(
    input_dataframe: pd.DataFrame, schema: str, table_name: str, user: str
) -> None:
    """
    Upload values from a dataframe via insert-statement into a DWH table.

    :param input_dataframe: DataFrame chosen for upload
    :param schema: Target schema in Teradata
    :param table_name: Target table name in Teradata
    :return: Nothing
    """
    __passwd__ = easygui.passwordbox(
        msg=f"Please enter password for [{user}].", title=f"Teradata Password Box"
    )

    pass


########################################################################################


def test_function() -> None:
    return None
