# trendtrack-usage

_This skill was installed by the trendtrack app and is read-only._

# TrendTrack

Ecommerce intelligence: Shopify stores, Meta and TikTok ads, email campaigns, brand tracking.

## Credits

Every returned row costs one credit (10,000/month per workspace). Before a broad sweep, check the balance with the usage tool, and keep `limit` small on the first call: widen only once the filters are proven. Metered responses carry `X-Credits-Remaining`. The identity, workspace and usage tools are free.

## Working the data

- `search_shops` filters stores by niche, country, traffic and growth. It carries additive TikTok presence fields, but linked advertisers and the ad endpoints stay Meta/Facebook only.
- `search_tiktok_library` is the separate door for TikTok creatives (ads and organic).
- For "top ads of the last 7 days", filter on the 7-day scaling fields (`reachDelta7d`, `last7d`, `minReach`), not on a first-seen date.
- `list_favorites` returns saved items: ad ids are numeric, shop and email ids are UUIDs.

## Writes

Brandtracker and favorites writes exist (`add_to_brandtracker`, `create_brandtracker_folder`, `move_tracked_brands`, `create_favorite_folder`, `add_favorite_item`, share links). Destructive tools require `confirm: true`; never pass it without the user asking for the deletion. On `delete_brandtracker_folder`, `action: "move_to_default"` is the safe default, `"delete_tracked_brands"` deactivates the trackers.