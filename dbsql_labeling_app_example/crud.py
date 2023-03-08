from itertools import chain
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from dbsql_labeling_app_example.engine import Label, engine


class DataOperator:
    def __init__(self) -> None:
        self._session = Session(bind=engine)

    def get_all_ids(self) -> List[int]:
        return self._session.execute(select(Label.label_id)).scalars().all()

    def get_element_by_id(self, id: int) -> Optional[Label]:
        return self._session.query(Label).get(id)

    def update_element_by_id(self, id: int, new_label: str):
        self._session.query(Label).filter_by(label_id=id).update(
            {Label.label: new_label}
        )

    def get_all_classes(self) -> List[str]:
        return list(chain(*self._session.query(Label.label).distinct().all()))
