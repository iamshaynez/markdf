from __future__ import annotations

import argparse
from pathlib import Path

from .renderer import RenderOptions, ThemeNotFoundError, list_builtin_themes, render_pdf
from .theme import init_theme_skeleton


def _path(p: str) -> Path:
    return Path(p).expanduser().resolve()


def main() -> None:
    parser = argparse.ArgumentParser(prog="markdf")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_render = sub.add_parser("render", help="把 Markdown 渲染成 PDF")
    p_render.add_argument("input", type=str, help="输入 Markdown 文件")
    p_render.add_argument("-o", "--output", type=str, required=True, help="输出 PDF 文件")
    p_render.add_argument("--theme", type=str, default="default", help="内置主题名")
    p_render.add_argument("--theme-dir", type=str, default=None, help="自定义主题目录")
    p_render.add_argument("--title", type=str, default=None, help="页眉标题")
    p_render.add_argument("--footer", type=str, default=None, help="页脚左侧小字")
    p_render.add_argument("--no-header", action="store_true", help="禁用页眉")
    p_render.add_argument("--no-footer", action="store_true", help="禁用页脚")

    p_list = sub.add_parser("list-themes", help="列出内置主题")

    p_init = sub.add_parser("init-theme", help="生成主题骨架")
    p_init.add_argument("path", type=str, help="目标目录")
    p_init.add_argument("--name", type=str, default="my-theme", help="主题名称")

    args = parser.parse_args()

    if args.cmd == "list-themes":
        for name in list_builtin_themes():
            print(name)
        return

    if args.cmd == "init-theme":
        init_theme_skeleton(_path(args.path), name=args.name)
        print(str(_path(args.path)))
        return

    if args.cmd == "render":
        input_path = _path(args.input)
        output_path = _path(args.output)
        theme_dir = _path(args.theme_dir) if args.theme_dir else None
        options = RenderOptions(
            theme_name=args.theme,
            theme_dir=theme_dir,
            title=args.title,
            footer_text=args.footer,
            header=not args.no_header,
            footer=not args.no_footer,
        )
        try:
            render_pdf(input_path=input_path, output_path=output_path, options=options)
        except ThemeNotFoundError as e:
            raise SystemExit(str(e)) from e
        return


if __name__ == "__main__":
    main()
