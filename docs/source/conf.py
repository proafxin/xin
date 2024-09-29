# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import tomllib
from os.path import abspath, dirname, join

from pydantic import BaseModel, RootModel

cwd = dirname(abspath(__file__))
root = join(cwd, "../..")

sys.path.insert(0, root)

toml_file = join(root, "pyproject.toml")


class Author(BaseModel):
    name: str
    email: str

    def __repr__(self) -> str:
        return f"{self.name}, <{self.email}>"


Authors = RootModel(root=Author)

with open(toml_file, "rb") as f:
    data = tomllib.load(f)
    project = data.get("project")
    if not isinstance(project, dict):
        raise ValueError("`project` is not present in toml.")

    if "version" not in project:
        raise ValueError("`version` not in project")
    version = project["version"]

    if "authors" not in project:
        raise ValueError("`author` not in project")
    authors = ", ".join([str(author) for author in Authors.model_validate(project["authors"])])


release = version

project = "Pandas Extras"
copyright = "2023, Masum Billal"
author = "Masum Billal"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
]

templates_path = ["_templates"]
exclude_patterns: list[str] = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"

html_theme_options: dict[str, str] = {}
html_context = {"default_mode": "dark"}

html_static_path: list[str] = []
