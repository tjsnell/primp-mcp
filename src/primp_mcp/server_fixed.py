#!/usr/bin/env python3
"""Simple MCP server implementation for primp HTTP client."""

import asyncio
import json
import logging
from typing import Any, Dict

import primp
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server
mcp = FastMCP("primp-mcp")


@mcp.tool()
def primp_request(
    url: str,
    method: str = "GET",
    headers: Dict[str, str] = None,
    data: str = None,
    json_data: Dict[str, Any] = None,
    params: Dict[str, str] = None,
    impersonate: str = "chrome_131",
    impersonate_os: str = "windows",
    proxy: str = None,
    bearer_token: str = None,
    timeout: int = 30,
    follow_redirects: bool = True,
    verify: bool = True,
    return_format: str = "text"
) -> str:
    """Make HTTP requests using primp with browser impersonation.
    
    Args:
        url: The URL to make the request to
        method: HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS)
        headers: HTTP headers to include
        data: Request body data for POST/PUT/PATCH
        json_data: JSON data to send in request body
        params: URL query parameters
        impersonate: Browser to impersonate
        impersonate_os: Operating system to impersonate
        proxy: Proxy URL
        bearer_token: Bearer token for authorization
        timeout: Request timeout in seconds
        follow_redirects: Whether to follow redirects
        verify: Whether to verify SSL certificates
        return_format: Format to return response (text, json, markdown, plain_text, rich_text)
    
    Returns:
        HTTP response formatted according to return_format
    """
    try:
        # Set up headers
        if headers is None:
            headers = {}
        
        if bearer_token:
            headers["Authorization"] = f"Bearer {bearer_token}"
        
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
        
        # Prepare request arguments
        request_kwargs = {
            "url": url,
            "headers": headers,
        }
        
        if params:
            request_kwargs["params"] = params
        
        # Add data/json based on method
        method = method.upper()
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
            response_text = response.text_markdown
        elif return_format == "plain_text":
            response_text = response.text_plain
        elif return_format == "rich_text":
            # Fall back to text_markdown if rich_text not available
            response_text = getattr(response, 'rich_text', response.text_markdown)
        else:  # text
            response_text = response.text
        
        # Prepare response summary
        status_info = f"Status: {response.status_code}"
        headers_info = f"Headers: {dict(response.headers)}"
        
        result = f"{status_info}\n{headers_info}\n\nContent:\n{response_text}"
        return result
        
    except Exception as e:
        error_msg = f"Error making request: {str(e)}"
        logger.error(error_msg)
        return error_msg


@mcp.tool()
def primp_upload(
    url: str,
    files: list,
    data: Dict[str, str] = None,
    headers: Dict[str, str] = None,
    impersonate: str = "chrome_131",
    impersonate_os: str = "windows",
    timeout: int = 30
) -> str:
    """Upload files using primp with multipart form data.
    
    Args:
        url: The URL to upload to
        files: List of file objects with name, filename, content (base64), content_type
        data: Additional form data
        headers: HTTP headers to include
        impersonate: Browser to impersonate
        impersonate_os: Operating system to impersonate
        timeout: Request timeout in seconds
    
    Returns:
        HTTP response as text
    """
    try:
        import base64
        
        if headers is None:
            headers = {}
        if data is None:
            data = {}
        
        # Create client
        client = primp.Client(
            impersonate=impersonate,
            impersonate_os=impersonate_os,
            timeout=timeout
        )
        
        # Prepare files for upload
        upload_files = []
        for file_info in files:
            name = file_info["name"]
            filename = file_info["filename"]
            content = base64.b64decode(file_info["content"])
            content_type = file_info.get("content_type", "application/octet-stream")
            
            upload_files.append((name, (filename, content, content_type)))
        
        # Make the upload request
        response = client.post(
            url=url,
            files=upload_files,
            data=data,
            headers=headers
        )
        
        # Format response
        status_info = f"Status: {response.status_code}"
        headers_info = f"Headers: {dict(response.headers)}"
        
        result = f"{status_info}\n{headers_info}\n\nContent:\n{response.text}"
        return result
        
    except Exception as e:
        error_msg = f"Error uploading files: {str(e)}"
        logger.error(error_msg)
        return error_msg


def main():
    """Main entry point."""
    mcp.run()


if __name__ == "__main__":
    main()