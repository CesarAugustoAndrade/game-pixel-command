"""
Main entry point for Classical Army Roguelite.
"""

import sys
from src.core.game import Game
from src.states.main_menu import MainMenuState


def main():
    """Main entry point."""
    print("Starting Classical Army Roguelite...")

    try:
        # Create game instance
        game = Game()

        # Initialize and set initial state
        game.initialize()

        # Set main menu as initial state
        main_menu = MainMenuState(game.state_manager, game.engine)
        game.state_manager.push_state(main_menu)

        # Run game loop
        game.run()

    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
