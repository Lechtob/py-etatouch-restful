from etatouch_restful.parser import parse_errors, parse_value, parse_variable_info


def test_parse_value_scales_numeric_raw_value() -> None:
    xml = """<?xml version="1.0" encoding="utf-8"?>
    <eta version="1.0" xmlns="http://www.eta.co.at/rest/v1">
      <value uri="/user/var/112/10021/0/0/12112" strValue="Off" unit=""
        decPlaces="0" scaleFactor="1" advTextOffset="1802">1802</value>
    </eta>"""

    value = parse_value(xml)

    assert value.uri == "/user/var/112/10021/0/0/12112"
    assert value.str_value == "Off"
    assert value.native_value == 1802


def test_parse_errors_flattens_errors_by_fub() -> None:
    xml = """<?xml version="1.0" encoding="utf-8"?>
    <eta version="1.0" xmlns="http://www.eta.co.at/rest/v1">
      <errors uri="/user/errors">
        <fub uri="/112/10021" name="Kessel">
          <error msg="Water pressure too low" priority="Error" time="2011-06-29 12:48:12">
            Top up heating water!
          </error>
        </fub>
      </errors>
    </eta>"""

    errors = parse_errors(xml)

    assert len(errors) == 1
    assert errors[0].fub_name == "Kessel"
    assert errors[0].message == "Water pressure too low"


def test_parse_variable_info_reads_valid_values() -> None:
    xml = """<?xml version="1.0" encoding="utf-8"?>
    <eta xmlns="http://www.eta.co.at/rest/v1" version="1.0">
      <varInfo uri="/user/varinfo/40/10021/0/0/12080">
        <variable uri="40/10021/0/0/12080" name="On/off button"
          fullName="Misc. &gt; On/off button" unit="" decPlaces="0"
          scaleFactor="1" advTextOffset="1802" isWritable="1">
          <type>TEXT</type>
          <validValues>
            <value strValue="Off">1802</value>
            <value strValue="On">1803</value>
          </validValues>
        </variable>
      </varInfo>
    </eta>"""

    info = parse_variable_info(xml)

    assert info.is_writable is True
    assert info.value_type == "TEXT"
    assert [value.str_value for value in info.valid_values] == ["Off", "On"]
