
from mcp.server import MCPServer

from mcp_server.tools import (
    get_customer_profile as fetch_customer_profile
)

from mcp_server.errors import (
    CustomerNotFoundError,
    DatabaseConnectionError,
    DatabaseTimeoutError,
    MCPToolError,
)


mcp = MCPServer("Personal Loan Agent")


@mcp.tool()
def get_customer_profile(customer_id: str) -> dict:
    """
    Retrieve all loan applications associated with a customer.
    """

    try:
        return fetch_customer_profile(customer_id)

    except CustomerNotFoundError as e:
        return {
            "success": False,
            "error_type": "CUSTOMER_NOT_FOUND",
            "customer_id": customer_id,
            "message": str(e),
        }

    except DatabaseTimeoutError as e:
        return {
            "success": False,
            "error_type": "DATABASE_TIMEOUT",
            "customer_id": customer_id,
            "message": str(e),
            "retryable": True,
        }

    except DatabaseConnectionError as e:
        return {
            "success": False,
            "error_type": "DATABASE_CONNECTION_ERROR",
            "customer_id": customer_id,
            "message": str(e),
            "retryable": True,
        }

    except MCPToolError as e:
        return {
            "success": False,
            "error_type": "MCP_TOOL_ERROR",
            "customer_id": customer_id,
            "message": str(e),
            "retryable": False,
        }

    except Exception:
        return {
            "success": False,
            "error_type": "UNKNOWN_ERROR",
            "customer_id": customer_id,
            "message": "An unexpected error occurred.",
            "retryable": False,
        }


if __name__ == "__main__":
    mcp.run()

