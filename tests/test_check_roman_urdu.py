import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from check_roman_urdu import check, fix, main  # noqa: E402


def test_finds_variants_with_positions():
    issues = check("Ap kia ker rhe hen?")
    assert [(i.found, i.suggestion) for i in issues] == [
        ("Ap", "Aap"), ("kia", "kya"), ("ker", "kar"), ("rhe", "rahe"), ("hen", "hain"),
    ]
    assert issues[0].line == 1 and issues[0].column == 1


def test_fix_keeps_case_and_punctuation():
    assert fix("THIK hai, Shukria!\nnhi") == "THEEK hai, Shukriya!\nnahi"


def test_clean_text_has_no_issues():
    assert check("Aap kya kar rahe hain? Shukriya.") == []


def test_cli_exit_codes(tmp_path, capsys):
    bad = tmp_path / "bad.txt"
    bad.write_text("mjhe jldi chahye", encoding="utf-8")
    good = tmp_path / "good.txt"
    good.write_text("mujhe jaldi chahiye", encoding="utf-8")
    assert main([str(bad)]) == 1
    assert main([str(good)]) == 0
    assert "No issues" in capsys.readouterr().out
