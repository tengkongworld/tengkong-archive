import json

with open("config/archive.config.json", "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

COLLECTIONS = CONFIG.get("collections", {})


def get_collection_default_view(name):
    """Return the default view for a collection."""
    return get_collection(name).get("default_view", "list")


def get_collection_default_sort(name):
    """Return the default sort order for a collection."""
    return get_collection(name).get("default_sort", "asc")


def get_collection(name):
    """Return a collection config by name, or an empty config."""
    collection = COLLECTIONS.get(name, {})

    if isinstance(collection, dict):
        return collection

    return {}


def get_collection_view(name):
    """Return the configured collection view, defaulting to list."""
    return get_collection(name).get("view", "list")


def show_in_exhibition(name):
    """Return whether a collection should appear in exhibitions."""
    return bool(get_collection(name).get("show_in_exhibition", False))


def is_homepage_collection(name):
    """Return whether a collection is marked for the homepage."""
    return bool(get_collection(name).get("homepage", False))


GALLERY_LABELS = CONFIG.get(
    "gallery_labels",
    [
        name
        for name in COLLECTIONS
        if (
            get_collection_view(name) == "gallery"
            or get_collection_default_view(name) == "gallery"
        )
    ],
)

DIGITAL_EXHIBITION = CONFIG.get(
    "digital_exhibition",
    [name for name in COLLECTIONS if show_in_exhibition(name)],
)

FEATURED_LABELS = CONFIG.get("featured_labels", [])

HOMEPAGE_RECOMMENDATIONS = CONFIG.get("homepage_recommendations", [])
