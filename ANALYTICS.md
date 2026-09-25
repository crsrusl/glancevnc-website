# Website acquisition funnel

The existing GA4 configuration (`G-DS4RF91ZXC`) automatically sends `page_view`
on every page load. Do not add another page-view event for the funnel.

`assets/analytics.js` sends `app_store_click` when a visitor activates an App
Store link, including clicks on its badge image and keyboard activation. It sends:

- `cta_location`: `hero`, `download`, or `guide` for the current buttons.
- `page_path`: the page containing the link.
- `link_url`: the App Store destination.

Normal same-tab navigation waits for the GA callback, with a one-second fallback
if analytics is blocked. Modified clicks keep the browser's normal behaviour.
The standard enhanced-measurement outbound `click` event may also exist; use only
`app_store_click` for the second funnel stage to avoid mixing the two events.

## Configure the report in Google Analytics

1. Open the website's GA4 property and select **Explore → Funnel exploration**.
2. Use a closed funnel (leave **Make open funnel** off).
3. Add step **Website visit** with event name exactly `page_view`. To measure only
   homepage visits, also filter Page location using the regular expression
   `^https://(www\.)?glancevnc\.com/(index\.html)?([?#].*)?$`.
   Use the actual production hostname if it differs.
4. Add step **App Store click** with event name exactly `app_store_click`,
   indirectly following the first step so other browsing can occur in between.
5. Save the exploration. Optionally mark `app_store_click` as a key event.
6. For button placement reports, create an event-scoped custom dimension named
   **CTA location** for event parameter `cta_location`.

This measures visits followed by App Store clicks, not downloads or purchases.
A guide visitor who later visits the homepage generates multiple page views;
GA's funnel reports users progressing through the steps, not raw event totals.

## Verify after publishing

With Google Tag Assistant connected, open the homepage and check GA4 DebugView
for `page_view`. Click each of the two App Store badges and the guide badge;
verify `app_store_click` and its expected `cta_location` before the store opens.
Confirm that the link still opens with analytics blocked. Realtime can also be
used to check that events arrive; standard reports can take time to populate.

References:
- https://developers.google.com/analytics/devguides/collection/ga4/events
- https://support.google.com/analytics/answer/9327974
