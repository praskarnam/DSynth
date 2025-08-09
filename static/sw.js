// Service Worker for DSynth
// This is a minimal service worker to prevent 404 errors

const CACHE_NAME = 'dsynth-v1';
const urlsToCache = [
  '/static/style.css',
  '/static/app.js'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        // Only cache files that actually exist
        return Promise.allSettled(
          urlsToCache.map(url => 
            cache.add(url).catch(err => {
              console.log('Failed to cache:', url, err);
              return null;
            })
          )
        );
      })
      .catch(err => {
        console.log('Service worker install failed:', err);
      })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Return cached version or fetch from network
        return response || fetch(event.request).catch(err => {
          console.log('Fetch failed:', event.request.url, err);
          // Return a fallback response for critical resources
          if (event.request.url.includes('/static/')) {
            return new Response('', { status: 404, statusText: 'Not Found' });
          }
          return new Response('', { status: 500, statusText: 'Internal Server Error' });
        });
      })
      .catch(err => {
        console.log('Cache match failed:', err);
        // Fallback to network request
        return fetch(event.request).catch(err => {
          console.log('Network fetch also failed:', err);
          return new Response('', { status: 500, statusText: 'Service Unavailable' });
        });
      })
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
}); 