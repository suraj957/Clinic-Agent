import autogen
from autogen import register_function
import os
from dotenv import load_dotenv
from backend.tools import check_availability, save_to_db

load_dotenv()
print("KEY:", os.getenv("AZURE_OPENAI_API_KEY"))
print("URL:", os.getenv("AZURE_OPENAI_BASE_URL"))

llm_config = {
    "config_list": [
        {
            "model": os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
            "api_type": "azure",
            "api_key": os.getenv("AZURE_OPENAI_API_KEY", ""),
            "base_url": os.getenv("AZURE_OPENAI_BASE_URL", "https://modana-customer-05.openai.azure.com/"),
            "api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
        }
    ]
}

# def is_termination_msg(message):
#     content = message.get("content", "") or ""
#     return "appointment is booked" in content.lower() or "scheduled" in content.lower()

def run_agents(user_message):

    receptionist_agent = autogen.AssistantAgent(
        name="Receptionist",
        llm_config=llm_config,
        system_message="""
        Extract patient name, date, and time from the user message.
        Output in JSON format: {"name": ..., "date": ..., "time": ...}
        """
    )

    scheduler_agent = autogen.AssistantAgent(
        name="Scheduler",
        llm_config=llm_config,
        system_message="""
        Check availability for the given date and time using the check_availability tool.
        Output 'Available' or 'Not Available'.
        """
    )

    data_agent = autogen.AssistantAgent(
        name="DataAgent",
        llm_config=llm_config,
        system_message="""
        Save the appointment using the save_to_db tool with the patient name, date, and time.
        After saving, reply in a friendly, natural tone like:
        'Hi Suraj, your appointment for tomorrow at 6pm has been successfully booked!'
        Always address the patient by name.
        """
    )

    user_proxy = autogen.UserProxyAgent(
        name="User",
        human_input_mode="NEVER",  # prevents terminal blocking
        code_execution_config=False
        # is_termination_msg= is_termination_msg
    )

    # Proper tool registration
    register_function(
        check_availability,
        caller=scheduler_agent,
        executor=user_proxy,
        name="check_availability",
        description="Check if a time slot is available. Args: date (str), time (str). Returns True if free."
    )

    register_function(
        save_to_db,
        caller=data_agent,
        executor=user_proxy,
        name="save_to_db",
        description="Save appointment to database. Args: name (str), date (str), time (str)."
    )

    groupchat = autogen.GroupChat(
        agents=[user_proxy, receptionist_agent, scheduler_agent, data_agent],
        messages=[],
        max_round=10
    )

    print("Base agents initialized and tools registered.")

    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config=llm_config
    )

    user_proxy.initiate_chat(
        manager,
        message=user_message
    )

    for msg in reversed(groupchat.messages):
        if msg.get("name") == "DataAgent" and msg.get("content"):
            return msg["content"]

    return "Appointment processing completed."