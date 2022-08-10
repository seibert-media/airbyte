import json
from abc import ABC
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Tuple

import requests
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http import HttpStream
from airbyte_cdk.sources.streams.http.auth import TokenAuthenticator


class LearnworldsStream(HttpStream, ABC):

    url_base = None

    def __init__(self, school_url: str, client_id: str, **kwargs):
        super().__init__(**kwargs)
        self.url_base = f"{school_url}/admin/api"
        self.client_id = client_id

    def request_headers(self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None) -> Mapping[str, Any]:
        return {"Lw-Client": self.client_id}

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        return None

    def parse_response(
            self,
            response: requests.Response,
            stream_state: Mapping[str, Any],
            stream_slice: Mapping[str, Any] = None,
            next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        yield from (response.json()).get("data", [])


class Users(LearnworldsStream):

    primary_key = "id"

    def path(self, **kwargs) -> str:
        return "v2/users"

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        current_page = response.json().meta.page
        if response.json().meta.totalPages == current_page:
            return None
        return {"page": current_page + 1}


class SourceLearnworlds(AbstractSource):
    def check_connection(self, logger, config) -> Tuple[bool, any]:
        r = requests.get(
            f"{config['school_url']}/admin/api/v2/users",
            headers={
                "Lw-Client": config["client_id"],
                "Authorization": f"Bearer {config['access_token']}"
            },
        )
        response = r.json()

        if "data" in response:
            return True, None

        error_messages = map(
            lambda error: error.get('message'),
            response.get('errors')
        )
        return False, f"Here's what LearnWorlds returned: {', '.join(error_messages)}"

    def streams(self, config: Mapping[str, Any]) -> List[Stream]:
        return [
            Users(
                authenticator=TokenAuthenticator(config["access_token"]),
                school_url=config["school_url"],
                client_id=config["client_id"]
            )
        ]
