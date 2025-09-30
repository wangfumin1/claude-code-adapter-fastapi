"""
应用测试
"""

from fastapi.testclient import TestClient
from src.claude_code_adapter.app import app

client = TestClient(app)


class TestHealthEndpoint:
    """测试健康检查端点"""

    def test_health_check(self):
        """测试健康检查"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["ok"] is True
        assert "target_base" in data


class TestMessagesEndpoint:
    """测试消息端点"""

    def test_messages_invalid_json(self):
        """测试无效JSON请求"""
        response = client.post("/v1/messages", data="invalid json")
        assert response.status_code == 400

    def test_messages_empty_request(self):
        """测试空请求"""
        response = client.post("/v1/messages", json={})
        # 由于没有目标服务，应该返回502或500
        assert response.status_code in [500, 502]

    def test_messages_basic_request(self):
        """测试基本请求"""
        request_data = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Hello"}],
        }
        response = client.post("/v1/messages", json=request_data)
        # 由于没有目标服务，应该返回502或500
        assert response.status_code in [500, 502]
