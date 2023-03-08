import pandas as pd
from sklearn.datasets import fetch_20newsgroups

SELECTED_CATEGORIES = {
    "comp.graphics": "Computer Graphics",
    "rec.autos": "Autos",
    "rec.sport.hockey": "Hockey",
    "sci.space": "Space",
}


def load_source() -> pd.DataFrame:
    bunch = fetch_20newsgroups(
        subset="train", categories=list(SELECTED_CATEGORIES.keys())
    )
    target_mapping = {
        i: SELECTED_CATEGORIES[v] for i, v in enumerate(bunch["target_names"])
    }

    data = pd.DataFrame(bunch["data"], columns=["text"])
    data["label"] = [target_mapping[i] for i in bunch["target"]]
    data.index.name = "label_id"
    data = data.reset_index()
    return data
