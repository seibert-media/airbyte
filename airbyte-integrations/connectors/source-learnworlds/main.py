#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#


import sys

from airbyte_cdk.entrypoint import launch
from source_learnworlds import SourceLearnworlds

if __name__ == "__main__":
    source = SourceLearnworlds()
    launch(source, sys.argv[1:])
