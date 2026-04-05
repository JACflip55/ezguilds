from fastapi import FastAPI

app = FastAPI(title="EZGuilds Worker")


@app.get("/health")
def health():
    return {"status": "ok"}
