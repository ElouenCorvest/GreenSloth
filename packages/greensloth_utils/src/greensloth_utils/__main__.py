import argparse
from greensloth_utils import installerfuncs


def main():
    parser = argparse.ArgumentParser(description="Install the GreenSloth pipeline.")
    parser.add_argument("model_name", help="Name of the model to install.")
    parser.add_argument("target_dir", help="Target directory for installation.", nargs='?', default=None)

    args = parser.parse_args()
    installerfuncs.gs_install(args.model_name, args.target_dir)


if __name__ == "__main__":
    main()
