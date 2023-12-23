import pytest
from project import validated, show_files, convert_to_json

def test_validated():
    assert validated("https://www.proteinatlas.org/download/pathology.tsv.zip") == ("https://www.proteinatlas.org/download/pathology.tsv.zip", "pathology", True)
    assert validated("https://www.proteinatlas.org/download/subcellular_location.tsv.zip") == ("https://www.proteinatlas.org/download/subcellular_location.tsv.zip", "subcellular_location")
    with pytest.raises(ValueError):
        validated("https://www.youtube.com/")
    with pytest.raises(ValueError):
        validated("https://www.proteinatlas.org/about/download/")

def test_show_files():
    assert show_files("Is this a file?") == ("No file in the correct format was selected")
    assert show_files("a/b.cde") == ("No file in the correct format was selected")
    assert show_files("/workspaces/131176334/project/README.md") == ("/workspaces/131176334/project/README.md")

def test_convert_to_json():
    # LIVER_edited_pathology.tsv has to be in the project folder for the following test
    assert convert_to_json("LIVER_edited_pathology.tsv") == f"LIVER_edited_pathology.json is created in project folder"
    with pytest.raises(ValueError):
        convert_to_json("filename")
    with pytest.raises(ValueError):
        convert_to_json("pathology.json")

