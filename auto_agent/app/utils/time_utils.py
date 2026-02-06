"""
Time Utils
Time operation utilities
"""

import time
from datetime import datetime, timedelta
from typing import Optional, Union


class TimeUtils:
    """Time utility class"""

    @staticmethod
    def get_current_time() -> datetime:
        """
        Get current time

        Returns:
            Current datetime object
        """
        return datetime.now()

    @staticmethod
    def get_current_timestamp() -> float:
        """
        Get current timestamp

        Returns:
            Current timestamp
        """
        return time.time()

    @staticmethod
    def get_current_timestamp_ms() -> int:
        """
        Get current timestamp in milliseconds

        Returns:
            Current timestamp in milliseconds
        """
        return int(time.time() * 1000)

    @staticmethod
    def format_time(
        dt: Optional[datetime] = None, format_str: str = "%Y-%m-%d %H:%M:%S"
    ) -> str:
        """
        Format time

        Args:
            dt: Datetime object (default: current time)
            format_str: Format string

        Returns:
            Formatted time string
        """
        if dt is None:
            dt = TimeUtils.get_current_time()
        return dt.strftime(format_str)

    @staticmethod
    def parse_time(
        time_str: str, format_str: str = "%Y-%m-%d %H:%M:%S"
    ) -> Optional[datetime]:
        """
        Parse time string

        Args:
            time_str: Time string
            format_str: Format string

        Returns:
            Parsed datetime object or None if error
        """
        try:
            return datetime.strptime(time_str, format_str)
        except Exception:
            return None

    @staticmethod
    def timestamp_to_datetime(timestamp: float) -> datetime:
        """
        Convert timestamp to datetime

        Args:
            timestamp: Timestamp

        Returns:
            Datetime object
        """
        return datetime.fromtimestamp(timestamp)

    @staticmethod
    def datetime_to_timestamp(dt: datetime) -> float:
        """
        Convert datetime to timestamp

        Args:
            dt: Datetime object

        Returns:
            Timestamp
        """
        return dt.timestamp()

    @staticmethod
    def add_seconds(dt: Optional[datetime] = None, seconds: int = 0) -> datetime:
        """
        Add seconds to datetime

        Args:
            dt: Datetime object (default: current time)
            seconds: Seconds to add

        Returns:
            New datetime object
        """
        if dt is None:
            dt = TimeUtils.get_current_time()
        return dt + timedelta(seconds=seconds)

    @staticmethod
    def add_minutes(dt: Optional[datetime] = None, minutes: int = 0) -> datetime:
        """
        Add minutes to datetime

        Args:
            dt: Datetime object (default: current time)
            minutes: Minutes to add

        Returns:
            New datetime object
        """
        if dt is None:
            dt = TimeUtils.get_current_time()
        return dt + timedelta(minutes=minutes)

    @staticmethod
    def add_hours(dt: Optional[datetime] = None, hours: int = 0) -> datetime:
        """
        Add hours to datetime

        Args:
            dt: Datetime object (default: current time)
            hours: Hours to add

        Returns:
            New datetime object
        """
        if dt is None:
            dt = TimeUtils.get_current_time()
        return dt + timedelta(hours=hours)

    @staticmethod
    def add_days(dt: Optional[datetime] = None, days: int = 0) -> datetime:
        """
        Add days to datetime

        Args:
            dt: Datetime object (default: current time)
            days: Days to add

        Returns:
            New datetime object
        """
        if dt is None:
            dt = TimeUtils.get_current_time()
        return dt + timedelta(days=days)

    @staticmethod
    def get_time_difference(
        start_time: Union[datetime, float], end_time: Union[datetime, float]
    ) -> float:
        """
        Get time difference in seconds

        Args:
            start_time: Start time (datetime or timestamp)
            end_time: End time (datetime or timestamp)

        Returns:
            Time difference in seconds
        """
        try:
            if isinstance(start_time, datetime):
                start_time = start_time.timestamp()
            if isinstance(end_time, datetime):
                end_time = end_time.timestamp()
            return end_time - start_time
        except Exception:
            return 0.0

    @staticmethod
    def format_duration(seconds: float) -> str:
        """
        Format duration

        Args:
            seconds: Duration in seconds

        Returns:
            Formatted duration string
        """
        try:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)

            parts = []
            if hours > 0:
                parts.append(f"{hours}h")
            if minutes > 0:
                parts.append(f"{minutes}m")
            if secs > 0 or not parts:
                parts.append(f"{secs}s")

            return " ".join(parts)
        except Exception:
            return f"{seconds}s"


# Global instance
time_utils = TimeUtils()
