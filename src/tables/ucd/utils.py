# ===------------------------------------------------------------------------===
# Distributed under the MIT License (See accompanying file LICENSE or copy at
# https://opensource.org/licenses/MIT).
# SPDX-License-Identifier: MIT
# ===------------------------------------------------------------------------===

"""Helper functions."""

import math

import requests
from tqdm import tqdm


def __recommend_block_size(total_size):
    """
    Estimate the block size to be used to read data from the request.

    Args:
        total_size (int): the total size of the data expected from the request

    Returns:
        int: recommended block size to read the data from teh request
    """
    min_block_size = 1024
    max_block_size = 1024 * 1024

    block_size = math.ceil(total_size / 100)
    block_size = max(block_size, min_block_size)
    block_size = min(block_size, max_block_size)

    return block_size


def request_sizes(url):
    """
    Estimate the total size of data that would be obtained through a http
    request and the block size to be used to read it.

    Args:
        url (string): the request url

    Returns:
        tuple(int, int): (total size, block size)
    """
    total_size = int(
        requests.head(url, headers={"accept-encoding": ""}).headers[
            "Content-Length"
        ]
    )
    block_size = __recommend_block_size(total_size)

    return total_size, block_size


def start_request(url):
    """Start the request to fetch teh data and start a progress bar for it."""

    [total_size_in_bytes, block_size] = request_sizes(url)

    response = requests.get(url, stream=True)
    response.raise_for_status()

    progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)

    return response, block_size, progress_bar
