# Physics labs

## About

You can find [here](https://hsse-physics-labs.streamlit.app/) the interactive labs (experiment simulations), play with parameters and enjoy materialized results!

Each page represents a separate lab, where you can find experiment description, limits of applicability, and the
playground itself.


## Contents

Try out interactive labs **right now**, on our [website!](https://hsse-physics-labs.streamlit.app/)

- **M1. Throw a rock** · [General information](labs/throw_a_rock) · [Tests](tests/throw_a_rock)
- **M2. Flight to Mars** · [General information](labs/flight_to_mars) · [Tests](tests/flight_to_mars)


## Launch guide

### Option 1. `uv`

Install [uv](https://docs.astral.sh/uv/) via `curl`:

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

...or via `brew`:

```shell
brew install uv
```

Then, sync python dependencies:

```shell
uv sync --no-dev
```

And launch the app:

```shell
uv run streamlit run main.py
```

### Option 2. `pip`

If you don't want to install `uv`, you can use `pip` with `requirements.txt`.

Install dependencies (preferably into a virtual environment):

```shell
pip install -r requirements.txt
```

And run the app:

```shell
streamlit run main.py
```


## Development guide

Install [uv](https://docs.astral.sh/uv/) via `curl`:

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

...or via `brew`:

```shell
brew install uv
```

Then, sync all python dependencies:
```shell
uv sync
```

Initialize pre-commit for convenient codestyle auto-formatting:

```shell
uv run pre-commit install
```

And run the app (with hot-reload):

```shell
uv run streamlit run main.py
```
