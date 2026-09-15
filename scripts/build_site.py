#!/usr/bin/env python3
"""Build the Oracle DBA course Markdown files as a static HTML manual."""

from __future__ import annotations

import argparse
import html
import posixpath
import re
import shutil
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {
    ".git",
    ".github",
    ".venv",
    "node_modules",
    "site",
    "dist",
    "build",
    "__pycache__",
    "professor",
    "nao-precisa",
    ".vscode",
}
SKIP_FILES = {".gitignore", "complemento.txt"}


def output_path(source: Path) -> Path:
    relative = source.relative_to(ROOT)
    if relative == Path("README.md"):
        return Path("index.html")
    if source.name.lower() == "readme.md":
        return relative.parent / "index.html"
    return relative.with_suffix(".html")


def slugify(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE).strip().lower()
    return re.sub(r"[-\s]+", "-", value) or "section"


def table_cells(line: str) -> list[str]:
    value = line.strip()
    if value.startswith("|"):
        value = value[1:]
    if value.endswith("|"):
        value = value[:-1]
    return [cell.strip() for cell in value.split("|")]


def is_table_separator(line: str) -> bool:
    cells = table_cells(line)
    return bool(cells) and all(
        re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells
    )


def first_heading(source: Path) -> str:
    for line in source.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^#\s+(.+?)\s*#*\s*$", line)
        if match:
            return re.sub(r"`", "", match.group(1)).strip()
    return source.stem.replace("-", " ").title()


