from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)

    nome: Mapped[str]
    genero: Mapped[str]
    ano: Mapped[int]

    zerado: Mapped[bool] = mapped_column(default=False)