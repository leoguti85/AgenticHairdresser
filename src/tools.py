from langchain_core.runnables import RunnableLambda
from google_tools.google_calendar import get_free_slots, create_event
from langchain_core.tools import tool
import datetime


def get_free_slots_tool():
    runnable = RunnableLambda(get_free_slots)
    get_free_slots_tool = runnable.as_tool(
        name="get_free_slots",
        description="""Given a time expression such as (tomorrow, next week, after tomorrow), convert it into a datetime data type. 
                        Example, tomorrow means today's date plus one day. 
                        Input should be the one datetime variable starting at 0am. 
                        The tool checks available time slots in google calendar""",
        arg_types={"start_time": datetime.datetime},
    )
    return get_free_slots_tool


def create_event_tool():
    runnable = RunnableLambda(create_event)
    create_event_tool = runnable.as_tool(
        name="create_event",
        description="""Once an appointment has been confirmed by the customer (service, price and date), 
                    create a new event in google calendar.
                    Inputs should be the the date, type of service, customer name, price in euros and duration in seconds.""",
        arg_types={
            "insert_date": str,
            "service": str,
            "customer": str,
            "price": str,
            "duration": int,
        },
    )
    return create_event_tool


@tool
def get_price_tool():
    """
    Get the price of a given service
    Returns:
        str: The service's price in euros
    """

    return """Infer the gender from customer's name. Here prices in euros of the services we propose: 
            Men prices
            - haircut 32 
            - hair coloring 520

            Women prices
            - haircut 81 
            - hair coloring 836
            - brushing 50"""
