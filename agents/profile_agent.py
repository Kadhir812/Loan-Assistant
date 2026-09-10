import json

from mcp import Client, StdioServerParameters


class ProfileAgent:

    def __init__(self):

        self.server_params = StdioServerParameters(
            command="python",
            args=[
                "-m",
                "mcp_server.server"
            ]
        )

    async def get_customer_profile(
        self,
        customer_id: str
    ) -> dict:

        if not customer_id:
            return {
                "success": False,
                "error_type": "INVALID_CUSTOMER_ID",
                "customer_id": customer_id,
                "message": "Customer ID is required."
            }

        try:

            async with Client(
                self.server_params
            ) as client:

                result = await client.call_tool(
                    "get_customer_profile",
                    {
                        "customer_id": customer_id
                    }
                )


                if not result.content:
                    return {
                        "success": False,
                        "error_type": "EMPTY_MCP_RESPONSE",
                        "customer_id": customer_id,
                        "message": "MCP returned no content."
                    }

                # ---------------------------------
                # Extract TextContent
                # ---------------------------------

                for content_item in result.content:

                    if hasattr(content_item, "text"):

                        text = content_item.text

                        if not text:
                            continue

                        try:

                            profile = json.loads(text)

                            if isinstance(profile, dict):
                                return profile

                        except json.JSONDecodeError:

                            continue

                # ---------------------------------
                # No valid JSON found
                # ---------------------------------

                return {
                    "success": False,
                    "error_type": "INVALID_MCP_RESPONSE",
                    "customer_id": customer_id,
                    "message": "MCP returned content but it was not valid JSON."
                }

        except Exception as error:

            return {
                "success": False,
                "error_type": "MCP_CLIENT_ERROR",
                "customer_id": customer_id,
                "message": str(error)
            }

