import os
import sys
import time
from miio import Vacuum
from prometheus_client import start_http_server, Gauge


class RoborockMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    Roborock metrics into Prometheus metrics.
    """

    def __init__(self, ip_address=None, token=None, polling_interval_seconds=30):
        self.polling_interval_seconds = polling_interval_seconds
        self.vac = Vacuum(ip_address, token)

        if ip_address == None or token == None:
            sys.exit("No IP address or token found.")

        # Prometheus metrics to collect
        self.batteryGauge = Gauge("roborock_battery", "Current battery percentage")
        self.cleanAreaGauge = Gauge("roborock_clean_area", "Clean area in m2")
        self.cleanTimeGauge = Gauge("roborock_clean_time", "Cleaning time in seconds")
        self.errorCodeGauge = Gauge("roborock_error_code", "Boolean if error occurred")
        self.fanspeedGauge = Gauge("roborock_fanspeed", "Current fanspeed code")
        self.inSegmentCleaningGauge = Gauge("roborock_in_segment_cleaning", "Boolean if is in segment cleaning")
        self.inZoneCleaningGauge = Gauge("roborock_in_zone_cleaning", "Boolean if is in zone cleaning")
        self.isOnGauge = Gauge("roborock_is_on", "Boolean if vacuum is cleaning")
        self.isPausedGauge = Gauge("roborock_is_pause", "Boolean if vacuum is paused")
        self.isWaterBoxAttachedGauge = Gauge("roborock_is_water_box_attached", "Boolean if waterbox is attached")
        self.isWaterBoxCarriageAttachedGauge = Gauge("roborock_is_water_box_carriage_attached", "Boolean if carriage is attached")
        self.isWaterShortageGauge = Gauge("roborock_water_shortage_status", "Boolean if there is water shortage")
        self.stateGauge = Gauge("roborock_state", "Roborock state")

        self.cleanCountGauge = Gauge("roborock_clean_count", "Integer count of cleanings")
        self.dustCollectionCountGauge = Gauge("roborock_dust_collection_count", "Integer count dust collections")
        self.totalAreaGauge = Gauge("roborock_total_area", "Metric of total cleaned area in m2")
        self.totalDurationGauge = Gauge("roborock_total_duration", "Metric of total time cleaning")

        self.filterLeftGauge = Gauge("roborock_filter_left", "Metric of left time until change of filter")
        self.mainBrushLeftGauge = Gauge("roborock_main_brush_left", "Metric of left time until change of main brush")
        self.sensorDirtyLeftGauge = Gauge("roborock_sensor_dirty_left", "Metric of left time until cleaning of sensors")
        self.sideBrushLeftGauge = Gauge("roborock_side_brush_left", "Metric of left time until change of side brush")

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
        state = status.data['state']

        cleaningSummary = self.vac.clean_history()

        cleanCount = cleaningSummary.count
        dustCollectionCount = cleaningSummary.dust_collection_count
        totalArea = cleaningSummary.total_area
        totalDuration = cleaningSummary.total_duration.seconds

        consumable = self.vac.consumable_status()

        filterLeft = consumable.filter_left
        mainBrushLeft = consumable.main_brush_left
        sensorDirtyLeft = consumable.sensor_dirty_left
        sideBrushLeft = consumable.side_brush_left

        # Update Prometheus metrics with roborock metrics
        self.batteryGauge.set(battery)
        self.cleanAreaGauge.set(cleanArea)
        self.cleanTimeGauge.set(cleanTime)
        self.errorCodeGauge.set(errorCode)
        self.fanspeedGauge.set(fanspeed)
        self.inSegmentCleaningGauge.set(inSegmentCleaning)
        self.inZoneCleaningGauge.set(inZoneCleaning)
        self.isOnGauge.set(isOn)
        self.isPausedGauge.set(isPaused)
        self.isWaterBoxAttachedGauge.set(isWaterBoxAttached)
        self.isWaterBoxCarriageAttachedGauge.set(isWaterBoxCarriageAttached)
        self.isWaterShortageGauge.set(isWaterShortage)
        self.stateGauge.set(state)

        self.cleanCountGauge.set(cleanCount)
        self.dustCollectionCountGauge.set(dustCollectionCount)
        self.totalAreaGauge.set(totalArea)
        self.totalDurationGauge.set(totalDuration)

        self.filterLeftGauge.set(filterLeft.total_seconds())
        self.mainBrushLeftGauge.set(mainBrushLeft.total_seconds())
        self.sensorDirtyLeftGauge.set(sensorDirtyLeft.total_seconds())
        self.sideBrushLeftGauge.set(sideBrushLeft.total_seconds())

def main():
    """Main entry point"""

    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "30"))
    ip_address = os.getenv("IP_ADDRESS", None)
    token = os.getenv("TOKEN", None)
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