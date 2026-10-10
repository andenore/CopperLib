"""Reusable requirements only: never assume electrical/production qualification."""
from pathlib import Path

import pytest
from pcbir.engineering_qualification import load_contract, REQUIRED

ROOT = Path(__file__).parents[1]
CONTRACTS = (
    "packages/circuits/ti/tps63020-buck-boost/qualification.json",
    "packages/circuits/nordic/nrf52832-johanson-reference/qualification.json",
    "packages/parts/simcom/sim7670g-lngv/qualification.json",
    "packages/parts/u-blox/max-m10s/qualification.json",
    "packages/parts/ti/bq24072/qualification.json",
    "packages/interfaces/usb/usb2-channel/qualification.json",
)


@pytest.mark.parametrize("relative", CONTRACTS)
def test_contract_is_strict_reusable_and_unqualified(relative):
    contract = load_contract(ROOT / relative)
    assert contract["production_publishable"] is False
    assert REQUIRED[contract["kind"]] <= {item["id"] for item in contract["requirements"]}
    assert contract["sources"]
    assert not any(key in contract for key in ("coordinates", "reference_designators", "tracker", "board"))
    if contract["kind"] == "rf":
        assert contract["matching"] in {"required", "integrated", "unresolved"}


def test_provisional_rf_sources_remain_explicitly_unresolved():
    modem = load_contract(ROOT / CONTRACTS[2])
    gnss = load_contract(ROOT / CONTRACTS[3])
    assert modem["matching"] == "unresolved"
    assert gnss["matching"] == "integrated"
    assert any(source["sha256"] is None for source in gnss["sources"])
    integration = next(source for source in gnss["sources"] if "IntegrationManual" in source["url"])
    assert integration["sha256"] == "5a7510ef84f7e2757c57e362a25e3c16bcf8c80af5a4f70790c2e51032dbcd13"
    assert "R05" in integration["revision"]
    assert all(item["algorithm"] == "external" for item in gnss["requirements"]
               if item["id"] in REQUIRED["rf"])


def test_usb_contract_requires_whole_channel_and_applicable_mode():
    contract = load_contract(ROOT / CONTRACTS[5])
    assert contract["kind"] == "interface"
    assert contract["protocol"] == "USB 2.0"
    assert {r["id"] for r in contract["requirements"]} == REQUIRED["interface"]
    assert all(r["algorithm"] == "external" for r in contract["requirements"])
    source = contract["sources"][0]
    assert source["sha256"] == "5fe9c53c04033818af396e8852b3acbca5c3a76ba92fab549fd81cd0ea7b3692"
    assert source["member_sha256"] == "d39698a33486c399124af92bd02e4f978fd9a836b5cf4e52e6e4633eb1d89f61"
