const CACHE_NAME = 'sosie-spotify-cache-v1';
const urlsToCache = [
  '/',
  '/static/manifest.json',
  '/static/logo.svg',
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request).then(response => {
        // Optionnel : Mettre à jour le cache ici
        return response;
    }).catch(() => {
        // En cas d'échec (hors ligne), on cherche dans le cache
        return caches.match(event.request);
    })
  );
});
