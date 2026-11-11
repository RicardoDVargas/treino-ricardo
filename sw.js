const CACHE = 'ricardo-workout-v4';
const ASSETS = ['./','./index.html','./style.css','./app.js','./workouts.json','./manifest.webmanifest','./icon.svg','./icon-192.png','./icon-512.png','./stars.svg','./fonts/cormorant-garamond-latin-500-normal.woff2','./fonts/cormorant-garamond-latin-600-normal.woff2','./fonts/manrope-latin-wght-normal.woff2'];
self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    const response = await fetch('./workouts.json');
    if (!response.ok || response.redirected) throw new Error('Treino indisponível');
    const days = await response.json();
    const images = [...new Set(days.flatMap(day => day.exercises.map(exercise => `./images/${exercise.image}.svg`)))];
    await cache.addAll([...ASSETS, ...images]);
    await self.skipWaiting();
  })());
});
self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    for (const key of await caches.keys()) if (key.startsWith('ricardo-workout-') && key !== CACHE) await caches.delete(key);
    await self.clients.claim();
  })());
});
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (event.request.method !== 'GET' || url.origin !== self.location.origin) return;
  event.respondWith((async () => {
    try {
      const response = await fetch(event.request);
      return response;
    } catch {
      const cached = await caches.match(event.request);
      if (cached) return cached;
      if (event.request.mode === 'navigate') return (await caches.match('./index.html')) || Response.error();
      return Response.error();
    }
  })());
});
