#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#


import sys

from destination_duckdb import DestinationDuckdb

if __name__ == "__main__":
    DestinationDuckdb().run(sys.argv[1:])
