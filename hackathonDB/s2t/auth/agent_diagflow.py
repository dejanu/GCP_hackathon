


import argparse
import uuid

from google.cloud.dialogflowcx_v3beta1.services.agents import AgentsClient
from google.cloud.dialogflowcx_v3beta1.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3beta1.types import session
import sys

#projects/hack-disability3/locations/europe-west1/agents/1083352c-a68b-403c-9b7e-a5ef704e7863

def run_sample():
    # (developer): Replace these values when running the function
    project_id = "hack-disability3"
    # For more information about regionalization see https://cloud.google.com/dialogflow/cx/docs/how/region
    location_id = "europe-west1"
    # For more info on agents see https://cloud.google.com/dialogflow/cx/docs/concept/agent
    agent_id = "1083352c-a68b-403c-9b7e-a5ef704e7863"
    agent = f"projects/{project_id}/locations/{location_id}/agents/{agent_id}"
    # For more information on sessions see https://cloud.google.com/dialogflow/cx/docs/concept/session
    session_id = uuid.uuid4()
    #texts = ["Hello"]
    texts = ["create cluster"]
    # For more supported languages see https://cloud.google.com/dialogflow/es/docs/reference/language
    language_code = "en-us"

    detect_intent_texts(agent, session_id, texts, language_code)


def detect_intent_texts(agent, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_path = f"{agent}/sessions/{session_id}"
    print(f"Session path: {session_path}\n")
    client_options = None
    agent_components = AgentsClient.parse_agent_path(agent)
    location_id = agent_components["location"]
    if location_id != "global":
        api_endpoint = f"{location_id}-dialogflow.googleapis.com:443"
        print(f"API Endpoint: {api_endpoint}\n")
        client_options = {"api_endpoint": api_endpoint}
    session_client = SessionsClient(client_options=client_options)

    for text in texts:
        text_input = session.TextInput(text=text)
        query_input = session.QueryInput(text=text_input, language_code=language_code)
        request = session.DetectIntentRequest(
            session=session_path, query_input=query_input
        )
        response = session_client.detect_intent(request=request)

        print("=" * 20)
        print(f"Query text: {response.query_result.text}")
        response_messages = [
            " ".join(msg.text.text) for msg in response.query_result.response_messages
        ]
        print(f"Response text: {' '.join(response_messages)}\n")



if __name__ == "__main__":
    run_sample()