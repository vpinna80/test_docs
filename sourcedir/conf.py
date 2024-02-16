import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

html_theme = "sphinx_rtd_theme"
extensions = [
    "sphinxcontrib.mermaid",
    "sphinxcontrib.plantuml",
    "rst2pdf.pdfbuilder",
    "sphinx_collapse"
]
pdf_documents = [
    ("index", "rst2pdf", "Sample rst2pdf doc", "Your Name"),
]
exclude_patterns = ["*intro.rst"]
html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
}
html_context = {
    "display_github": True,  # Integrate GitHub
    "github_user": "vpinna80",  # Username
    "github_repo": "test_docs",  # Repo name
    "github_version": "master",  # Version
    "conf_py_path": "/sourcedir/",  # Path in the checkout to the docs root
}
# Load templates
jinjaEnv = Environment(loader=FileSystemLoader(searchpath="templates"))
templates = {}
for template in next(os.walk("templates"))[2]:
    templates[template] = jinjaEnv.get_template(template)

# Apply templates in each op folder
for op_folder in next(os.walk("operators"))[1]:
    # Write the op main page
    op_path = Path("operators").joinpath(op_folder)
    with open(op_path.joinpath("index.rst"), "w") as f:
        f.write(templates["operator"].render({"title": op_folder}))

    # Write the op examples
    examples_folder = op_path.joinpath("examples")
    ds_list = sorted(x.with_suffix('').name for x in examples_folder.glob("ds_*.csv"))
    ex_list = sorted(x.with_suffix('').name for x in examples_folder.glob("ex_*.vtl"))
    with open(op_path.joinpath("examples.rst"), "w") as f:
        f.write(
            templates["examples"].render({"examples": ex_list, "ds_list": ds_list})
        )

plantuml = "java -jar " + os.getenv("PUML_PATH", "/tmp/plantuml-mit-1.2023.13.jar")
