import os
import sys
import time
import requests
from miio import Vacuum
from prometheus_client import start_http_server, Gauge, Enum


class RoborockMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    Roborock metrics into Prometheus metrics.
    """

    def __init__(self, ip_address="192.168.30.224", token="595037474941624f63494a6651533636", polling_interval_seconds=30):
        self.polling_interval_seconds = polling_interval_seconds
        self.vac = Vacuum(ip_address, token)

        if ip_address == None or token == None:
            sys.exit("No IP address or token found.")

        # Prometheus metrics to collect
        self.batteryGauge = Gauge("roborock_battery", "Current battery percentage")
        self.cleanAreaGauge = Gauge("roborock_clean_are", "Clean area in m2")
        self.cleanTimeGauge = Gauge("roborock_clean_time", "Cleaning time in seconds")
        self.errorCodeGauge = Gauge("roborock_error_code", "Boolean if error occurred")
        self.fanspeed = Gauge("roborock_fanspeed", "Current fanspeed code")
        self.inSegmentCleaningGauge = Gauge("roborock_in_segment_cleaning", "Boolean if is in segment cleaning")
        self.inZoneCleaningGauge = Gauge("roborock_in_zone_cleaning", "Boolean if is in zone cleaning")
        self.isOnGauge = Gauge("roborock_is_on", "Boolean if vacuum is cleaning")
        self.isPaused = Gauge("roborock_battery", "Current battery percentage")
        self.batteryGauge = Gauge("roborock_battery", "Current battery percentage")
        self.batteryGauge = Gauge("roborock_battery", "Current battery percentage")

        self.health = Enum("app_health", "Health", states=["healthy", "unhealthy"])

    def run_metrics_loop(self):
        """Metrics fetching loop"""

        while True:
            self.fetch()
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        """
        Get metrics from roborock and refresh Prometheus metrics with
        new values.
        """
        status = self.vac.status()

        battery = status.battery
        cleanArea = status.clean_area
        cleanTime = status.data['clean_time']
        errorCode = status.data['error_code']
        fanspeed = status.fanspeed
        inSegmentCleaning = status.in_segment_cleaning
        inZoneCleaning = status.in_zone_cleaning
        isOn = status.is_on
        isPaused = status.is_paused
        isWaterBoxAttached = status.is_water_box_attached
        isWaterBoxCarriageAttached = status.is_water_box_carriage_attached
        isWaterShortage = status.data['water_shortage_status']
        state = status.state

        cleaningSummary = self.vac.clean_history()

        cleanCount = cleaningSummary.count
        dustCollectionCount = cleaningSummary.dust_collection_count
        totalArea = cleaningSummary.total_area
        totalDuration = cleaningSummary.total_duration.seconds

        consumable = self.vac.consumable_status()

        filterLeft = consumable.filter_left
        mainBrushLeft = consumable.main_brush_left
        sensorDirtyLeft = consumable.sensor_dirty_left
        sideBrush Left = consumable.side_brush_left

        # Update Prometheus metrics with application metrics
        self.batteryGauge.set(battery)

def main():
    """Main entry point"""

    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "30"))
    ip_address = os.getenv("IP_ADDRESS", "192.168.30.224")
    token = os.getenv("TOKEN", "595037474941624f63494a6651533636")
    exporter_port = int(os.getenv("EXPORTER_PORT", "9877"))

    roborock_metrics = RoborockMetrics(
        polling_interval_seconds=polling_interval_seconds,
        ip_address=ip_address,
        token = token
    )
    start_http_server(exporter_port)
    roborock_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()