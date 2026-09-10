
import asyncio

from mcp import Client, StdioServerParameters


async def main():

    server = StdioServerParameters(
        command="python",
        args=["-m", "mcp_server.server"],
    )

    async with Client(server) as client:

        print("Connected to MCP server")

        tools = await client.list_tools()

        print("\nAvailable tools:")

        for tool in tools.tools:
            print("-", tool.name)

        result = await client.call_tool(
            "get_customer_profile",
            {
                "customer_id": "CUST0001"
            }
        )

        print("\nCustomer profile:")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
