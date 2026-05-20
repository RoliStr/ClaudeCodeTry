"""Tool registry.

To add a new tool:
  1. Create tools/<your_tool>.py defining a Flask `bp` (Blueprint) and a
     `TOOL` metadata dict (slug, name, description, icon, url).
  2. Import it below and append (module.TOOL, module.bp) to REGISTRY.
The portal landing page and route registration pick it up automatically.
"""
from . import pdf_converter

# (metadata, blueprint) for every registered tool
REGISTRY = [
    (pdf_converter.TOOL, pdf_converter.bp),
]

TOOLS = [meta for meta, _bp in REGISTRY]
BLUEPRINTS = [bp for _meta, bp in REGISTRY]
