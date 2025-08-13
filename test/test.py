from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession
import asyncio
import json

server = StdioServerParameters(
    command='apollo-io-mcp',  # Replace with the actual path to your Python interpreter
    args=[
    ],
    env={
        "APOLLO_API_KEY": "your_apollo_api_key_here",  # Replace with your actual Apollo API key
    }
)


async def main():
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            try:
                response = await session.list_tools()
                tools = response.model_dump()['tools']
                print(len(tools), "tools found:")
                print(json.dumps(tools, indent=4, ensure_ascii=False))
            except Exception as e:
                print(f"Error listing tools: {e}")

            try:
                response = await session.list_prompts()
                prompts = response.model_dump()['prompts']
                print(json.dumps(prompts, indent=4, ensure_ascii=False))
            except Exception as e:
                print(f"Error listing prompts: {e}")

            try:
                response = await session.list_resources()
                resources = response.model_dump()['resources']
                print(json.dumps(resources, indent=4, ensure_ascii=False, default=str))
            except Exception as e:
                print(f"Error listing resources: {e}")

            try:
                response = await session.list_resource_templates()
                resource_templates = []
                for res in response.model_dump()['resourceTemplates']:
                    res['uri'] = res['uriTemplate']
                    resource_templates.append(res)
                print(json.dumps(resource_templates, indent=4, ensure_ascii=False))
            except Exception as e:
                print(f"Error listing resource templates: {e}")

            try:
                response = await session.call_tool(
                    'list_account_stages',
                    arguments={}
                )
                result = response.model_dump()['content']
                print(json.dumps(result, indent=4, ensure_ascii=False))
            except Exception as e:
                print(f"Error calling tool : {e}")



if __name__ == "__main__":
    asyncio.run(main())
