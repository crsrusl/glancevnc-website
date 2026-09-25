(() => {
  document.addEventListener('click', (event) => {
    const link = event.target.closest('a[href]');
    if (!link || event.defaultPrevented || typeof window.gtag !== 'function') return;

    const destination = new URL(link.href);
    if (destination.hostname !== 'apps.apple.com') return;

    const parameters = {
      link_url: link.href,
      cta_location: link.dataset.ctaLocation || 'other',
      page_path: window.location.pathname,
    };
    const navigatesCurrentTab = event.button === 0
      && !event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey
      && (!link.target || link.target === '_self') && !link.hasAttribute('download');

    if (navigatesCurrentTab) {
      event.preventDefault();
      let navigated = false;
      const navigate = () => {
        if (navigated) return;
        navigated = true;
        window.location.assign(link.href);
      };
      // Give GA time to send before leaving; blocked analytics must not block the link.
      window.setTimeout(navigate, 1000);
      parameters.event_callback = navigate;
      parameters.event_timeout = 1000;
    }

    window.gtag('event', 'app_store_click', parameters);
  });
})();
