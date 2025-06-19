"""
Simple Chart Processor Base Class

Minimal base class for processors that need to track chart files.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from .services import get_chart_service


class SimpleChartProcessor(ABC):
    """
    Simple base processor for chart file tracking
    """

    def __init__(self):
        self.chart_service = get_chart_service()

    @abstractmethod
    def get_chart_key(self):
        """Return unique chart key for this processor"""
        pass

    def track_chart_file(self, chart_type: str, data: Dict[str, Any], 
                        file_path: str, title: str = "") -> Optional[str]:
        """
        Track a chart file
        
        Args:
            chart_type: Type of chart (pie, bar, etc.)
            data: Chart data for hash generation
            file_path: Relative path to the chart file
            title: Optional title
            
        Returns:
            URL of the chart file if it exists, None otherwise
        """
        chart_key = f"{self.get_chart_key()}_{chart_type}"
        
        return self.chart_service.track_chart(
            chart_key=chart_key,
            chart_type=chart_type,
            data=data,
            file_path=file_path,
            title=title
        )

    def get_chart_url(self, chart_type: str) -> Optional[str]:
        """Get URL for existing chart"""
        chart_key = f"{self.get_chart_key()}_{chart_type}"
        return self.chart_service.get_chart_url(chart_key)

    def is_chart_current(self, chart_type: str, data: Dict[str, Any]) -> bool:
        """Check if chart is current (data hasn't changed)"""
        chart_key = f"{self.get_chart_key()}_{chart_type}"
        return self.chart_service.is_chart_current(chart_key, data)
