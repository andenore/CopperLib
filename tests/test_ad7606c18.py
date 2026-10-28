from copper_cli import compile_board, part
def test_adc_serial_pin_contract():
    b=compile_board('board T { import a "github.com/andenore/CopperLib/packages/parts/adi/ad7606c-18"; component U: a.AD7606C18BSTZ_SERIAL_EXTERNAL_REF; }')
    pins=part(b,"a.AD7606C18BSTZ_SERIAL_EXTERNAL_REF")["pins"]
    assert {p["number"] for p in pins.values()}=={str(n) for n in range(1,65)}
    assert pins["REGCAP_36"]["number"]=="36" and pins["REGCAP_39"]["number"]=="39"
    assert pins["REFCAPA"]["number"]=="44" and pins["REFCAPB"]["number"]=="45"
    assert pins["DOUTA"]["number"]=="24" and pins["SDI"]["number"]=="29"
    assert pins["V1P"]["number"]=="49" and pins["V8N"]["number"]=="64"
