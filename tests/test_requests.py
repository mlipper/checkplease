"""Unit tests for requests module."""


class TestDiffRequest:

    def test_diff_request_common_name_json(self, diff_request_json):
        common_name = "1200-address"
        assert common_name == diff_request_json.common_name()

    def test_diff_request_common_name_xml(self, diff_request_xml):
        common_name = "1200-address"
        assert common_name == diff_request_xml.common_name()

    def test_diff_request_dirname_json(self, diff_request_json, date_stamp_001):
        assert date_stamp_001 == diff_request_json.dirname()

    def test_diff_request_dirname_xml(self, diff_request_xml, date_stamp_002):
        assert date_stamp_002 == diff_request_xml.dirname()

    def test_diff_local_request_file_id_json(
        self, address_json_local_request, diff_request_json
    ):
        # 1200-address-1.json
        assert (
            address_json_local_request.file_id() + "-1.json"
            == diff_request_json.file_id_one()
        )

    def test_diff_remote_request_file_id_json(
        self, address_json_remote_request, diff_request_json
    ):
        # 1200-address-2.json
        assert (
            address_json_remote_request.file_id() + "-2.json"
            == diff_request_json.file_id_two()
        )

    def test_diff_local_request_file_id_xml(
        self, address_xml_local_request, diff_request_xml
    ):
        # 1200-address-1.xml
        assert (
            address_xml_local_request.file_id() + "-1.xml"
            == diff_request_xml.file_id_one()
        )

    def test_diff_remote_request_file_id_xml(
        self, address_xml_remote_request, diff_request_xml
    ):
        # 1200-address-2.xml
        assert (
            address_xml_remote_request.file_id() + "-2.xml"
            == diff_request_xml.file_id_two()
        )


class TestRequest:
    def test_common_id_forward_slash(
        self, foo_bar_endpoint, foo_bar_id_zero, foo_bar_json_local_request
    ):
        expected = f"{foo_bar_id_zero}-{foo_bar_endpoint}"
        assert foo_bar_json_local_request.common_id() == expected

    def test_common_id(
        self, address_endpoint, address_id_zero, address_xml_local_request
    ):
        expected = f"{address_id_zero}-{address_endpoint}"
        assert address_xml_local_request.common_id() == expected

    def test_file_id_forward_slash(
        self, foo_bar_endpoint, foo_bar_id_zero, foo_bar_json_local_request
    ):
        expected = f"{foo_bar_id_zero}-{foo_bar_endpoint.replace('/', '-')}"
        assert foo_bar_json_local_request.file_id() == expected

    def test_file_id(
        self, address_endpoint, address_id_zero, address_xml_local_request
    ):
        expected = f"{address_id_zero}-{address_endpoint}"
        assert address_xml_local_request.file_id() == expected

    def test_query_params_with_params(self, address_xml_local_request, address_params):
        params = address_xml_local_request.query_params()
        assert len(params) == 4
        assert params == address_params

    def test_query_params_no_params(self, version_xml_remote_request, none_params):
        params = version_xml_remote_request.query_params()
        assert len(params) == 1
        assert params is not None

    def test_url_json_local(
        self, local_url_str, address_endpoint, address_json_local_request
    ):
        expected = f"{local_url_str}/{address_endpoint}"
        assert address_json_local_request.url() == expected

    def test_url_json_remote(
        self, remote_url_str, address_endpoint, address_json_remote_request
    ):
        expected = f"{remote_url_str}/{address_endpoint}"
        assert address_json_remote_request.url() == expected

    def test_url_xml_local(
        self, local_url_str, address_endpoint, address_xml_local_request
    ):
        expected = f"{local_url_str}/{address_endpoint}.xml"
        assert address_xml_local_request.url() == expected

    def test_url_xml_remote(
        self, remote_url_str, address_endpoint, address_xml_remote_request
    ):
        expected = f"{remote_url_str}/{address_endpoint}.xml"
        assert address_xml_remote_request.url() == expected