class MarkdownRenderer:
    def __init__(self, source: Path):
        self.source = source
        self.current_output = output_path(source)
        self.heading_ids: dict[str, int] = {}
        self.tokens: dict[str, str] = {}

    def token(self, value: str) -> str:
        key = f"ORACLEDBATOKEN{len(self.tokens)}END"
        self.tokens[key] = value
        return key

    def rewrite_url(self, raw_url: str) -> str:
        raw_url = raw_url.strip()
        if not raw_url or raw_url.startswith("#"):
            return raw_url
        parsed = urlsplit(raw_url)
        if parsed.scheme or parsed.netloc:
            return raw_url

        target = unquote(parsed.path)
        if not target:
            return raw_url
        candidate = (self.source.parent / target).resolve()
        try:
            relative_target = candidate.relative_to(ROOT)
        except ValueError:
            return raw_url

        if candidate.is_dir() and (candidate / "README.md").exists():
            relative_target = relative_target / "README.md"
        if not candidate.exists():
            return raw_url

        if candidate.suffix.lower() == ".md":
            target_output = output_path(ROOT / relative_target)
        else:
            target_output = relative_target
        href = posixpath.relpath(
            target_output.as_posix(), self.current_output.parent.as_posix()
        )
        return urlunsplit(("", "", href, parsed.query, parsed.fragment))

    def inline(self, value: str) -> str:
        code_pattern = re.compile(r"`([^`]+)`")
        value = code_pattern.sub(
            lambda match: self.token(
                f"<code>{html.escape(match.group(1), quote=False)}</code>"
            ),
            value,
        )

        image_pattern = re.compile(
            r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+['\"]([^'\"]*)['\"])?\)"
        )
        value = image_pattern.sub(
            lambda match: self.token(
                f'<img src="{html.escape(self.rewrite_url(match.group(2)), quote=True)}" '
                f'alt="{html.escape(match.group(1), quote=True)}" loading="lazy">'
            ),
            value,
        )

        link_pattern = re.compile(
            r"\[([^\]]+)\]\(([^)\s]+)(?:\s+['\"]([^'\"]*)['\"])?\)"
        )
        value = link_pattern.sub(
            lambda match: self.token(
                f'<a href="{html.escape(self.rewrite_url(match.group(2)), quote=True)}">'
                f"{self.inline(match.group(1))}</a>"
            ),
            value,
        )

        value = html.escape(value, quote=False)
        value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)
        value = re.sub(r"(?<!\w)\*([^*]+)\*(?!\w)", r"<em>\1</em>", value)
        for key, replacement in self.tokens.items():
            value = value.replace(html.escape(key), replacement)
        return value

    def render(self, markdown: str) -> str:
        lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        output: list[str] = []
        index = 0

        while index < len(lines):
            line = lines[index]
            if not line.strip():
                index += 1
                continue

            fence = re.match(r"^\s*(`{3,}|~{3,})([\w+-]*)\s*$", line)
            if fence:
                marker = fence.group(1)[0]
                language = fence.group(2)
                code_lines: list[str] = []
                index += 1
                while index < len(lines) and not re.match(
                    rf"^\s*{re.escape(marker)}{{3,}}\s*$", lines[index]
                ):
                    code_lines.append(lines[index])
                    index += 1
                if index < len(lines):
                    index += 1
                class_name = (
                    f' class="language-{html.escape(language, quote=True)}"'
                    if language
                    else ""
                )
                code = html.escape("\n".join(code_lines), quote=False)
                output.append(f"<pre><code{class_name}>{code}</code></pre>")
                continue

            heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
            if heading:
                level = len(heading.group(1))
                text = heading.group(2)
                base_id = slugify(text)
                count = self.heading_ids.get(base_id, 0)
                self.heading_ids[base_id] = count + 1
                heading_id = base_id if count == 0 else f"{base_id}-{count + 1}"
                output.append(
                    f'<h{level} id="{heading_id}">{self.inline(text)}</h{level}>'
                )
                index += 1
                continue

            if re.fullmatch(r"\s{0,3}([-*_])(?:\s*\1){2,}\s*", line):
                output.append("<hr>")
                index += 1
                continue

            if line.lstrip().startswith(">"):
                quote_lines: list[str] = []
                while index < len(lines) and (
                    lines[index].lstrip().startswith(">") or not lines[index].strip()
                ):
                    if lines[index].lstrip().startswith(">"):
                        quote_lines.append(re.sub(r"^\s*>\s?", "", lines[index]))
                    elif quote_lines:
                        quote_lines.append("")
                    index += 1
                output.append(f"<blockquote>{self.render(chr(10).join(quote_lines))}</blockquote>")
                continue

            if index + 1 < len(lines) and "|" in line and is_table_separator(lines[index + 1]):
                headers = table_cells(line)
                index += 2
                rows: list[list[str]] = []
                while index < len(lines) and "|" in lines[index] and lines[index].strip():
                    rows.append(table_cells(lines[index]))
                    index += 1
                table = ['<div class="table-wrap"><table><thead><tr>']
                table.extend(f"<th>{self.inline(cell)}</th>" for cell in headers)
                table.append("</tr></thead><tbody>")
                for row in rows:
                    table.append("<tr>")
                    table.extend(f"<td>{self.inline(cell)}</td>" for cell in row)
                    table.append("</tr>")
                table.append("</tbody></table></div>")
                output.append("".join(table))
                continue

            unordered = re.match(r"^\s*[-+*]\s+(.+)$", line)
            ordered = re.match(r"^\s*\d+[.)]\s+(.+)$", line)
            if unordered or ordered:
                tag = "ul" if unordered else "ol"
                pattern = re.compile(
                    r"^\s*[-+*]\s+(.+)$"
                    if unordered
                    else r"^\s*\d+[.)]\s+(.+)$"
                )
                items: list[str] = []
                while index < len(lines):
                    match = pattern.match(lines[index])
                    if not match:
                        break
                    items.append(f"<li>{self.inline(match.group(1))}</li>")
                    index += 1
                output.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
                continue

            paragraph = [line.strip()]
            index += 1
            while index < len(lines) and lines[index].strip():
                next_line = lines[index]
                if re.match(r"^(#{1,6})\s+", next_line):
                    break
                if re.match(r"^\s*(`{3,}|~{3,})", next_line):
                    break
                if re.match(r"^\s*[-+*]\s+", next_line) or re.match(
                    r"^\s*\d+[.)]\s+", next_line
                ):
                    break
                if next_line.lstrip().startswith(">"):
                    break
                paragraph.append(next_line.strip())
                index += 1
            output.append(f"<p>{self.inline(' '.join(paragraph))}</p>")

        return "\n".join(output)


