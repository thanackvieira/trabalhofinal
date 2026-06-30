from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home():
    return RedirectResponse(url="/games")


# LISTAR
@app.get("/games")
def listar(request: Request, session: Session = Depends(get_session)):
    games = session.scalars(select(models.Game)).all()

    return templates.TemplateResponse(
        request,
        "lista.html",
        {"games": games}
    )


# FORM NOVO
@app.get("/games/novo")
def form_novo(request: Request):
    return templates.TemplateResponse(
        request,
        "form.html",
        {"game": None}
    )


# CRIAR
@app.post("/games")
def criar(
    nome: str = Form(...),
    genero: str = Form(...),
    ano: int = Form(...),
    zerado: bool = Form(False),
    session: Session = Depends(get_session),
):

    game = models.Game(
        nome=nome,
        genero=genero,
        ano=ano,
        zerado=zerado
    )

    session.add(game)
    session.commit()
    return RedirectResponse(url="/games", status_code=303)


# EDITAR FORM
@app.get("/games/{game_id}/editar")
def form_editar(game_id: int, request: Request, session: Session = Depends(get_session)):
    game = session.get(models.Game, game_id)

    return templates.TemplateResponse(
        request,
        "form.html",
        {"game": game}
    )


# EDITAR SALVAR
@app.post("/games/{game_id}/editar")
def atualizar(
    game_id: int,
    nome: str = Form(...),
    genero: str = Form(...),
    ano: int = Form(...),
    zerado: bool = Form(False),
    session: Session = Depends(get_session),
):

    game = session.get(models.Game, game_id)

    game.nome = nome
    game.genero = genero
    game.ano = ano
    game.zerado = zerado

    session.commit()
    return RedirectResponse(url="/games", status_code=303)


# EXCLUIR
@app.post("/games/{game_id}/excluir")
def excluir(game_id: int, session: Session = Depends(get_session)):
    game = session.get(models.Game, game_id)

    session.delete(game)
    session.commit()

    return RedirectResponse(url="/games", status_code=303)