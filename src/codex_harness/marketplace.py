from __future__ import annotations

from .constants import NAME_RE


def marketplace_catalog(
    marketplace_name: str,
    display_name: str,
    plugin_name: str,
    plugin_source: str,
    category: str,
) -> dict[str, object]:
    if not NAME_RE.match(marketplace_name):
        raise ValueError("marketplace name must be lowercase hyphen-case")
    if not NAME_RE.match(plugin_name):
        raise ValueError("plugin name must be lowercase hyphen-case")
    if not plugin_source.startswith("./"):
        raise ValueError("plugin source must be a relative path beginning with ./")
    if not display_name.strip():
        raise ValueError("display name must not be empty")
    if not category.strip():
        raise ValueError("category must not be empty")

    return {
        "name": marketplace_name,
        "interface": {
            "displayName": display_name,
        },
        "plugins": [
            {
                "name": plugin_name,
                "source": {
                    "source": "local",
                    "path": plugin_source,
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": category,
            }
        ],
    }