CSS = r"""
:root{color-scheme:dark;--bg:#07111f;--panel:#0d1d31;--panel-2:#122941;--text:#e9f3fb;--muted:#96aec4;--line:#294863;--accent:#ef9b4f;--accent-2:#62d6ff;--green:#5be0bd;--code:#050c15}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;min-width:320px;color:var(--text);background:radial-gradient(circle at 8% 0%,#20587866,transparent 32rem),radial-gradient(circle at 92% 12%,#a35b2b40,transparent 30rem),var(--bg);font:16px/1.7 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}a{color:var(--accent-2)}a:hover{color:var(--accent)}
.site-header{position:sticky;top:0;z-index:20;border-bottom:1px solid var(--line);background:#07111fe8;backdrop-filter:blur(18px)}.header-inner{width:min(1480px,calc(100% - 40px));min-height:76px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:20px}.brand{display:inline-flex;align-items:center;gap:13px;color:var(--text);text-decoration:none}.brand-mark{display:grid;place-items:center;width:42px;height:42px;border:1px solid var(--accent);border-radius:12px;color:var(--accent);font-weight:900;box-shadow:0 0 24px #ef9b4f32}.brand strong{font-size:.92rem;letter-spacing:.13em}.brand span{display:block;margin-top:3px;color:var(--muted);font-size:.72rem;letter-spacing:.09em;text-transform:uppercase}.toolbar{display:flex;align-items:center;gap:10px}.toolbar input{width:220px;padding:9px 12px;color:var(--text);background:var(--panel);border:1px solid var(--line);border-radius:9px}.toolbar button{padding:9px 13px;color:var(--text);background:var(--panel-2);border:1px solid var(--line);border-radius:9px;cursor:pointer}
.layout{width:min(1480px,calc(100% - 40px));display:grid;grid-template-columns:290px minmax(0,1fr);gap:34px;margin:0 auto;padding:34px 0 64px}.sidebar{position:sticky;top:110px;align-self:start;max-height:calc(100vh - 130px);overflow:auto;padding-right:8px}.sidebar-title{margin:0 0 10px;color:var(--muted);font-size:.72rem;letter-spacing:.16em;text-transform:uppercase}.nav-group{margin:20px 0}.nav-group-title{margin:0 0 5px;padding:0 12px;color:var(--accent);font-size:.76rem;letter-spacing:.1em;text-transform:uppercase}.sidebar a{display:block;padding:7px 12px;color:var(--muted);border-left:2px solid transparent;border-radius:0 8px 8px 0;text-decoration:none;font-size:.9rem}.sidebar a:hover,.sidebar a.active{color:var(--text);background:#62d6ff14;border-left-color:var(--accent-2)}.content{min-width:0}.breadcrumb{margin-bottom:18px;color:var(--muted);font-size:.82rem}.article{overflow:hidden;padding:clamp(25px,5vw,62px);background:linear-gradient(145deg,#10243bf2,#081522ed);border:1px solid var(--line);border-radius:24px;box-shadow:0 25px 80px #0000004d}.article>h1{margin-top:0;color:#fbfdff;font-size:clamp(2rem,4vw,3.4rem);line-height:1.12}.article h2{margin-top:2.5em;color:#d8f6ff;font-size:clamp(1.45rem,3vw,2rem)}.article h3{margin-top:2em;color:#bdf3e3}.article p,.article ul,.article ol,.article blockquote{max-width:86ch}.article li{margin:6px 0}.article blockquote{margin:24px 0;padding:13px 20px;color:#c7d7e7;background:#5be0bd0e;border-left:3px solid var(--green);border-radius:0 12px 12px 0}.article code{padding:.12em .35em;color:#d2fff2;background:#00000047;border:1px solid #ffffff14;border-radius:5px;font-size:.9em}.article pre{overflow:auto;margin:22px 0;padding:18px 20px;background:var(--code);border:1px solid #62d6ff35;border-radius:12px}.article pre code{display:block;padding:0;color:#d6f3ff;background:transparent;border:0;line-height:1.6;font-size:.9rem}.article img{display:block;max-width:100%;height:auto;margin:22px auto;border-radius:12px}.article table{width:100%;min-width:600px;border-collapse:collapse}.table-wrap{overflow-x:auto;margin:22px 0}.article th,.article td{padding:10px 12px;text-align:left;vertical-align:top;border:1px solid var(--line)}.article th{color:#e8f9ff;background:#62d6ff16}.article hr{margin:36px 0;border:0;border-top:1px solid var(--line)}.site-footer{width:min(1480px,calc(100% - 40px));padding:24px 0 40px;margin:0 auto;color:var(--muted);border-top:1px solid var(--line);font-size:.84rem}
.landing{position:relative;margin:-18px 0 35px;padding:42px clamp(25px,5vw,62px);overflow:hidden;background:linear-gradient(120deg,#123554,#1b2c42 48%,#3c2a25);border:1px solid #4d6b80;border-radius:24px}.landing:after{content:"";position:absolute;right:-80px;top:-120px;width:330px;height:330px;border:1px solid #ef9b4f66;border-radius:50%;box-shadow:0 0 0 35px #ef9b4f12,0 0 0 70px #ef9b4f08}.landing h1{position:relative;z-index:1;margin:0 0 10px;max-width:780px;font-size:clamp(2.2rem,5vw,4.5rem);line-height:1.03}.landing p{position:relative;z-index:1;max-width:760px;margin:0;color:#bcd0df;font-size:1.08rem}.quick-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:0 0 32px}.quick-card{padding:18px;background:#ffffff08;border:1px solid var(--line);border-radius:15px}.quick-card strong{display:block;color:var(--accent);font-size:.78rem;letter-spacing:.12em;text-transform:uppercase}.quick-card span{display:block;margin-top:5px;color:var(--muted);font-size:.91rem}.empty{display:none}
html.light{color-scheme:light;--bg:#eef5f8;--panel:#fff;--panel-2:#fff;--text:#17283a;--muted:#557086;--line:#aac2d0;--accent:#b45e14;--accent-2:#087da6;--green:#087957}html.light .site-header{background:#eef5f8e8}html.light .article{background:#fffffff2}html.light .article>h1{color:#122333}html.light .article h2{color:#075e7a}html.light .article h3{color:#087957}html.light .landing{background:linear-gradient(120deg,#d7eef5,#fff9ef)}html.light .landing p{color:#456277}
@media(max-width:980px){.header-inner,.layout,.site-footer{width:min(calc(100% - 28px),760px)}.layout{display:block;padding-top:20px}.sidebar{position:static;max-height:none;margin-bottom:20px;padding:15px;background:var(--panel);border:1px solid var(--line);border-radius:15px}.sidebar nav{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:4px}.toolbar input{width:170px}}@media(max-width:620px){.header-inner{min-height:68px}.brand strong{font-size:.76rem}.brand span{display:none}.toolbar input{display:none}.layout{width:min(calc(100% - 20px),600px)}.article{padding:25px 18px;font-size:15px}.quick-grid{grid-template-columns:1fr}.sidebar nav{display:block}.landing{padding:30px 22px}.landing h1{font-size:2.35rem}}
"""


