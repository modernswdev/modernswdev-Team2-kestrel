// Minimal service worker: it only has to exist and handle fetches
// for the browser to treat PawLink as an installable app.
self.addEventListener("fetch", () => {});
