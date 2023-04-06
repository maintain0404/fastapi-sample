from typing import Annotated

from sqlalchemy.orm import mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]
required_str = Annotated[str, mapped_column(nullable=False)]
required_bytes = Annotated[bytes, mapped_column(nullable=False)]
