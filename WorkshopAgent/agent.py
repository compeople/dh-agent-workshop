from google.adk import Agent
from google.adk.tools import ToolContext


def get_weather_in_city(city: str, tool_context: ToolContext):
    if city.lower() == 'berlin' or city.lower() == 'bn':
        return {"status": "success",
                "message": "it's nice and sunny in Berlin, 38 degrees Celcius."}
    return {
        "status": "success",
        "message": f"Cloudy and 15 degrees Celcius in {city}"
    }


root_agent = Agent(
    model="gemini-2.5-flash",
    name="WeatherAgent",
    description="Agent to get weather information",
    instruction="You are an helpful, friendly assistant and help the user to get information about the weather in different cities.",
    before_model_callback=[],
    after_model_callback=[],
    before_agent_callback=[],
    after_agent_callback=[],
    sub_agents=[],
    tools=[get_weather_in_city],

)
