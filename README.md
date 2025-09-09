# Physics labs

## About

You can find here the interactive labs (experiment simulations), play with parameters and enjoy materialized results!

Each page represents a separate lab, where you can find experiment description, limits of applicability, and the
playground itself.

## Development guide

If you want to play with app on your own, follow the guide to set up cloned app.

### Install [uv](https://docs.astral.sh/uv/)

You can install it via `curl` or `brew`:

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```shell
brew install uv
```

### Then, sync all python dependencies:

```shell
uv sync
```

### Initialize pre-commit

For convenient codestyle auto-formatting.

```shell
uv run pre-commit install
```

### Launch

```shell
uv run streamlit run Main.py
```
