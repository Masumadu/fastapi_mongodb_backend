from app.core.notifications import NotificationHandler


class EventNotificationHandler(NotificationHandler):
    """
    Event Notification handler
    this class handles event notification. It publishes an Event message to
    the message queue which is consumed by the rightful service.
    """

    def send(self):
        pass
