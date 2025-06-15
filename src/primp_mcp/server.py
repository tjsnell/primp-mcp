"""MCP server implementation for primp HTTP client."""

import asyncio
import json
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

import primp
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.lowlevel.server import NotificationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    TextContent,
    Tool,
)


class PrimpMCPServer:
    """MCP server for primp HTTP client operations."""
    
    def __init__(self):
        self.server = Server("primp-mcp")
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Set up MCP server handlers."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> ListToolsResult:
            """List available primp tools."""
            return ListToolsResult(
                tools=[
                    Tool(
                        name="primp_request",
                        description="Make HTTP requests using primp with browser impersonation",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "url": {
                                    "type": "string",
                                    "description": "The URL to make the request to"
                                },
                                "method": {
                                    "type": "string",
                                    "enum": ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
                                    "default": "GET",
                                    "description": "HTTP method to use"
                                },
                                "headers": {
                                    "type": "object",
                                    "description": "HTTP headers to include in the request",
                                    "additionalProperties": {"type": "string"}
                                },
                                "data": {
                                    "type": "string",
                                    "description": "Request body data (for POST, PUT, PATCH)"
                                },
                                "json": {
                                    "type": "object",
                                    "description": "JSON data to send in request body"
                                },
                                "params": {
                                    "type": "object",
                                    "description": "URL query parameters",
                                    "additionalProperties": {"type": "string"}
                                },
                                "impersonate": {
                                    "type": "string",
                                    "enum": ["chrome_131", "chrome_130", "chrome_129", "chrome_128", "chrome_127", "chrome_126", "chrome_125", "chrome_124", "chrome_123", "chrome_120", "chrome_119", "chrome_118", "chrome_117", "chrome_116", "chrome_115", "chrome_114", "chrome_113", "chrome_112", "chrome_111", "chrome_110", "chrome_109", "chrome_108", "chrome_107", "chrome_106", "chrome_105", "chrome_104", "chrome_103", "chrome_102", "chrome_101", "chrome_100", "chrome_99", "safari_18_0", "safari_17_5", "safari_17_4_1", "safari_17_2_1", "safari_17_0", "safari_16_5", "safari_15_6_1", "safari_15_5", "safari_15_3", "safari_15_0", "safari_14_1_2", "safari_14_0_3", "safari_13_1_3", "safari_13_0_5", "safari_12_1_2", "safari_12_0", "safari_ipad_18_0", "safari_ipad_17_5", "safari_ipad_17_4_1", "safari_ipad_17_2_1", "safari_ipad_17_0", "safari_ipad_16_5", "safari_ipad_15_6_1", "safari_ipad_15_5", "safari_ipad_15_3", "safari_ipad_15_0", "safari_iphone_18_0", "safari_iphone_17_5", "safari_iphone_17_4_1", "safari_iphone_17_2_1", "safari_iphone_17_0", "safari_iphone_16_5", "safari_iphone_15_6_1", "safari_iphone_15_5", "safari_iphone_15_3", "safari_iphone_15_0", "edge_131", "edge_130", "edge_129", "edge_128", "edge_127", "edge_126", "edge_125", "edge_124", "edge_123", "edge_122", "edge_121", "edge_120", "edge_119", "edge_118", "edge_117", "edge_116", "edge_115", "edge_114", "edge_113", "edge_112", "edge_111", "edge_110", "edge_109", "edge_108", "edge_107", "edge_106", "edge_105", "edge_104", "edge_103", "edge_102", "edge_101", "edge_100", "edge_99", "firefox_133", "firefox_132", "firefox_131", "firefox_130", "firefox_129", "firefox_128", "firefox_127", "firefox_126", "firefox_125", "firefox_124", "firefox_123", "firefox_122", "firefox_121", "firefox_120", "firefox_119", "firefox_118", "firefox_117", "firefox_116", "firefox_115", "firefox_114", "firefox_113", "firefox_112", "firefox_111", "firefox_110", "firefox_109", "firefox_108", "firefox_107", "firefox_106", "firefox_105", "firefox_104", "firefox_103", "firefox_102", "firefox_101", "firefox_100", "firefox_99", "okhttp_5_0_0", "okhttp_4_12_0", "okhttp_4_11_0", "okhttp_4_10_0", "okhttp_4_9_3", "okhttp_3_14_9"],
                                    "default": "chrome_131",
                                    "description": "Browser to impersonate"
                                },
                                "impersonate_os": {
                                    "type": "string",
                                    "enum": ["windows", "macos", "linux", "android", "ios"],
                                    "default": "windows",
                                    "description": "Operating system to impersonate"
                                },
                                "proxy": {
                                    "type": "string",
                                    "description": "Proxy URL (e.g., http://proxy:8080)"
                                },
                                "auth": {
                                    "type": "object",
                                    "properties": {
                                        "username": {"type": "string"},
                                        "password": {"type": "string"}
                                    },
                                    "required": ["username", "password"],
                                    "description": "Basic authentication credentials"
                                },
                                "bearer_token": {
                                    "type": "string",
                                    "description": "Bearer token for authorization"
                                },
                                "timeout": {
                                    "type": "number",
                                    "default": 30,
                                    "description": "Request timeout in seconds"
                                },
                                "follow_redirects": {
                                    "type": "boolean",
                                    "default": True,
                                    "description": "Whether to follow redirects"
                                },
                                "verify": {
                                    "type": "boolean",
                                    "default": True,
                                    "description": "Whether to verify SSL certificates"
                                },
                                "return_format": {
                                    "type": "string",
                                    "enum": ["text", "json", "markdown", "plain_text", "rich_text"],
                                    "default": "text",
                                    "description": "Format to return response content in"
                                }
                            },
                            "required": ["url"]
                        }
                    ),
                    Tool(
                        name="primp_upload",
                        description="Upload files using primp with multipart form data",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "url": {
                                    "type": "string",
                                    "description": "The URL to upload to"
                                },
                                "files": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string", "description": "Form field name"},
                                            "filename": {"type": "string", "description": "File name"},
                                            "content": {"type": "string", "description": "File content (base64 encoded)"},
                                            "content_type": {"type": "string", "description": "MIME type"}
                                        },
                                        "required": ["name", "filename", "content"]
                                    },
                                    "description": "Files to upload"
                                },
                                "data": {
                                    "type": "object",
                                    "description": "Additional form data",
                                    "additionalProperties": {"type": "string"}
                                },
                                "headers": {
                                    "type": "object",
                                    "description": "HTTP headers to include",
                                    "additionalProperties": {"type": "string"}
                                },
                                "impersonate": {
                                    "type": "string",
                                    "default": "chrome_131",
                                    "description": "Browser to impersonate"
                                },
                                "impersonate_os": {
                                    "type": "string",
                                    "default": "windows",
                                    "description": "Operating system to impersonate"
                                },
                                "timeout": {
                                    "type": "number",
                                    "default": 30,
                                    "description": "Request timeout in seconds"
                                }
                            },
                            "required": ["url", "files"]
                        }
                    )
                ]
            )
        
        @self.server.call_tool()
        async def handle_call_tool(request: CallToolRequest) -> CallToolResult:
            """Handle tool calls."""
            try:
                if request.params.name == "primp_request":
                    return await self._handle_primp_request(request.params.arguments)
                elif request.params.name == "primp_upload":
                    return await self._handle_primp_upload(request.params.arguments)
                else:
                    raise ValueError(f"Unknown tool: {request.params.name}")
            except Exception as e:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")],
                    isError=True
                )
    
    async def _handle_primp_request(self, args: Dict[str, Any]) -> CallToolResult:
        """Handle primp HTTP request."""
        url = args["url"]
        method = args.get("method", "GET").upper()
        headers = args.get("headers", {})
        data = args.get("data")
        json_data = args.get("json")
        params = args.get("params", {})
        impersonate = args.get("impersonate", "chrome_131")
        impersonate_os = args.get("impersonate_os", "windows")
        proxy = args.get("proxy")
        auth = args.get("auth")
        bearer_token = args.get("bearer_token")
        timeout = args.get("timeout", 30)
        follow_redirects = args.get("follow_redirects", True)
        verify = args.get("verify", True)
        return_format = args.get("return_format", "text")
        
        # Create client with impersonation
        client_kwargs = {
            "impersonate": impersonate,
            "impersonate_os": impersonate_os,
            "timeout": timeout,
            "follow_redirects": follow_redirects,
            "verify": verify
        }
        
        if proxy:
            client_kwargs["proxy"] = proxy
        
        client = primp.Client(**client_kwargs)
        
        # Handle authentication
        if bearer_token:
            headers["Authorization"] = f"Bearer {bearer_token}"
        
        # Prepare request arguments
        request_kwargs = {
            "url": url,
            "headers": headers,
            "params": params
        }
        
        if auth:
            request_kwargs["auth"] = (auth["username"], auth["password"])
        
        # Add data/json based on method
        if method in ["POST", "PUT", "PATCH"]:
            if json_data:
                request_kwargs["json"] = json_data
            elif data:
                request_kwargs["data"] = data
        
        # Make the request
        if method == "GET":
            response = client.get(**request_kwargs)
        elif method == "POST":
            response = client.post(**request_kwargs)
        elif method == "PUT":
            response = client.put(**request_kwargs)
        elif method == "PATCH":
            response = client.patch(**request_kwargs)
        elif method == "DELETE":
            response = client.delete(**request_kwargs)
        elif method == "HEAD":
            response = client.head(**request_kwargs)
        elif method == "OPTIONS":
            response = client.options(**request_kwargs)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        # Format response based on return_format
        if return_format == "json":
            try:
                content = response.json()
                response_text = json.dumps(content, indent=2)
            except:
                response_text = response.text
        elif return_format == "markdown":
            response_text = response.markdown
        elif return_format == "plain_text":
            response_text = response.plain_text
        elif return_format == "rich_text":
            response_text = response.rich_text
        else:  # text
            response_text = response.text
        
        # Prepare response summary
        status_info = f"Status: {response.status_code} {response.reason_phrase}"
        headers_info = f"Headers: {dict(response.headers)}"
        
        result_text = f"{status_info}\n{headers_info}\n\nContent:\n{response_text}"
        
        return CallToolResult(
            content=[TextContent(type="text", text=result_text)]
        )
    
    async def _handle_primp_upload(self, args: Dict[str, Any]) -> CallToolResult:
        """Handle file upload using primp."""
        import base64
        
        url = args["url"]
        files_data = args["files"]
        form_data = args.get("data", {})
        headers = args.get("headers", {})
        impersonate = args.get("impersonate", "chrome_131")
        impersonate_os = args.get("impersonate", "windows")
        timeout = args.get("timeout", 30)
        
        # Create client
        client = primp.Client(
            impersonate=impersonate,
            impersonate_os=impersonate_os,
            timeout=timeout
        )
        
        # Prepare files for upload
        files = []
        for file_info in files_data:
            name = file_info["name"]
            filename = file_info["filename"]
            content = base64.b64decode(file_info["content"])
            content_type = file_info.get("content_type", "application/octet-stream")
            
            files.append((name, (filename, content, content_type)))
        
        # Make the upload request
        response = client.post(
            url=url,
            files=files,
            data=form_data,
            headers=headers
        )
        
        # Format response
        status_info = f"Status: {response.status_code} {response.reason_phrase}"
        headers_info = f"Headers: {dict(response.headers)}"
        
        result_text = f"{status_info}\n{headers_info}\n\nContent:\n{response.text}"
        
        return CallToolResult(
            content=[TextContent(type="text", text=result_text)]
        )
    
    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="primp-mcp",
                    server_version="0.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    ),
                ),
            )


def main():
    """Main entry point."""
    server = PrimpMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()