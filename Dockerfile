FROM ghcr.io/astral-sh/uv:python3.12-alpine

WORKDIR /app
COPY labs/ ./labs/
COPY main.py pyproject.toml uv.lock ./

ENV UV_NO_DEV=1
ENV UV_LINK_MODE=copy
ENV UV_CACHE_DIR=/cache/uv
RUN --mount=type=cache,target=$UV_CACHE_DIR \
    uv sync --frozen --compile-bytecode

ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_PORT=8501
CMD ["uv", "run", "streamlit", "run", "Main.py"]
EXPOSE $STREAMLIT_SERVER_PORT
