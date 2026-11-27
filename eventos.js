// Cliques no WhatsApp: evento "clique_whatsapp" para o Web Analytics da Vercel (painel da Central)
// e para o dataLayer (Google Tag Manager, quando instalado). "local" diz qual botão foi clicado.
document.addEventListener('click', function (e) {
  var a = e.target.closest && e.target.closest('a[href*="whatsapp.com"], a[href*="wa.me"]');
  if (!a) return;
  var local = a.closest('.top') ? 'topo'
    : a.closest('#contato') ? 'contato'
    : a.closest('footer') ? 'rodape'
    : location.pathname.indexOf('/cases') === 0 ? 'case'
    : 'outro';
  try { window.va && window.va('event', { name: 'clique_whatsapp', data: { local: local } }); } catch (_) {}
  try { (window.dataLayer = window.dataLayer || []).push({ event: 'clique_whatsapp', local: local }); } catch (_) {}
}, true);
