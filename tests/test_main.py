import pytest

from uv_template import main


def test_main_prints(capsys: pytest.CaptureFixture[str]) -> None:
    main.main()
    assert capsys.readouterr().out == "Hello World\n"
