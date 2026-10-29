from typing import Annotated

from sqlalchemy.orm import Session
from src.core.db import get_session

from fastapi import Depends

SessionDep = Annotated[Session, Depends(get_session)]
