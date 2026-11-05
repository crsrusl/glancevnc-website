(() => {
  const tabs = Array.from(document.querySelectorAll('[data-platform]'));
  const panels = Array.from(document.querySelectorAll('[data-platform-panel]'));
  const tabList = document.querySelector('.platform-tabs');
  if (tabList && tabs.length && panels.length) {
    tabList.setAttribute('role', 'tablist');
    tabList.setAttribute('aria-label', 'Computer setup');
    const select = (tab, focus = false) => {
      tabs.forEach((item) => {
        const active = item === tab;
        item.setAttribute('role', 'tab');
        item.setAttribute('aria-selected', String(active));
        item.tabIndex = active ? 0 : -1;
      });
      panels.forEach((panel) => {
        panel.setAttribute('role', 'tabpanel');
        panel.setAttribute('aria-labelledby', `tab-${panel.dataset.platformPanel}`);
        panel.tabIndex = 0;
        panel.hidden = panel.dataset.platformPanel !== tab.dataset.platform;
      });
      if (focus) tab.focus();
    };
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => select(tab));
      tab.addEventListener('keydown', (event) => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        if (next !== undefined) {
          event.preventDefault();
          select(tabs[next], true);
        }
      });
    });
    select(tabs[0]);
    tabList.hidden = false;
  }

  const input = document.querySelector('#faq-query');
  const clear = document.querySelector('#clear-search');
  const status = document.querySelector('#search-status');
  const empty = document.querySelector('#empty-search');
  const items = Array.from(document.querySelectorAll('.faq-item'));
  const groups = Array.from(document.querySelectorAll('.faq-group'));
  if (input && clear && status && empty && items.length) {
    document.querySelector('.faq-search').hidden = false;
    const filter = () => {
      const words = input.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
      let count = 0;
      items.forEach((item) => {
        const text = item.textContent.toLocaleLowerCase();
        const matches = words.every((word) => text.includes(word));
        item.hidden = !matches;
        if (words.length) item.open = matches;
        else item.open = item.id === location.hash.slice(1);
        if (matches) count++;
      });
      groups.forEach((group) => {
        group.hidden = !Array.from(group.querySelectorAll('.faq-item')).some((item) => !item.hidden);
      });
      clear.hidden = !words.length;
      empty.hidden = count > 0;
      status.textContent = words.length ? `${count} ${count === 1 ? 'answer' : 'answers'} found` : `${items.length} answers, organised by topic`;
    };
    input.addEventListener('input', filter);
    clear.addEventListener('click', () => { input.value = ''; filter(); input.focus(); });
    const revealHash = () => {
      const target = document.getElementById(location.hash.slice(1));
      if (!target) return;
      if (input.value) { input.value = ''; filter(); }
      if (target.matches('.faq-item')) target.open = true;
      requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
    };
    window.addEventListener('hashchange', revealHash);
    filter();
    if (location.hash) revealHash();
  }
})();
