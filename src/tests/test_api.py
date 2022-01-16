import pytest


class TestAttack:
    ATTACK_URI = "/api/v1/attack"

    @pytest.mark.parametrize(
        "vm_id, expected",
        [
            ("vm-1", ["vm-2", "vm-3"]),
            ("vm-2", ["vm-1", "vm-2"]),
            ("vm-3", ["vm-2"]),
            ("vm-4", ["vm-4"]),
            ("vm-5", []),
        ],
    )
    def test_success(self, test_client, upload_cloud_env, vm_id, expected):
        response = test_client.get(self.ATTACK_URI, params={"vm_id": vm_id})
        assert response.status_code == 200
        assert sorted(response.json()) == sorted(expected)

    def test_vm_id_not_provided(self, test_client):
        response = test_client.get(self.ATTACK_URI)
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "loc": ["query", "vm_id"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }

    def test_vm_not_found(self, test_client, upload_cloud_env):
        response = test_client.get(self.ATTACK_URI, params={"vm_id": "vm-invalid"})

        assert response.status_code == 200
        assert response.json() == []

    def test_spy(self, mocker, test_client, upload_cloud_env):
        from cloud.views import CloudEnvironmentService

        spy = mocker.spy(CloudEnvironmentService, "get_vm_vulnerabilities")
        test_client.get(self.ATTACK_URI, params={"vm_id": "vm-1"})
        spy.assert_called_once_with("vm-1")


class TestStats:
    STATS_URI = "/api/v1/stats"

    def test_success(self, test_client, upload_cloud_env):
        # this test should be done using a mock for middleware, but this has proven to be problematic and time-consuming
        response = test_client.get(self.STATS_URI)

        assert response.status_code == 200
        response_json = response.json()

        assert response_json["vm_count"] == 5
        assert response_json["request_count"] == 17
        assert response_json["average_request_time"] < 0.0005

    def test_spy(self, mocker, test_client, upload_cloud_env):
        from monitoring.views import CloudEnvironmentService

        spy = mocker.spy(CloudEnvironmentService, "get_vm_count")
        test_client.get(self.STATS_URI)
        spy.assert_called_once_with()
