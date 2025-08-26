from typing import TypedDict, Literal, NotRequired


class Skill(TypedDict):
    nome: str
    tipo: Literal["ataque", "defesa", "passiva"]
    custo: int
    descricao: NotRequired[str]


class Card(TypedDict):
    _id: str
    nome: str
    foto: str
    habilidades: list[Skill]


class User(TypedDict):
    _id: str
    discord_id: int
    cartas: list[str]
    xp: int
