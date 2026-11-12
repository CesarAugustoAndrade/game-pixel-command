"""
Base entity class for ECS architecture.
"""

from typing import Dict, Any, Type, Optional


class Entity:
    """
    Base entity class in the ECS architecture.
    Entities are containers for components.
    """

    _next_id = 0

    def __init__(self):
        """Initialize entity with unique ID."""
        self.id = Entity._next_id
        Entity._next_id += 1

        self.components: Dict[Type, Any] = {}
        self.is_active = True

    def add_component(self, component: Any) -> None:
        """
        Add a component to this entity.

        Args:
            component: Component instance to add
        """
        component_type = type(component)
        self.components[component_type] = component

    def remove_component(self, component_type: Type) -> None:
        """
        Remove a component from this entity.

        Args:
            component_type: Type of component to remove
        """
        if component_type in self.components:
            del self.components[component_type]

    def get_component(self, component_type: Type) -> Optional[Any]:
        """
        Get a component of the specified type.

        Args:
            component_type: Type of component to get

        Returns:
            Component instance or None if not found
        """
        return self.components.get(component_type)

    def has_component(self, component_type: Type) -> bool:
        """
        Check if entity has a component of the specified type.

        Args:
            component_type: Type of component to check

        Returns:
            True if component exists
        """
        return component_type in self.components

    def destroy(self) -> None:
        """Mark entity as inactive and clear components."""
        self.is_active = False
        self.components.clear()
