# skfd.github.io

Redirects for sites that used to live at `skfd.github.io/<repo>/` and moved to an
organisation (`guelph-maps`, `toronto-maps`).

GitHub redirects `github.com/skfd/<repo>` after a transfer, but not the Pages site: the old
address just returns 404. GitHub Pages serves this repo's `404.html` for any
`skfd.github.io` path with no site behind it, and the script in it sends the browser to the
same path, query and fragment on the organisation's host.

## Adding a moved repo

Add its name to the organisation's list in `MOVED` at the top of `404.html`, after the
transfer and once the new site answers. Listing a repo that still has a site under `skfd`
does nothing; Pages never reaches `404.html` for it.

## What it cannot do

- The response is still HTTP 404. Browsers follow the script; crawlers, link checkers and
  anything fetching a file directly (`curl`, a tile request from iD or JOSM) do not.
- So tile URLs (`.../tiles/{z}/{x}/{y}.png`) under the old host stay broken. Only pages
  redirect.

There is deliberately no `index.html`: the root has no content of its own.
