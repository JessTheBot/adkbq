from bigquery_agent import create_bigquery_agent

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from google.genai import types as genai_types

import logging


BIGQUERY_PROJECT_ID = "agents-driven-development"
REGION = "us-west1"
DATASET_ID = "movies_agent"
TABLE_ID = "movies"
MODEL_NAME = "gemini-2.5-pro-preview-03-25"

todo_agent = create_bigquery_agent(
    bigquery_project_id=BIGQUERY_PROJECT_ID,
    dataset_id=DATASET_ID,
    table_id=TABLE_ID,
    model_name=MODEL_NAME,
    system_instruction="you are movies recommending agent, in DB you have previouse user preferances of the movies"
)


session_service = InMemorySessionService()


chat_session = session_service.create_session(
    app_name="app_name",
    user_id="adk_user_id",
    session_id="adk_session_id")


runner_instance = Runner(
    agent=todo_agent,
    app_name="app_name",
    session_service=session_service
)

user_content = genai_types.Content(role='user', parts=[genai_types.Part(text="Show me top 3 of my favorite movie")])
final_response_text = ""

for event in runner_instance.run(
    user_id="adk_user_id",
    new_message=user_content,
    session_id="adk_session_id"):

    if event.error_message:
        logging.error(f"ADK Runner Error: {event.error_message}")
        break

    if event.is_final_response() and event.content and event.content.parts:
        text_part = next((part.text for part in event.content.parts if part.text), None)
        print(text_part)
        break
