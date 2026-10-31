# Sun Devil Rocketry Documentation Server

This repository publishes the documentation site to GitHub Pages.

During deployment, the workflow copies the repository to a site artifact and
generates an `index.html` for every directory that does not supply one,
including the artifact root. Existing index pages are never replaced.
Generated pages link to all files and subdirectories so the library remains
browsable on a static host. Folders without an index are expandable and use a
folder icon with a trailing `/`; folders that supplied their own `index.html`
use a web icon, omit the trailing `/`, and link directly to that page.

To build the same artifact locally, run:

```shell
python scripts/build_site.py . _site
```

To add new contents to the top level, just add a folder with your documentation! Metadata used to generate the site is filtered out.