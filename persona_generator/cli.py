"""
Command-line interface for the persona generator.
"""

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

from .factories.persona_factory import PersonaFactory


def load_environment():
    """Load environment variables from .env file if it exists."""
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(env_path)
        print("✅ Loaded environment variables from .env file")
    else:
        print("⚠️  No .env file found. Using system environment variables.")
    
    # Check if OpenAI API key is available
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found!")
        print("   Please set your OpenAI API key in one of these ways:")
        print("   1. Create a .env file with: OPENAI_API_KEY=your_key_here")
        print("   2. Export it: export OPENAI_API_KEY=your_key_here")
        print("   3. Set it in your shell profile (~/.bashrc, ~/.zshrc, etc.)")
        raise ValueError("OPENAI_API_KEY environment variable is required")


def get_package_path():
    """Get the path to the installed package."""
    import persona_generator
    return Path(persona_generator.__file__).parent


def parse_arguments():
    """Parse command line arguments."""
    package_path = get_package_path()
    default_schema = package_path / "schemas" / "default_schema.yaml"
    default_config = package_path / "generators" / "config" / "generator_config.yaml"
    
    parser = argparse.ArgumentParser(
        description="Generate personas using OpenAI",
        epilog="""
Environment Variables:
  OPENAI_API_KEY    Your OpenAI API key (required)
  
Examples:
  # Generate 1 persona with default settings
  persona-generator
  
  # Generate 5 personas
  persona-generator -n 5
  
  # Use custom schema and config
  persona-generator -s my_schema.yaml -c my_config.yaml
  
  # Export as YAML format
  persona-generator -f yaml -o my_personas
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-n",
        "--num-personas",
        type=int,
        default=1,
        help="Number of personas to generate (default: 1)",
    )
    parser.add_argument(
        "-s",
        "--schema",
        type=str,
        default=str(default_schema),
        help=f"Path to schema file (default: {default_schema})",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default=str(default_config),
        help=f"Path to generator config file (default: {default_config})",
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        choices=["json", "yaml"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default="export",
        help="Directory where exported files will be saved (default: export)",
    )
    return parser.parse_args()


def main():
    """Main application workflow."""
    try:
        # Parse command line arguments
        args = parse_arguments()

        # Step 1: Load environment variables
        print("Loading environment variables...")
        load_environment()

        # Step 2: Initialize factory and verify connection
        print("Initializing persona factory...")
        factory = PersonaFactory(
            schema_path=args.schema,
            output_format=args.format,
            config_path=args.config,
            output_dir=args.output_dir,
        )
        if not factory.verify_connection():
            raise ConnectionError("Failed to connect to OpenAI API")
        print("✅ OpenAI connection verified!")

        # Step 3: Generate and export personas
        print(f"Generating {args.num_personas} persona(s)...")
        factory.generate_and_export(args.num_personas)

        print("\nApplication workflow completed successfully!")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return


if __name__ == "__main__":
    main()
