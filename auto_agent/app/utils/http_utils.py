"""
HTTP Utils
HTTP request utilities
"""

from typing import Any, Dict, Optional

import requests


class HttpUtils:
    """HTTP utility class"""

    @staticmethod
    def get(
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = 30,
    ) -> Dict[str, Any]:
        """
        HTTP GET request

        Args:
            url: Request URL
            headers: Request headers
            params: Request parameters
            timeout: Request timeout

        Returns:
            Response dictionary
        """
        try:
            response = requests.get(
                url, headers=headers, params=params, timeout=timeout
            )
            return {
                "status_code": response.status_code,
                "ok": response.ok,
                "content": response.text,
                "json": (
                    response.json()
                    if response.headers.get("content-type") == "application/json"
                    else None
                ),
                "headers": dict(response.headers),
            }
        except Exception as e:
            return {
                "status_code": 500,
                "ok": False,
                "content": str(e),
                "json": None,
                "headers": {},
            }

    @staticmethod
    def post(
        url: str,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
    ) -> Dict[str, Any]:
        """
        HTTP POST request

        Args:
            url: Request URL
            data: Form data
            json: JSON data
            headers: Request headers
            timeout: Request timeout

        Returns:
            Response dictionary
        """
        try:
            response = requests.post(
                url, data=data, json=json, headers=headers, timeout=timeout
            )
            return {
                "status_code": response.status_code,
                "ok": response.ok,
                "content": response.text,
                "json": (
                    response.json()
                    if response.headers.get("content-type") == "application/json"
                    else None
                ),
                "headers": dict(response.headers),
            }
        except Exception as e:
            return {
                "status_code": 500,
                "ok": False,
                "content": str(e),
                "json": None,
                "headers": {},
            }

    @staticmethod
    def put(
        url: str,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
    ) -> Dict[str, Any]:
        """
        HTTP PUT request

        Args:
            url: Request URL
            data: Form data
            json: JSON data
            headers: Request headers
            timeout: Request timeout

        Returns:
            Response dictionary
        """
        try:
            response = requests.put(
                url, data=data, json=json, headers=headers, timeout=timeout
            )
            return {
                "status_code": response.status_code,
                "ok": response.ok,
                "content": response.text,
                "json": (
                    response.json()
                    if response.headers.get("content-type") == "application/json"
                    else None
                ),
                "headers": dict(response.headers),
            }
        except Exception as e:
            return {
                "status_code": 500,
                "ok": False,
                "content": str(e),
                "json": None,
                "headers": {},
            }

    @staticmethod
    def delete(
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = 30,
    ) -> Dict[str, Any]:
        """
        HTTP DELETE request

        Args:
            url: Request URL
            headers: Request headers
            params: Request parameters
            timeout: Request timeout

        Returns:
            Response dictionary
        """
        try:
            response = requests.delete(
                url, headers=headers, params=params, timeout=timeout
            )
            return {
                "status_code": response.status_code,
                "ok": response.ok,
                "content": response.text,
                "json": (
                    response.json()
                    if response.headers.get("content-type") == "application/json"
                    else None
                ),
                "headers": dict(response.headers),
            }
        except Exception as e:
            return {
                "status_code": 500,
                "ok": False,
                "content": str(e),
                "json": None,
                "headers": {},
            }

    @staticmethod
    def patch(
        url: str,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
    ) -> Dict[str, Any]:
        """
        HTTP PATCH request

        Args:
            url: Request URL
            data: Form data
            json: JSON data
            headers: Request headers
            timeout: Request timeout

        Returns:
            Response dictionary
        """
        try:
            response = requests.patch(
                url, data=data, json=json, headers=headers, timeout=timeout
            )
            return {
                "status_code": response.status_code,
                "ok": response.ok,
                "content": response.text,
                "json": (
                    response.json()
                    if response.headers.get("content-type") == "application/json"
                    else None
                ),
                "headers": dict(response.headers),
            }
        except Exception as e:
            return {
                "status_code": 500,
                "ok": False,
                "content": str(e),
                "json": None,
                "headers": {},
            }

    @staticmethod
    def download_file(
        url: str,
        save_path: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
    ) -> bool:
        """
        Download file

        Args:
            url: File URL
            save_path: Save path
            headers: Request headers
            timeout: Request timeout

        Returns:
            Whether download was successful
        """
        try:
            response = requests.get(url, headers=headers, timeout=timeout, stream=True)
            if response.ok:
                # Ensure directory exists
                import os

                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                with open(save_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
            return False
        except Exception:
            return False


# Global instance
http_utils = HttpUtils()
