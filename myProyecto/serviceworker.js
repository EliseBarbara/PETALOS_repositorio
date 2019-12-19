//instalacion: al momento de instalar, hace cache de todas las urls que estimemos conveniente
var CACHE_NAME = 'my-site-cache-v1';
var urlsToCache = [
    '/',
    '/static/core/css/estilos_floreria.css',
    '/static/core/img/flor_inicio.jpg',
    '/static/core/img/floreria_banner.jpg',
    '/static/core/img/flores1.jpeg',
    '/static/core/img/fondo_nosotros.jpeg',
    '/static/core/img/lirio_flor.jpg',
];

//interceptacion: cada petición para saber si responde desde el servidor o del cache

self.addEventListener('install', function(event) {
    // Perform install steps
    event.waitUntil(
        caches.open(CACHE_NAME)
        .then(function(cache) {
            console.log('Opened cache');
            return cache.addAll(urlsToCache);
        })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        fetch(event.request) //hace la peticion (x ej, los productos que se cargan automaticamente por codigo)
        .then(function(result) { //intercepta la petición
            return caches.open(CACHE_NAME)
                .then(function(c) { //retorna una instancia del cache
                    c.put(event.request.url, result.clone()); //toma el dato interceptado y lo guarda en el cache - además, clona el dato para guardarlo en la memoria ram
                    return result;
                })
        })
        .catch(function(err) { //en caso de que falle
            return caches.match(event.request)
        })
    );
});