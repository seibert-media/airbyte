#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

from unittest.mock import MagicMock, patch

import requests
from source_learnworlds.source import SourceLearnworlds


@patch.object(requests, 'get')
def test_check_connection(mocker):
    response = MagicMock()
    response.json = MagicMock(return_value={"data": []})
    mocker.return_value = response
    source = SourceLearnworlds()
    logger_mock, config_mock = MagicMock(), MagicMock()
    assert source.check_connection(logger_mock, config_mock) == (True, None)


def test_streams(mocker):
    source = SourceLearnworlds()
    config_mock = MagicMock()
    streams = source.streams(config_mock)
    expected_streams_number = 1
    assert len(streams) == expected_streams_number
