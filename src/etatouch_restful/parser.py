"""XML parsers for ETA Touch responses."""

from __future__ import annotations

import xml.etree.ElementTree as ET

from .exceptions import EtaTouchResponseError
from .models import EtaError, EtaMenuNode, EtaValidValue, EtaValue, EtaVariableInfo, EtaVariableSet

NS = {"eta": "http://www.eta.co.at/rest/v1"}


def parse_api_version(xml: str) -> str:
    root = _root(xml)
    api = root.find("eta:api", NS)
    if api is None:
        raise EtaTouchResponseError("ETA Touch response did not contain an api element")
    return api.attrib["version"]


def parse_menu(xml: str) -> list[EtaMenuNode]:
    root = _root(xml)
    menu = root.find("eta:menu", NS)
    if menu is None:
        raise EtaTouchResponseError("ETA Touch response did not contain a menu element")
    return [_parse_menu_node(child) for child in menu]


def parse_value(xml: str) -> EtaValue:
    root = _root(xml)
    value = root.find("eta:value", NS)
    if value is None:
        raise EtaTouchResponseError("ETA Touch response did not contain a value element")
    return _parse_value(value)


def parse_variable_sets(xml: str) -> list[str]:
    root = _root(xml)
    return [element.attrib["uri"].removeprefix("/user/vars/") for element in root.findall("eta:vars", NS)]


def parse_variable_set(xml: str) -> EtaVariableSet:
    root = _root(xml)
    vars_element = root.find("eta:vars", NS)
    if vars_element is None:
        raise EtaTouchResponseError("ETA Touch response did not contain a vars element")
    return EtaVariableSet(
        uri=vars_element.attrib.get("uri", ""),
        variables=tuple(_parse_value(element) for element in vars_element.findall("eta:variable", NS)),
    )


def parse_errors(xml: str) -> list[EtaError]:
    root = _root(xml)
    errors: list[EtaError] = []
    for fub in root.findall(".//eta:fub", NS):
        for error in fub.findall("eta:error", NS):
            errors.append(
                EtaError(
                    fub_uri=fub.attrib.get("uri", ""),
                    fub_name=fub.attrib.get("name", ""),
                    message=error.attrib.get("msg", ""),
                    priority=error.attrib.get("priority", ""),
                    time=error.attrib.get("time", ""),
                    description=(error.text or "").strip(),
                )
            )
    return errors


def parse_variable_info(xml: str) -> EtaVariableInfo:
    root = _root(xml)
    variable = root.find(".//eta:variable", NS)
    if variable is None:
        raise EtaTouchResponseError("ETA Touch response did not contain a variable element")
    valid_values = tuple(
        EtaValidValue(raw=(value.text or "").strip(), str_value=value.attrib.get("strValue", ""))
        for value in variable.findall("eta:validValues/eta:value", NS)
    )
    type_element = variable.find("eta:type", NS)
    return EtaVariableInfo(
        uri=variable.attrib.get("uri", ""),
        name=variable.attrib.get("name", ""),
        full_name=variable.attrib.get("fullName", ""),
        unit=variable.attrib.get("unit", ""),
        decimal_places=_int_attr(variable, "decPlaces", 0),
        scale_factor=_float_attr(variable, "scaleFactor", 1.0),
        advanced_text_offset=_optional_int_attr(variable, "advTextOffset"),
        is_writable=variable.attrib.get("isWritable") == "1",
        value_type=(type_element.text or "").strip() if type_element is not None else "",
        valid_values=valid_values,
    )


def ensure_success(xml: str) -> None:
    root = _root(xml)
    if root.find("eta:success", NS) is None:
        raise EtaTouchResponseError("ETA Touch response did not contain a success element")


def _root(xml: str) -> ET.Element:
    try:
        return ET.fromstring(xml)
    except ET.ParseError as err:
        raise EtaTouchResponseError("ETA Touch returned invalid XML") from err


def _parse_menu_node(element: ET.Element) -> EtaMenuNode:
    return EtaMenuNode(
        uri=element.attrib.get("uri", ""),
        name=element.attrib.get("name", ""),
        kind=_local_name(element.tag),
        children=tuple(_parse_menu_node(child) for child in element),
    )


def _parse_value(element: ET.Element) -> EtaValue:
    return EtaValue(
        uri=element.attrib.get("uri", ""),
        raw=(element.text or "").strip(),
        str_value=element.attrib.get("strValue", ""),
        unit=element.attrib.get("unit", ""),
        decimal_places=_int_attr(element, "decPlaces", 0),
        scale_factor=_float_attr(element, "scaleFactor", 1.0),
        advanced_text_offset=_optional_int_attr(element, "advTextOffset"),
    )


def _int_attr(element: ET.Element, name: str, default: int) -> int:
    try:
        return int(element.attrib.get(name, default))
    except ValueError:
        return default


def _optional_int_attr(element: ET.Element, name: str) -> int | None:
    if name not in element.attrib:
        return None
    return _int_attr(element, name, 0)


def _float_attr(element: ET.Element, name: str, default: float) -> float:
    try:
        return float(element.attrib.get(name, default))
    except ValueError:
        return default


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]

