# cache-stampede-replay

## Français

Comparer cache simple, verrou et renouvellement anticipé sur une même trace.

Données fictives ; aucun accès réseau ni secret requis.

```sh
python -m cache_stampede_replay examples/demo.json --lang fr
python -m unittest discover -s tests -v
```

### Méthode et différence

Rejoue la même trace d’arrivées avec cache naïf, coalescence et renouvellement anticipé. Modèle événementiel : fin de chargement avant arrivée au même instant, durée de vie après chargement, attente partagée et rafraîchissement déclenché par une requête.

### Limites

Simulation à durée de chargement constante sans panne ni coût de synchronisation réel. Aucun Redis, CDN ou serveur natif ; les gains simulés ne mesurent pas une performance de production.

### Validation

Tests de domaine, cas limites et interface FR/EN/ES. La CI teste Python 3.11/3.13 et exécute la wheel installée hors du checkout. JSON conserve les identifiants techniques et les données fournis. Erreur d’entrée : code de sortie 2.

## English

Compare plain cache, singleflight and early refresh on one trace.

Synthetic data; no network access or secret required.

```sh
python -m cache_stampede_replay examples/demo.json --lang en
python -m unittest discover -s tests -v
```

### Method and difference

Replays one arrival trace through plain caching, singleflight and early refresh. Event model specifies completion before same-time arrival, TTL after loading, shared waits and request-triggered refresh.

### Limits

Constant-load-time simulation without failures or actual synchronization overhead. No native Redis, CDN or server; simulated gains do not measure production performance.

### Validation

Domain tests, boundary cases and FR/EN/ES interface. CI tests Python 3.11/3.13 and runs the installed wheel outside the checkout. JSON preserves technical identifiers and supplied data. Invalid input exits with code 2.

## Español

Comparar caché simple, bloqueo y renovación anticipada en una traza.

Datos sintéticos; no requiere red ni secretos.

```sh
python -m cache_stampede_replay examples/demo.json --lang es
python -m unittest discover -s tests -v
```

### Método y diferencia

Reproduce una traza de llegadas con caché simple, singleflight y renovación anticipada. Modelo especifica fin de carga antes de llegada simultánea, TTL posterior, esperas compartidas y renovación disparada por consulta.

### Límites

Simulación de carga constante sin fallos ni coste real de sincronización. Sin Redis, CDN ni servidor nativo; ganancias simuladas no miden rendimiento de producción.

### Validación

Pruebas de dominio, casos límite e interfaz FR/EN/ES. CI prueba Python 3.11/3.13 y ejecuta la wheel instalada fuera del repositorio. JSON conserva identificadores técnicos y datos proporcionados. Entrada inválida termina con código 2.

## Sources / Fuentes

- https://github.com/golang/sync/tree/master/singleflight
