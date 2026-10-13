<p align="center"><img src="res/logo.svg" width="96" alt="SevenDesk"></p>

# SevenDesk

Assistenza remota di [Sevenix](https://sevenix.it).

## Varianti

| Variante | Per chi | Build |
| --- | --- | --- |
| **SevenDesk** | staff Sevenix: controlla e può essere controllato | Windows, macOS, Linux, Android |
| **SevenDesk Supporto** | clienti: accetta solo connessioni in entrata, si avvia senza installazione | Windows (`.exe` portabile), macOS (`.dmg`), Linux (`.tar.gz` portabile: si estrae e si lancia `./sevendesk`) |

La variante si sceglie a compile time: `SEVENDESK_VARIANT=supporto` nell'ambiente di
`cargo build` produce la build Supporto (`src/sevenix.rs`).

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

`.github/workflows/sevendesk.yml` (PR, manuale, o push di un tag `v*`, che crea la release nel
repo **privato** `7evenix/sevendesk-dist`: i binari contengono la chiave del server e questo repo
è pubblico, quindi qui non si pubblicano, e gli artifact dei run scadono dopo un giorno. La release
usa il secret `DIST_TOKEN`, un token fine-grained limitato a `sevendesk-dist`, Contents: read and
write):
Windows completo e Supporto, Linux `.deb` e `.rpm` (`res/sevenix/rpm-flutter.spec`), Android arm64,
macOS x86_64/arm64 non firmato.

Host e chiave del server non sono nel sorgente: la CI li passa a `cargo` dalla variabile di
repository `SEVENDESK_SERVER` e dal secret `SEVENDESK_KEY`, e il job di release verifica che la
chiave sia nel binario prima di pubblicare. Una build senza (fork, build locale) non usa il server
Sevenix.

## Server

`server/compose.yaml` avvia hbbs e hbbr (rustdesk-server open source) con rete host:
firewalld decide cosa è raggiungibile. Porte pubbliche: 21115-21117/tcp e 21116/udp.
Il record `desk.sevenix.it` deve essere DNS-only (Cloudflare non inoltra queste porte).

La coppia di chiavi sta nel volume `sevendesk-data` (il backup notturno di Atlas ne tiene una
copia cifrata). La pubblica è compilata nel client: se la privata va persa, tutti i client vanno
ricompilati.

Chi può usare il server: hbbs/hbbr partono con `-k _` e rifiutano i client senza la chiave. Il
server open source non ha login, e la chiave si può estrarre da qualunque binario distribuito:
filtra i client RustDesk qualsiasi e le build dei fork, non chi la estrae apposta. Nessuno entra
in un PC senza la sua password (e, con la variante Supporto, senza il click del cliente); il
rischio è l'uso della banda del relay.

- `server/peers.sh [giorni]` elenca i dispositivi registrati (ID, prima registrazione, IP).
  ID sconosciuti o un salto nel numero vogliono dire che qualcun altro usa il server.
- Ruotare la chiave: ferma lo stack, sposta `id_ed25519*` nel volume, riavvia (hbbs ne genera
  una nuova, letta anche da hbbr), aggiorna il secret `SEVENDESK_KEY`, rilascia una nuova
  versione e reinstalla i client: quelli vecchi vengono rifiutati.

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

AGPL-3.0, (vedi [LICENCE](LICENCE)). Copyright © Purslane Tech Pte. Ltd.
per il codice originale; le modifiche sono di Sevenix. Il repository è pubblico, chi riceve
un binario SevenDesk (anche la variante Supporto) ha diritto al sorgente corrispondente.
