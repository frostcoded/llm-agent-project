# integrations/apple_calendar_client.py

import datetime
from typing import List, Dict, Optional

try:
    import objc
    from Foundation import NSDate
    from EventKit import EKEventStore, EKEntityTypeEvent
except ImportError:
    objc = None  # For non-macOS platforms or testing


class AppleCalendarClient:
    """
    Integrates with Apple Calendar using macOS EventKit framework.
    Provides methods to read and write calendar events.
    """

    def __init__(self):
        if objc is None:
            raise EnvironmentError("AppleCalendarClient requires macOS with pyobjc installed.")
        self.store = EKEventStore.alloc().init()
        self._authorize()

    def _authorize(self):
        """
        Requests access to the user's calendar data.
        """
        self.store.requestAccessToEntityType_completion_(EKEntityTypeEvent, lambda granted, err: None)

    def list_events(self, start_date: datetime.datetime, end_date: datetime.datetime) -> List[Dict]:
        """
        Lists calendar events between two dates.
        """
        start_ns = NSDate.dateWithTimeIntervalSince1970_(start_date.timestamp())
        end_ns = NSDate.dateWithTimeIntervalSince1970_(end_date.timestamp())
        predicate = self.store.predicateForEventsWithStartDate_endDate_calendars_(
            start_ns, end_ns, None
        )
        events = self.store.eventsMatchingPredicate_(predicate)

        return [
            {
                "title": event.title(),
                "start": event.startDate().description(),
                "end": event.endDate().description(),
                "location": event.location(),
                "notes": event.notes(),
            }
            for event in events
        ]

    def create_block_event(self, title: str, start_time: datetime.datetime, end_time: datetime.datetime) -> Dict:
        """
        Creates a blocking calendar event.
        """
        calendar = self.store.defaultCalendarForNewEvents()
        event = self.store.eventWithEntityType_insertedInCalendar_(EKEntityTypeEvent, calendar)

        event.setTitle_(title)
        event.setStartDate_(NSDate.dateWithTimeIntervalSince1970_(start_time.timestamp()))
        event.setEndDate_(NSDate.dateWithTimeIntervalSince1970_(end_time.timestamp()))
        event.setCalendar_(calendar)

        success, error = self.store.saveEvent_span_error_(event, 0, None)
        if not success:
            raise RuntimeError(f"Failed to save event: {error}")

        return {
            "status": "created",
            "title": title,
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
        }

    def remove_event_by_title(self, title: str, window_days: int = 7) -> int:
        """
        Deletes events by title within the last and next `window_days` range.
        """
        now = datetime.datetime.now()
        start = now - datetime.timedelta(days=window_days)
        end = now + datetime.timedelta(days=window_days)
        events = self.list_events(start, end)

        count = 0
        for e in events:
            if e["title"] == title:
                predicate = self.store.predicateForEventsWithStartDate_endDate_calendars_(
                    NSDate.dateWithTimeIntervalSince1970_(start.timestamp()),
                    NSDate.dateWithTimeIntervalSince1970_(end.timestamp()),
                    None,
                )
                matched = self.store.eventsMatchingPredicate_(predicate)
                for event in matched:
                    if event.title() == title:
                        self.store.removeEvent_span_error_(event, 0, None)
                        count += 1
        return count
