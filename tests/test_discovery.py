from etatouch_restful.discovery import flatten_menu, is_default_discovery_candidate
from etatouch_restful.models import EtaMenuNode


def test_flatten_menu_returns_leaf_variables_with_paths() -> None:
    menu = [
        EtaMenuNode(
            uri="/120/10021",
            name="Kessel",
            kind="fub",
            children=(
                EtaMenuNode(
                    uri="/120/10021/0/0/12197",
                    name="Außentemperatur",
                    kind="object",
                ),
            ),
        )
    ]

    variables = flatten_menu(menu)

    assert len(variables) == 1
    assert variables[0].uri == "120/10021/0/0/12197"
    assert variables[0].full_name == "Kessel > Außentemperatur"


def test_default_discovery_candidate_excludes_time_slots() -> None:
    variables = flatten_menu(
        [
            EtaMenuNode(
                uri="/120/10101",
                name="FBH",
                kind="fub",
                children=(
                    EtaMenuNode(
                        uri="/120/10101/12113/0/1082",
                        name="Zeitfenster 1",
                        kind="object",
                        children=(),
                    ),
                ),
            )
        ]
    )

    assert is_default_discovery_candidate(variables[0]) is False


def test_default_discovery_candidate_prefers_inputs() -> None:
    variables = flatten_menu(
        [
            EtaMenuNode(
                uri="/120/10101",
                name="FBH",
                kind="fub",
                children=(
                    EtaMenuNode(
                        uri="/120/10101/0/0/12197",
                        name="Außentemperatur",
                        kind="object",
                        children=(),
                    ),
                ),
            )
        ]
    )

    assert is_default_discovery_candidate(variables[0]) is True
