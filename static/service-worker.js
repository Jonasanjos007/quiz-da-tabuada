self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open('quiz-cache-v1').then((cache) => {
      return cache.addAll([
        '/',
        '/static/manifest.json',
        '/static/service-worker.js'
      ]);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter(k => k !== 'quiz-cache-v1').map(k => caches.delete(k))
      );
    })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
