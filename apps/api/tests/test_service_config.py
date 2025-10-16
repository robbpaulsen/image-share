"""
Tests for systemd service configuration validation.

These tests verify that the service configuration files are properly formatted
and contain the required settings for production deployment.
"""
import pytest
import configparser
from pathlib import Path


@pytest.fixture
def service_file_path():
    """Path to the systemd service file."""
    return Path(__file__).parent.parent.parent.parent / "infrastructure" / "image-share.service"


@pytest.fixture
def service_config(service_file_path):
    """Parse and return the systemd service configuration."""
    if not service_file_path.exists():
        pytest.skip(f"Service file not found at {service_file_path}")

    config = configparser.ConfigParser()
    config.read(service_file_path)
    return config


def test_service_file_exists(service_file_path):
    """Test that the systemd service file exists."""
    assert service_file_path.exists(), f"Service file not found at {service_file_path}"


def test_service_has_required_sections(service_config):
    """Test that service file has required sections."""
    required_sections = ["Unit", "Service", "Install"]

    for section in required_sections:
        assert service_config.has_section(section), f"Missing required section: [{section}]"


def test_unit_section_configuration(service_config):
    """Test Unit section has proper configuration."""
    unit = service_config["Unit"]

    # Should have a description
    assert "Description" in unit, "Missing Description in [Unit]"
    assert len(unit["Description"]) > 0, "Description is empty"

    # Should depend on network.target
    assert "After" in unit, "Missing After in [Unit]"
    assert "network.target" in unit["After"], "Service should start after network.target"


def test_service_section_configuration(service_config):
    """Test Service section has proper configuration."""
    service = service_config["Service"]

    # Type should be simple
    assert service.get("Type") == "simple", "Service Type should be 'simple'"

    # Should run as non-root user
    assert "User" in service, "Missing User in [Service]"
    user = service["User"]
    assert user != "root", "Service should NOT run as root user"
    assert user == "pi", "Service should run as 'pi' user"

    # Should have working directory
    assert "WorkingDirectory" in service, "Missing WorkingDirectory in [Service]"
    assert "/home/pi/image-share" in service["WorkingDirectory"], "WorkingDirectory should be /home/pi/image-share"

    # Should have environment file
    assert "EnvironmentFile" in service, "Missing EnvironmentFile in [Service]"
    assert ".env" in service["EnvironmentFile"], "EnvironmentFile should reference .env"

    # Should have startup delay (AC: 2)
    assert "ExecStartPre" in service, "Missing ExecStartPre in [Service]"
    assert "sleep" in service["ExecStartPre"], "ExecStartPre should include sleep command"
    assert "180" in service["ExecStartPre"], "Startup delay should be 180 seconds"

    # Should have ExecStart with uvicorn
    assert "ExecStart" in service, "Missing ExecStart in [Service]"
    exec_start = service["ExecStart"]
    assert "uvicorn" in exec_start, "ExecStart should use uvicorn"
    assert "apps.api.main:app" in exec_start, "ExecStart should run apps.api.main:app"
    assert "--host 0.0.0.0" in exec_start, "Uvicorn should bind to 0.0.0.0"
    assert "--port" in exec_start, "Uvicorn should specify port"

    # Should have restart configuration (AC: 4)
    assert "Restart" in service, "Missing Restart in [Service]"
    assert service["Restart"] == "on-failure", "Restart should be 'on-failure'"

    assert "RestartSec" in service, "Missing RestartSec in [Service]"
    assert service["RestartSec"] == "10", "RestartSec should be 10 seconds"

    # Should log to journal
    assert "StandardOutput" in service, "Missing StandardOutput in [Service]"
    assert service["StandardOutput"] == "journal", "StandardOutput should be 'journal'"

    assert "StandardError" in service, "Missing StandardError in [Service]"
    assert service["StandardError"] == "journal", "StandardError should be 'journal'"


def test_install_section_configuration(service_config):
    """Test Install section has proper configuration."""
    install = service_config["Install"]

    # Should be enabled for multi-user.target (AC: 5)
    assert "WantedBy" in install, "Missing WantedBy in [Install]"
    assert "multi-user.target" in install["WantedBy"], "Service should be wanted by multi-user.target"


def test_service_uses_virtual_environment(service_config):
    """Test that service uses the virtual environment Python."""
    service = service_config["Service"]
    exec_start = service.get("ExecStart", "")

    # Should use .venv/bin/uvicorn (absolute path)
    assert ".venv/bin/uvicorn" in exec_start, "ExecStart should use virtual environment uvicorn"
    assert "/home/pi/image-share/.venv/bin/uvicorn" in exec_start, "Should use absolute path to uvicorn"


def test_health_check_script_exists():
    """Test that health check script exists."""
    script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "health-check.sh"
    assert script_path.exists(), f"Health check script not found at {script_path}"


def test_installation_script_exists():
    """Test that installation script exists."""
    script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "install-service.sh"
    assert script_path.exists(), f"Installation script not found at {script_path}"


def test_status_script_exists():
    """Test that service status script exists."""
    script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "service-status.sh"
    assert script_path.exists(), f"Service status script not found at {script_path}"


def test_deployment_documentation_exists():
    """Test that deployment documentation exists."""
    doc_path = Path(__file__).parent.parent.parent.parent / "docs" / "deployment.md"
    assert doc_path.exists(), f"Deployment documentation not found at {doc_path}"

    # Should be substantial documentation (more than 1000 characters)
    content = doc_path.read_text()
    assert len(content) > 1000, "Deployment documentation should be comprehensive"

    # Should contain key sections
    assert "Service Management" in content, "Missing 'Service Management' section"
    assert "Troubleshooting" in content, "Missing 'Troubleshooting' section"
    assert "systemctl" in content, "Documentation should mention systemctl commands"
    assert "journalctl" in content, "Documentation should mention journalctl for logs"
