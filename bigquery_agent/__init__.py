
from .bigquery_helper import BigQueryHelper
from google.adk.agents import LlmAgent 


SYSTEM_INSTRUCTION_INJECTION = """
You are an assistant that helps to query data from a BigQuery database.
You have access to the tools required for this.

When using the tool to query:

- **SQL Syntax:**  You MUST generate valid BigQuery SQL.
- **String Literals:** String literals in SQL queries MUST be enclosed in single quotes (').  Do NOT use backslashes (\) to escape characters within SQL string literals unless specifically needed for a special character inside the string (e.g., a single quote within the string itself should be escaped as '').
- **Table and Column Names:** If table or column names contain special characters or are reserved keywords, enclose them in backticks (`).
- **Example**
    -  To query for a run_id of "abc-123", the SQL should be: `SELECT * FROM my_table WHERE run_id = 'abc-123'`
    - **Do not use** double backslashes: `SELECT * FROM my_table WHERE run_id = \\'abc-123\\'`
- **Do not** use excessive backslashes. Only use them when necessary to escape special characters within a string literal according to BigQuery SQL rules.
- **BEFORE** doing any query make sure that you have checked table name by calling get_table_ref and schema from get_schema to make sure that you have constracted the correct SQL
- **UNLESSS** user is asking about SQL query to show, your main goal is to answer the question and not to show the SQL query, do not respond with the query you want to execute - try to get to the answer (unless you got the error and do not know how to proceed)

When generating SQL queries, be concise and avoid unnecessary clauses or joins unless explicitly requested by the user.

Always return results in a clear and human-readable format. If the result is a table, format it nicely.
"""


def create_bigquery_agent(
    bigquery_project_id: str,
    dataset_id: str,
    table_id: str,
    model_name:str = "gemini-2.5-pro-preview-03-25",
    system_instruction: str = "",
    bq_credentials = None,
    max_byte_limit_per_query = 0
):
    """
    Creates and returns an agent initialized with functions from BigQueryHelper 
    that can interact with a specific BigQuery table.

    :param bigquery_project_id: GCP project ID for BigQuery.
    :param dataset_id: BigQuery dataset ID.
    :param table_id: BigQuery table ID.
    :param model_name: The Vertex AI model name to be used by the agent.
    :param system_instruction: Instruction message.
    :param bq_credentials: credentials that will be used with BigQuery
    :param max_byte_limit_per_query: the query will NOT be executed if this value is set and estimates is exceeds it
    :return: An agent instance configured to query the specified BigQuery table.
    """

    # Initialize the BigQuery helper with the bigquery_project_id
    helper = BigQueryHelper(
        project_id=bigquery_project_id,
        dataset_id=dataset_id,
        table_id=table_id,
        credentials=bq_credentials,
        max_byte_limit_per_query=max_byte_limit_per_query
    )

    # Define the agent with helper's functions
    all_tools = [helper.get_schema, helper.run_query, helper.get_table_ref]

    # Prepend prompt to the system_instruction
    updated_system_instruction = f"""{SYSTEM_INSTRUCTION_INJECTION}. {system_instruction}""".strip()

    return LlmAgent(
        # LiteLLM knows how to connect to a local Ollama server by default
        # model=LiteLlm(model="ollama/llama3.3"), # Standard LiteLLM format for Ollama
        model=model_name,
        name="bigquery_agent",
        instruction=updated_system_instruction,
        tools=all_tools
        # ... other agent parameters
    )
