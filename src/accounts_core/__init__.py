# SPDX-License-Identifier: MIT
"""accounts-core: neutral domain core for the account/bank-balance domain (BACH, OCEAN).

Wave 1 ships bank account CRUD, CAMT balance import, and a privacy-safe
read-only transit projection. ``credits`` (Kredite) stays out of wave 1 --
a related but separate domain, see the ``accounts`` module docstring.
"""
from .accounts import (
    DB_ENV,
    TRANSIT_FIELDS,
    AccountStore,
    default_db_path,
    mask_iban,
    to_transit_row,
)
from .transit_publisher import publish_transit_projection

__version__ = "0.1.0"
__all__ = [
    "DB_ENV",
    "TRANSIT_FIELDS",
    "AccountStore",
    "default_db_path",
    "mask_iban",
    "to_transit_row",
    "publish_transit_projection",
    "__version__",
]
