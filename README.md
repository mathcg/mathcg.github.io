# Gang Cheng — Personal Website

Source for [mathcg.github.io](https://mathcg.github.io/), a dependency-free personal academic website.
The layout uses a compact academic masthead and profile sidebar inspired by
the information architecture of [zhangyk8.github.io](https://zhangyk8.github.io/),
with an original visual implementation and content.

The profile photograph is a local high-resolution copy of Gang Cheng's
University of Washington graduation portrait.

## Local preview

```sh
python3 -m http.server 8000
```

Then visit <http://localhost:8000>.

An optional Playwright smoke test lives in `tests/browser_check.py`. With the
site running on port 8000 and Playwright installed, run:

```sh
python tests/browser_check.py
```

## Updating content

- Profile, publications, and links are in `index.html`.
- Visual design and responsive behavior are in `styles.css`.
- Navigation and scroll reveals are in `script.js`.

The site is served directly from the `main` branch by GitHub Pages.
