<p align="center"><img src="res/logo.svg" width="96" alt="SevenDesk"></p>

# SevenDesk

Assistenza remota di [Sevenix](https://sevenix.it). È una versione modificata di
[RustDesk](https://github.com/rustdesk/rustdesk) (AGPL-3.0) che si collega solo al
server Sevenix `desk.sevenix.it`.

## Varianti

| Variante | Per chi | Build |
| --- | --- | --- |
| **SevenDesk** | staff Sevenix: controlla e può essere controllato | Windows, macOS, Linux, Android |
| **SevenDesk Supporto** | clienti: accetta solo connessioni in entrata, si avvia senza installazione | Windows |

La variante si sceglie a compile time: `SEVENDESK_VARIANT=supporto` nell'ambiente di
`cargo build` produce la build Supporto (`src/sevenix.rs`).

## Cosa cambia rispetto a RustDesk

- `src/sevenix.rs`: nome app, server e chiave pubblica, restrizioni (niente account,
  rubrica né registrazione del dispositivo: il server open source non ha API).
  È applicato da `load_custom_client()` all'avvio di ogni processo, quindi le impostazioni
  non si possono cambiare dall'interfaccia.
- `flutter/lib/sevenix.dart` e `MyTheme` in `flutter/lib/common.dart`: link e colori Sevenix.
- Icone (`res/`, `flutter/assets/icon.svg`, Android, macOS, Windows), generate dal
  favicon di sevenix.it.
- Nomi visibili: metadati Windows (`Runner.rc`), `SevenDesk.app` / `it.sevenix.sevendesk`
  su macOS, label e `applicationId` su Android, file `.desktop` su Linux, schema URL
  `sevendesk://`.
- Eseguibile `sevendesk` (Windows e Linux): il codice cerca processi, servizio systemd e file
  `.desktop` col nome dell'app in minuscolo. La CI rinomina `rustdesk.exe` prima del pacchetto
  portabile e rimpacchetta il `.deb` con `res/sevenix/repack-deb.sh`; `build.py` e `librustdesk`
  restano quelli di upstream. L'installer Windows installa `SevenDesk.exe`.

## Icone

Generate dal favicon di sevenix.it (il "7" di JetBrains Mono 600 convertito in tracciato) con
`res/sevenix/icons` (immagine Docker con fontTools, rsvg e ImageMagick):

```sh
docker build -t sevendesk-icons res/sevenix/icons
docker run --rm --user "$(id -u):$(id -g)" -v "$PWD/res/sevenix/icons":/tool:ro,z \
  -v /tmp/svg:/out:z -v <cartella con jetbrains-mono-latin-wght-normal.woff2>:/fonts:ro,z \
  -v "$PWD":/repo:z sevendesk-icons /tool/render.sh /fonts/jetbrains-mono-latin-wght-normal.woff2 /out /repo
```

## Build

`.github/workflows/sevendesk.yml` (manuale o al push di un tag `v*`, che crea la release):
Windows completo e Supporto, Linux `.deb` e `.rpm` (`res/sevenix/rpm-flutter.spec`), Android arm64. macOS (x86_64/arm64, non firmato) solo
lanciandolo a mano con `macos=true`: nel repo privato i minuti macOS contano 10×. I `.dmg`
restano negli artifact del run, non nella release.

## Server

`server/compose.yaml` avvia hbbs e hbbr (rustdesk-server open source) con rete host:
firewalld decide cosa è raggiungibile. Porte pubbliche: 21115-21117/tcp e 21116/udp.
Il record `desk.sevenix.it` deve essere DNS-only (Cloudflare non inoltra queste porte).

La coppia di chiavi sta nel volume `sevendesk-data`. La pubblica è compilata nel client:
se la privata va persa, tutti i client vanno ricompilati. Tienine una copia offline.

## Aggiornare da upstream

```sh
git fetch upstream --tags
git merge <tag upstream>   # es. 1.5.2
```

I workflow di upstream con trigger automatici (`ci`, `flutter-ci`, `flutter-nightly`,
`flutter-tag`, `fdroid`, `playground`) sono rimossi: se un merge li riporta in conflitto,
risolvi con `git rm`. Restano `flutter-build.yml` (riferimento per aggiornare `sevendesk.yml`),
`bridge.yml` e `third-party-RustDeskTempTopMostWindow.yml`, che `sevendesk.yml` richiama.
Dopo un merge, allinea `VERSION` in `sevendesk.yml` alla versione di `Cargo.toml`.

## Licenza

AGPL-3.0, come RustDesk (vedi [LICENCE](LICENCE)). Copyright © Purslane Tech Pte. Ltd.
per il codice originale; le modifiche sono di Sevenix. Il repository è privato, ma chi riceve
un binario SevenDesk (anche la variante Supporto) ha diritto al sorgente corrispondente: va
fornito su richiesta a info@sevenix.it, come dice la schermata Informazioni.
