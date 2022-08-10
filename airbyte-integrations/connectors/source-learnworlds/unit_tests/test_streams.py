#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from source_learnworlds.source import LearnworldsStream


@pytest.fixture
def patch_base_class(mocker):
    # Mock abstract methods to enable instantiating abstract class
    mocker.patch.object(LearnworldsStream, "path", "v0/example_endpoint")
    mocker.patch.object(LearnworldsStream, "primary_key", "test_primary_key")
    mocker.patch.object(LearnworldsStream, "__abstractmethods__", set())


def test_request_headers(patch_base_class):
    stream = LearnworldsStream(school_url="url", client_id="id")
    inputs = {"stream_slice": None,
              "stream_state": None, "next_page_token": None}
    expected_params = {"Lw-Client": "id"}
    assert stream.request_headers(**inputs) == expected_params


def test_next_page_token(patch_base_class):
    # TODO: NYI
    stream = LearnworldsStream(school_url="url", client_id="id")
    inputs = {"response": MagicMock()}
    expected_token = None
    assert stream.next_page_token(**inputs) == expected_token


def test_parse_response(patch_base_class):
    stream = LearnworldsStream(school_url="url", client_id="id")
    response = MagicMock()
    response.json = MagicMock(return_value={"data": ["foo"]})
    inputs = {"response": response, "stream_state": MagicMock()}
    expected_parsed_object = "foo"
    assert next(stream.parse_response(**inputs)) == expected_parsed_object


def test_http_method(patch_base_class):
    stream = LearnworldsStream(school_url="url", client_id="id")
    expected_method = "GET"
    assert stream.http_method == expected_method


@pytest.mark.parametrize(
    ("http_status", "should_retry"),
    [
        (HTTPStatus.OK, False),
        (HTTPStatus.BAD_REQUEST, False),
        (HTTPStatus.TOO_MANY_REQUESTS, True),
        (HTTPStatus.INTERNAL_SERVER_ERROR, True),
    ],
)
def test_should_retry(patch_base_class, http_status, should_retry):
    response_mock = MagicMock()
    response_mock.status_code = http_status
    stream = LearnworldsStream(school_url="url", client_id="id")
    assert stream.should_retry(response_mock) == should_retry


def test_backoff_time(patch_base_class):
    response_mock = MagicMock()
    stream = LearnworldsStream(school_url="url", client_id="id")
    expected_backoff_time = None
    assert stream.backoff_time(response_mock) == expected_backoff_time
