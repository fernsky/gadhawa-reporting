"""
Chart Generation Service

Provides high-level interface for chart generation, caching, and management.
"""

import time
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from .models import ChartCache, ChartGenerationLog, ChartStatusChoice, ChartTypeChoice
from apps.demographics.utils.svg_chart_generator import SVGChartGenerator


class ChartGenerationService:
    """
    Service for managing chart generation with caching and tracking
    """
    
    def __init__(self):
        self.svg_generator = SVGChartGenerator()
        self.charts_dir = Path(settings.STATIC_ROOT) / "images" / "charts"
        self.charts_dir.mkdir(parents=True, exist_ok=True)
    
    def get_or_generate_chart(
        self,
        chart_key: str,
        chart_type: str,
        data: Dict[str, Any],
        title: str,
        width: int = 800,
        height: int = 400,
        **kwargs
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Get existing chart or generate new one if needed
        
        Returns:
            Tuple of (svg_url, png_url)
        """
        
        # Generate content hash
        content_hash = ChartCache.generate_content_hash(data)
        
        # Try to get existing chart
        chart_cache = self._get_existing_chart(chart_key, content_hash)
        
        if chart_cache and self._validate_chart_files(chart_cache):
            # Chart exists and files are valid
            chart_cache.mark_accessed()
            return chart_cache.svg_url, chart_cache.png_url
        
        # Generate new chart
        return self._generate_new_chart(
            chart_key=chart_key,
            chart_type=chart_type,
            data=data,
            title=title,
            width=width,
            height=height,
            content_hash=content_hash,
            **kwargs
        )
    
    def _get_existing_chart(self, chart_key: str, content_hash: str) -> Optional[ChartCache]:
        """Get existing chart from cache"""
        try:
            return ChartCache.objects.get(
                chart_key=chart_key,
                content_hash=content_hash,
                status=ChartStatusChoice.COMPLETED
            )
        except ChartCache.DoesNotExist:
            return None
    
    def _validate_chart_files(self, chart_cache: ChartCache) -> bool:
        """Validate that chart files exist on filesystem"""
        svg_exists = chart_cache.svg_exists()
        png_exists = chart_cache.png_exists() if chart_cache.png_path else True
        
        if not svg_exists or not png_exists:
            # Mark as failed and clean up
            chart_cache.status = ChartStatusChoice.FAILED
            chart_cache.error_message = "Chart files missing from filesystem"
            chart_cache.save()
            return False
        
        return True
    
    def _generate_new_chart(
        self,
        chart_key: str,
        chart_type: str,
        data: Dict[str, Any],
        title: str,
        width: int,
        height: int,
        content_hash: str,
        **kwargs
    ) -> Tuple[Optional[str], Optional[str]]:
        """Generate new chart and save to cache"""
        
        start_time = time.time()
        
        # Create or update chart cache entry
        with transaction.atomic():
            chart_cache, created = ChartCache.objects.get_or_create(
                chart_key=chart_key,
                content_hash=content_hash,
                defaults={
                    'chart_type': chart_type,
                    'title': title,
                    'width': width,
                    'height': height,
                    'status': ChartStatusChoice.GENERATING,
                }
            )
            
            if not created:
                # Update existing entry
                chart_cache.status = ChartStatusChoice.GENERATING
                chart_cache.title = title
                chart_cache.width = width
                chart_cache.height = height
                chart_cache.save()
        
        try:
            # Generate SVG
            svg_content = self._generate_svg_content(
                chart_type, data, title, width, height, **kwargs
            )
            
            if not svg_content:
                raise ValueError("Failed to generate SVG content")
            
            # Save SVG file
            svg_path = self._save_svg_file(chart_cache, svg_content)
            
            # Generate PNG
            png_path = self._generate_png_file(chart_cache, svg_path)
            
            # Update cache with success
            svg_content_hash = ChartCache.generate_svg_content_hash(svg_content)
            
            chart_cache.svg_path = svg_path.name
            chart_cache.png_path = png_path.name if png_path else None
            chart_cache.svg_content_hash = svg_content_hash
            chart_cache.status = ChartStatusChoice.COMPLETED
            chart_cache.svg_generated_at = timezone.now()
            if png_path:
                chart_cache.png_generated_at = timezone.now()
            chart_cache.error_message = None
            chart_cache.save()
            
            # Log successful generation
            self._log_generation(
                chart_cache,
                'svg_generation',
                ChartStatusChoice.COMPLETED,
                time.time() - start_time
            )
            
            return chart_cache.svg_url, chart_cache.png_url
            
        except Exception as e:
            # Update cache with failure
            chart_cache.status = ChartStatusChoice.FAILED
            chart_cache.error_message = str(e)
            chart_cache.save()
            
            # Log failure
            self._log_generation(
                chart_cache,
                'svg_generation',
                ChartStatusChoice.FAILED,
                time.time() - start_time,
                error_message=str(e)
            )
            
            return None, None
    
    def _generate_svg_content(
        self,
        chart_type: str,
        data: Dict[str, Any],
        title: str,
        width: int,
        height: int,
        **kwargs
    ) -> Optional[str]:
        """Generate SVG content using the chart generator"""
        
        try:
            if chart_type == ChartTypeChoice.PIE:
                return self.svg_generator.generate_pie_chart(
                    data=data,
                    title=title,
                    width=width,
                    height=height,
                    **kwargs
                )
            elif chart_type == ChartTypeChoice.BAR:
                return self.svg_generator.generate_bar_chart(
                    data=data,
                    title=title,
                    width=width,
                    height=height,
                    **kwargs
                )
            else:
                raise ValueError(f"Unsupported chart type: {chart_type}")
                
        except Exception as e:
            print(f"Error generating SVG content: {e}")
            return None
    
    def _save_svg_file(self, chart_cache: ChartCache, svg_content: str) -> Path:
        """Save SVG content to file"""
        
        # Generate filename based on cache ID and content hash
        filename = f"{chart_cache.chart_key}_{chart_cache.content_hash[:8]}.svg"
        file_path = self.charts_dir / filename
        
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write SVG content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        return file_path
    
    def _generate_png_file(self, chart_cache: ChartCache, svg_path: Path) -> Optional[Path]:
        """Convert SVG to PNG using Inkscape"""
        
        start_time = time.time()
        
        try:
            # Generate PNG filename
            png_filename = svg_path.stem + '.png'
            png_path = svg_path.parent / png_filename
            
            # Use Inkscape to convert SVG to PNG
            cmd = [
                'inkscape',
                '--export-type=png',
                f'--export-filename={png_path}',
                f'--export-width={chart_cache.width}',
                f'--export-height={chart_cache.height}',
                str(svg_path)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            if result.returncode == 0 and png_path.exists():
                # Log successful PNG conversion
                self._log_generation(
                    chart_cache,
                    'png_conversion',
                    ChartStatusChoice.COMPLETED,
                    time.time() - start_time
                )
                return png_path
            else:
                # Log PNG conversion failure
                error_msg = f"Inkscape error: {result.stderr}"
                self._log_generation(
                    chart_cache,
                    'png_conversion',
                    ChartStatusChoice.FAILED,
                    time.time() - start_time,
                    error_message=error_msg
                )
                print(f"PNG conversion failed: {error_msg}")
                return None
                
        except subprocess.TimeoutExpired:
            error_msg = "PNG conversion timed out"
            self._log_generation(
                chart_cache,
                'png_conversion',
                ChartStatusChoice.FAILED,
                time.time() - start_time,
                error_message=error_msg
            )
            print(error_msg)
            return None
            
        except Exception as e:
            error_msg = f"PNG conversion error: {str(e)}"
            self._log_generation(
                chart_cache,
                'png_conversion',
                ChartStatusChoice.FAILED,
                time.time() - start_time,
                error_message=error_msg
            )
            print(error_msg)
            return None
    
    def _log_generation(
        self,
        chart_cache: ChartCache,
        operation_type: str,
        status: str,
        processing_time: float,
        error_message: Optional[str] = None
    ):
        """Log chart generation operation"""
        
        ChartGenerationLog.objects.create(
            chart_cache=chart_cache,
            operation_type=operation_type,
            status=status,
            processing_time=processing_time,
            error_message=error_message
        )
    
    def cleanup_old_charts(self, days_old: int = 30) -> int:
        """Clean up old unused charts"""
        
        from django.utils import timezone
        from datetime import timedelta
        
        cutoff_date = timezone.now() - timedelta(days=days_old)
        
        # Find old charts
        old_charts = ChartCache.objects.filter(
            created_at__lt=cutoff_date,
            access_count__lt=5  # Haven't been accessed much
        )
        
        deleted_count = 0
        
        for chart in old_charts:
            try:
                # Delete files
                if chart.svg_exists():
                    chart.get_svg_full_path().unlink()
                if chart.png_exists():
                    chart.get_png_full_path().unlink()
                
                # Delete database record
                chart.delete()
                deleted_count += 1
                
            except Exception as e:
                print(f"Error cleaning up chart {chart.chart_key}: {e}")
        
        return deleted_count
    
    def get_chart_stats(self) -> Dict[str, Any]:
        """Get statistics about chart generation"""
        
        total_charts = ChartCache.objects.count()
        completed_charts = ChartCache.objects.filter(
            status=ChartStatusChoice.COMPLETED
        ).count()
        failed_charts = ChartCache.objects.filter(
            status=ChartStatusChoice.FAILED
        ).count()
        
        # Calculate cache hit rate
        total_logs = ChartGenerationLog.objects.count()
        cache_hits = total_charts - ChartGenerationLog.objects.filter(
            operation_type='svg_generation'
        ).count()
        
        cache_hit_rate = (cache_hits / max(total_logs, 1)) * 100
        
        return {
            'total_charts': total_charts,
            'completed_charts': completed_charts,
            'failed_charts': failed_charts,
            'cache_hit_rate': round(cache_hit_rate, 2),
            'pending_charts': ChartCache.objects.filter(
                status__in=[ChartStatusChoice.PENDING, ChartStatusChoice.GENERATING]
            ).count()
        }


# Global service instance
_chart_service = None

def get_chart_service() -> ChartGenerationService:
    """Get the global chart generation service instance"""
    global _chart_service
    if _chart_service is None:
        _chart_service = ChartGenerationService()
    return _chart_service
