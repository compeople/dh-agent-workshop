from fastmcp import FastMCP
import random
import datetime

# Create the MCP instance
mcp = FastMCP(
    name="System Status MCP", instructions="Use this MCP for system status queries."
)

# Mock data for systems
SYSTEMS = [
    "Database",
    "API Gateway",
    "Auth Service",
    "Frontend",
    "Cache",
]


@mcp.tool
def get_systems() -> list[str]:
    """Return a list of available systems."""
    return SYSTEMS


@mcp.tool
def get_system_status(system_name: str) -> dict:
    """Return status info for a given system (availability, last checked, status)."""
    if system_name not in SYSTEMS:
        raise ValueError(f"Unknown system: {system_name}")
    status = random.choice(["OK", "DEGRADED", "ERROR", "MAINTENANCE"])
    available = status == "OK"
    last_checked = datetime.datetime.now().isoformat()
    return {
        "system": system_name,
        "status": status,
        "available": available,
        "last_checked": last_checked,
    }


@mcp.tool
def get_system_errors(system_name: str, limit: int = 5) -> list[dict]:
    """Return log entries for a given system."""
    if system_name not in SYSTEMS:
        raise ValueError(f"Unknown system: {system_name}")
    log_entries = []
    for i in range(limit):
        log_entries.append(
            {
                "timestamp": (
                    datetime.datetime.now()
                    - datetime.timedelta(minutes=i * random.randint(1, 5))
                ).isoformat(),
                "level": random.choice(["ERROR", "WARNING", "INFO"]),
                "message": f"Mock log entry {i+1} for {system_name}",
            }
        )
    return log_entries


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8080)
