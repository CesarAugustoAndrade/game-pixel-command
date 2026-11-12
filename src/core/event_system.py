"""
Event bus system for decoupled communication between game systems.
"""

from typing import Callable, Dict, List, Any


class EventSystem:
    """
    Central event bus for game-wide communication.
    Allows systems to communicate without direct dependencies.
    """

    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable) -> None:
        """
        Subscribe a callback function to an event type.

        Args:
            event_type: The type of event to listen for
            callback: Function to call when event is emitted
        """
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """
        Unsubscribe a callback from an event type.

        Args:
            event_type: The event type to unsubscribe from
            callback: The callback to remove
        """
        if event_type in self._listeners:
            if callback in self._listeners[event_type]:
                self._listeners[event_type].remove(callback)

    def emit(self, event_type: str, data: Any = None) -> None:
        """
        Emit an event to all subscribed listeners.

        Args:
            event_type: The type of event to emit
            data: Optional data to pass to listeners
        """
        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                callback(data)

    def clear_event(self, event_type: str) -> None:
        """Clear all listeners for a specific event type."""
        if event_type in self._listeners:
            self._listeners[event_type].clear()

    def clear_all(self) -> None:
        """Clear all event listeners."""
        self._listeners.clear()


# Common event types
EVENT_UNIT_DIED = "unit_died"
EVENT_UNIT_MOVED = "unit_moved"
EVENT_UNIT_ATTACKED = "unit_attacked"
EVENT_MORALE_CHANGED = "morale_changed"
EVENT_TURN_START = "turn_start"
EVENT_TURN_END = "turn_end"
EVENT_BATTLE_START = "battle_start"
EVENT_BATTLE_END = "battle_end"
EVENT_STATE_CHANGED = "state_changed"
EVENT_PLAYER_ACTION = "player_action"
