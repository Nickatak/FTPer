"""Miscellaenous helpers (mostly URL-builders)."""
import os

from bot.types import UUID
from conf import DOMAIN_NAME, UPLOAD_DIR


def construct_upload_link(uuid: UUID) -> str:
    """Helper method to construct a url to our upload-route with a UUID."""

    return 'http://{}/{}'.format(DOMAIN_NAME, uuid)

def construct_download_link(uuid: UUID) -> str:
    """Helper method to construct a url to our download-route with a UUID."""

    return 'http://{}/download/{}'.format(DOMAIN_NAME, uuid)

def cleanup_file(uuid: UUID, ext: str) -> None:
    """Deletes file on disk associated with the File object."""

    try:
        os.remove(UPLOAD_DIR.joinpath('{}{}'.format(uuid.hex, ext)))
    except FileNotFoundError:
        # This happens because I'm debugging.  In theory, this should never happen really (unless the server is forcefully terminated or something).  I'm not a fan of capturing an error and doing nothing, so maybe I'll add something here later.
        pass