JS = r"""
(() => {
  const root = document.documentElement;
  const themeButton = document.querySelector("#theme-toggle");
  const search = document.querySelector("#nav-search");
  if (localStorage.getItem("oracle-dba-theme") === "light") root.classList.add("light");
  const updateTheme = () => {
    if (themeButton) themeButton.textContent = root.classList.contains("light") ? "Modo escuro" : "Modo claro";
  };
  if (themeButton) themeButton.addEventListener("click", () => {
    root.classList.toggle("light");
    localStorage.setItem("oracle-dba-theme", root.classList.contains("light") ? "light" : "dark");
    updateTheme();
  });
  updateTheme();
  if (search) search.addEventListener("input", () => {
    const query = search.value.toLowerCase().trim();
    document.querySelectorAll(".nav-link").forEach((link) => {
      link.classList.toggle("empty", query && !link.textContent.toLowerCase().includes(query));
    });
    document.querySelectorAll(".nav-group").forEach((group) => {
      group.style.display = [...group.querySelectorAll(".nav-link")].some((link) => !link.classList.contains("empty")) ? "" : "none";
    });
  });
})();
"""


def discover_markdown() -> list[Path]:
    files = []
    for path in ROOT.rglob("*.md"):
        relative_parts = path.relative_to(ROOT).parts
        if any(part in SKIP_DIRS for part in relative_parts):
            continue
        files.append(path)
    return sorted(files, key=lambda path: (path != ROOT / "README.md", path.as_posix()))


def group_name(source: Path) -> str:
    relative = source.relative_to(ROOT)
    if relative == Path("README.md"):
        return "Início"
    top = relative.parts[0]
    if top.startswith("aula"):
        return "Aulas e revisões"
    if top.startswith("modulo"):
        return "Módulos"
    if top == "repo":
        return "Laboratórios"
    if top == "podman":
        return "Ambiente"
    if top == "trabalho-final":
        return "Trabalho final"
    return "Referências"


def relative_href(current: Path, target: Path) -> str:
    return posixpath.relpath(target.as_posix(), current.parent.as_posix())


