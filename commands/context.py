"""
Context object that provides access to Fusion 360 application objects.
"""

import adsk.core
import adsk.fusion


class CommandContext:
    """
    Provides access to common Fusion 360 objects for command handlers.

    Attributes:
        app: The Fusion 360 Application object
        ui: The UserInterface object
        design: The active Design (may be None)
        root: The root component (if design exists)
        sketches: The sketches collection (if design exists)
        extrudes: The extrude features collection (if design exists)
    """

    def __init__(self, app, ui):
        self.app = app
        self.ui = ui
        self._design = None
        self._root = None

    @property
    def design(self):
        """Get the active design, refreshed each access."""
        return adsk.fusion.Design.cast(self.app.activeProduct)

    @property
    def root(self):
        """Get the root component of the active design."""
        design = self.design
        return design.rootComponent if design else None

    @property
    def sketches(self):
        """Get the sketches collection from root component."""
        root = self.root
        return root.sketches if root else None

    @property
    def extrudes(self):
        """Get the extrude features collection from root component."""
        root = self.root
        return root.features.extrudeFeatures if root else None

    def require_design(self):
        """
        Check if a design is active.

        Returns:
            tuple: (success: bool, error_message: str or None)
        """
        if not self.design:
            return False, "No active design"
        return True, None
