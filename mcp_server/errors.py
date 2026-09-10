class MCPToolError(Exception):
    """
    Base exception for MCP-related errors.
    """
    pass


class DatabaseConnectionError(MCPToolError):
    """
    Raised when a connection to the SQLite database cannot be established.
    """
    pass


class CustomerNotFoundError(MCPToolError):
    """
    Raised when the requested customer does not exist.
    """
    pass


class DatabaseTimeoutError(MCPToolError):
    """
    Raised when a database operation exceeds the allowed timeout.
    """
    pass