def navigation(files: list[Path]) -> list[tuple[str, list[tuple[Path, str]]]]:
    groups: dict[str, list[tuple[Path, str]]] = {}
    for source in files:
        if source.name.lower() != "readme.md" and source.parent == ROOT:
            continue
        group = group_name(source)
        groups.setdefault(group, []).append((source, first_heading(source)))
    order = ["Início", "Aulas e revisões", "Módulos", "Ambiente", "Laboratórios", "Trabalho final", "Referências"]
    return [(name, groups[name]) for name in order if name in groups]


def page(source: Path, body: str, nav: list[tuple[str, list[tuple[Path, str]]]]) -> str:
    current = output_path(source)
    root_href = relative_href(current, Path("index.html"))
    css_href = relative_href(current, Path("assets/styles.css"))
    js_href = relative_href(current, Path("assets/app.js"))
    nav_html = []
    for group, items in nav:
        links = []
        for nav_source, title in items:
            active = " active" if nav_source == source else ""
            href = relative_href(current, output_path(nav_source))
            links.append(
                f'<a class="nav-link{active}" href="{html.escape(href, quote=True)}">{html.escape(title)}</a>'
            )
        nav_html.append(
            f'<div class="nav-group"><p class="nav-group-title">{html.escape(group)}</p>{"".join(links)}</div>'
        )

    breadcrumb = source.relative_to(ROOT).as_posix()
    landing = ""
    if source == ROOT / "README.md":
        landing = (
            '<section class="landing"><h1>Oracle DBA Course</h1>'
            '<p>Um manual prático e progressivo para compreender Oracle Database, operar ambientes com Podman e conectar teoria, administração, backup, segurança e APIs.</p>'
            '</section><div class="quick-grid">'
            '<div class="quick-card"><strong>Comece aqui</strong><span>Conexão, CDB, PDB, usuário, schema e tabela.</span></div>'
            '<div class="quick-card"><strong>Laboratório</strong><span>Oracle Free, Podman, SQL*Plus, RMAN e ORDS.</span></div>'
            '<div class="quick-card"><strong>Ritmo</strong><span>Conceito curto, execução prática e validação.</span></div>'
            '</div>'
        )

    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Manual do curso Oracle Database Administration, criado por Jeffotoni.">
<title>{html.escape(first_heading(source))} · Oracle DBA Course</title>
<link rel="stylesheet" href="{html.escape(css_href, quote=True)}">
</head>
<body>
<header class="site-header"><div class="header-inner">
<a class="brand" href="{html.escape(root_href, quote=True)}"><span class="brand-mark">DB</span><span><strong>ORACLE DBA COURSE</strong><span>aprender · operar · administrar</span></span></a>
<div class="toolbar"><input id="nav-search" type="search" placeholder="Buscar no manual..."><button id="theme-toggle" type="button">Modo claro</button></div>
</div></header>
<div class="layout"><aside class="sidebar" aria-label="Navegação do manual"><p class="sidebar-title">Manual do curso</p><nav>{"".join(nav_html)}</nav></aside>
<main class="content"><div class="breadcrumb">{html.escape(breadcrumb)}</div><article class="article">{landing}{body}</article></main></div>
<footer class="site-footer">Oracle DBA Course · conteúdo HTML gerado automaticamente a partir dos arquivos Markdown · Jeffotoni</footer>
<script src="{html.escape(js_href, quote=True)}"></script>
</body></html>'''


def copy_static(output: Path) -> None:
    for source in ROOT.rglob("*"):
        if not source.is_file():
            continue
        relative = source.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in relative.parts):
            continue
        if source.name in SKIP_FILES:
            continue
        if source.suffix.lower() == ".md" or source.suffix.lower() == ".py":
            continue
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def build(output: Path) -> None:
    output = output.resolve()
    if output == ROOT or ROOT not in output.parents:
        raise SystemExit("O diretório de saída deve ficar dentro do repositório e não pode ser a raiz.")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    files = discover_markdown()
    nav = navigation(files)
    for source in files:
        destination = output / output_path(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        body = MarkdownRenderer(source).render(source.read_text(encoding="utf-8"))
        destination.write_text(page(source, body, nav), encoding="utf-8")

    assets = output / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    (assets / "styles.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    (assets / "app.js").write_text(JS.strip() + "\n", encoding="utf-8")
    copy_static(output)
    shutil.copy2(output / "index.html", output / "404.html")
    print(f"Generated {len(files)} Markdown pages in {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the Oracle DBA static manual")
    parser.add_argument("--output-dir", default="site")
    args = parser.parse_args()
    build(ROOT / args.output_dir)


if __name__ == "__main__":
    main()
