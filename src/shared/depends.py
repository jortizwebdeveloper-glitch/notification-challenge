from typing import Annotated

from arq import ArqRedis
from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.arq import get_arq
from src.core.db import get_session

SessionDep = Annotated[Session, Depends(get_session)]
ArqDep = Annotated[ArqRedis, Depends(get_arq)]
