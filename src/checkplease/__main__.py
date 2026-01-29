"""Entry point for the checkplease application."""
import argparse
import logging
import sys

from checkplease import app,load_config, log


def main():
    parser = argparse.ArgumentParser(prog="checkplease", description="%(prog)s is a CLI for making REST requests and diff'ing responses.")
    parser.add_argument("-c", "--config", help="Show the current configuration and exit.", action="store_true")
    parser.add_argument("-j", "--json", help="Compare JSON responses only. Normally, both JSON and XML are compared.", action="store_true")
    parser.add_argument("-d", "--debug", help="Enable debugging output.", action="store_true")
    parser.add_argument("-x", "--xml", help="Compare XML responses only. Normally, both JSON and XML are compared.", action="store_true")

    args = parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)
        log.debug("Debugging output enabled.")

    config = load_config()

    if args.json:
        config.compare.only_json()

    if args.xml:
        config.compare.only_xml()

    if args.config:
        print("Current Configuration:")
        print
        print("\t{0:<8s}".format(f"{config.show_config()}"))
        sys.exit(0)
    
    app.run(config)

if __name__ == "__main__":
    main()