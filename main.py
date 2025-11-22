#!/usr/bin/env python3
"""Main entry point for the Burnout & Office Syndrome Prevention App."""
import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import settings
from ui.app import create_app


def main():
    """Main function to run the application."""
    parser = argparse.ArgumentParser(
        description="Burnout & Office Syndrome Prevention App"
    )
    parser.add_argument(
        '--port',
        type=int,
        default=settings.GRADIO_SERVER_PORT,
        help=f'Port to run the server on (default: {settings.GRADIO_SERVER_PORT})'
    )
    parser.add_argument(
        '--host',
        type=str,
        default=settings.GRADIO_SERVER_NAME,
        help=f'Host to bind to (default: {settings.GRADIO_SERVER_NAME})'
    )
    parser.add_argument(
        '--share',
        action='store_true',
        default=settings.SHARE_GRADIO,
        help='Create a public share link'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        default=settings.DEBUG_MODE,
        help='Run in debug mode'
    )

    args = parser.parse_args()

    # Print welcome message
    print("=" * 60)
    print("🌟 Burnout & Office Syndrome Prevention App")
    print("=" * 60)
    print(f"Starting server on {args.host}:{args.port}")
    print(f"Database: {settings.DATABASE_PATH}")
    print(f"Data directory: {settings.DATA_DIR}")

    if not settings.ANTHROPIC_API_KEY:
        print("\n⚠️  Warning: ANTHROPIC_API_KEY not set!")
        print("   The app will work with limited AI features.")
        print("   Set your API key in .env file for full functionality.\n")

    print("=" * 60)
    print("Ready! Open your browser to start your wellness journey! 🚀")
    print("=" * 60)

    # Create and launch the app
    try:
        app = create_app()
        app.launch(
            server_name=args.host,
            server_port=args.port,
            share=args.share,
            debug=args.debug
        )
    except KeyboardInterrupt:
        print("\n\nShutting down gracefully... 👋")
        print("Remember to take care of yourself! 💚")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        if args.debug:
            raise
        sys.exit(1)


if __name__ == "__main__":
    main()
