import pynecone as pc
from faker import Faker

fake = Faker()


class State(pc.State):
    """The app state."""


def index() -> pc.Component:
    return pc.center(
        pc.vstack(
            pc.flex(
                pc.flex(
                    pc.heading("🪄 This is a sample data labeling app"),
                    width="80%",
                    justify_content="center",
                ),
                pc.spacer(),
                pc.button(
                    pc.icon(tag="moon"),
                    on_click=pc.toggle_color_mode,
                    color="black",
                    size="sm",
                ),
                width="100%",
                padding_top="10px",
                justify_content="center",
            ),
            pc.hstack(
                pc.button(pc.icon(tag="arrow_back"), variant="outline"),
                pc.hstack(
                    pc.text(fake.paragraph(nb_sentences=20), width="70%"),
                    pc.spacer(),
                    pc.box(
                        pc.vstack(
                            pc.select(
                                [f"Class {i}" for i in range(10)],
                                placeholder="Select the class",
                            ),
                            pc.flex(
                                pc.button("Confirm!", bg="green", width="100%"),
                                width="100%",
                            ),
                        ),
                        width="20%",
                    ),
                    padding="5%",
                ),
                pc.button(pc.icon(tag="arrow_forward"), variant="outline"),
            ),
        ),
        padding_X="4%",
    )


# Add state and page to the app.
app = pc.App(
    state=State,
)

app.add_page(
    index,
    title="Labeling app",
    description="Sample labeling app with DBSQL and pynecone",
)
app.compile()
