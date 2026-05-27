#!/usr/bin/env python3
"""
微信公众号 HTML 文章草稿箱推送脚本（通用版）
功能：
  1. 读取 HTML 文章 + 配图文件夹
  2. 自动去除与微信标题栏重复的元素（header/footer/标题H1/标签行）
  3. 上传配图到微信永久素材库
  4. 替换正文中的截图占位符为实际图片
  5. 推送图文草稿到公众号草稿箱

用法：
  python3 wx_push_article.py <文章文件夹路径> [--title 标题] [--author 作者]

示例：
  python3 wx_push_article.py "公众号/A04_斜杠命令"
  python3 wx_push_article.py "公众号/A04_斜杠命令" --title "自定义标题" --author "阿超AI"

依赖：Python 3.8+（仅标准库，无额外依赖）

环境变量：
  WX_APP_ID      微信公众号 AppID
  WX_APP_SECRET  微信公众号 AppSecret
"""

import sys
import json
import time
import os
import re
import urllib.request
import urllib.error
from pathlib import Path
from argparse import ArgumentParser

# ===== 配置 =====
WX_APP_ID = os.environ.get("WX_APP_ID", "wx945e86e48d0bab64")
WX_APP_SECRET = os.environ.get("WX_APP_SECRET", "49612916342c72b7cc9b874436142a0b")
TOKEN_CACHE = os.path.expanduser("~/.hermes/cache/wx_access_token.json")


# ===== Token 管理 =====
def get_access_token():
    if os.path.exists(TOKEN_CACHE):
        with open(TOKEN_CACHE) as f:
            cache = json.load(f)
            if cache.get("expires_at", 0) > time.time():
                return cache["access_token"]

    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WX_APP_ID}&secret={WX_APP_SECRET}"
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read().decode())

    if "access_token" not in data:
        print(f"❌ Token获取失败: {data}")
        sys.exit(1)

    token = data["access_token"]
    os.makedirs(os.path.dirname(TOKEN_CACHE), exist_ok=True)
    with open(TOKEN_CACHE, "w") as f:
        json.dump({
            "access_token": token,
            "expires_at": time.time() + data.get("expires_in", 7200) - 300,
        }, f)
    return token


# ===== 图片上传 =====
def upload_image(token: str, filepath: str) -> tuple:
    """上传图片到微信永久素材库，返回 (media_id, url)"""
    filepath = Path(filepath)
    if not filepath.exists():
        print(f"⚠️  图片不存在，跳过: {filepath.name}")
        return None, None

    ext = filepath.suffix.lower()
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "gif": "image/gif"}.get(ext.lstrip("."), "image/png")

    with open(filepath, "rb") as f:
        img_data = f.read()

    boundary = "----WebKitFormBoundary" + os.urandom(16).hex()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="{filepath.name}"\r\n'
        f"Content-Type: {mime}\r\n\r\n"
    ).encode() + img_data + f"\r\n--{boundary}--\r\n".encode()

    upload_url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    req = urllib.request.Request(upload_url, data=body, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"❌ 上传失败: {e.read().decode()}")
        return None, None

    if "media_id" not in result:
        print(f"❌ 上传失败: {result}")
        return None, None

    media_id = result["media_id"]
    url = result.get("url", "")
    print(f"  ✅ {filepath.name} → {media_id[:20]}...")
    return media_id, url


# ===== HTML 清理 =====
def clean_html_for_wechat(html: str, article_title: str) -> str:
    """
    清理 HTML 中与微信标题栏重复的元素：
    - <header> 块（系列名、标题H1、标签badge）
    - <article> 内的重复标题H1
    - blockquote 中的标签行
    - <footer> 块
    """
    # 1. 移除 <header> 整个块
    html = re.sub(r'<header[^>]*>.*?</header>', '', html, flags=re.DOTALL)

    # 2. 移除 <article> 内与文章标题相同的第一个 H1
    escaped_title = re.escape(article_title)
    html = re.sub(
        rf'<h1[^>]*>{escaped_title}</h1>\s*',
        '',
        html,
        count=1
    )

    # 3. 移除 blockquote 中的标签行
    html = re.sub(
        r'<p[^>]*><strong[^>]*>标签</strong>[^<]*</p>\s*',
        '',
        html
    )

    # 4. 移除 <footer> 块
    html = re.sub(r'<footer[^>]*>.*?</footer>', '', html, flags=re.DOTALL)

    return html


# ===== 替换截图占位符 =====
def replace_screenshots(html: str, images: dict) -> str:
    """
    替换正文中的截图占位符为实际图片
    占位符格式：[截图：XX - 描述]
    图片匹配规则：配图XX 对应 images 字典中 key 包含 XX 的图片
    """
    def replace_match(m):
        num = m.group(1)
        desc = m.group(2)
        # 查找匹配的图片 URL
        for key, (mid, url) in images.items():
            if num in key or f"配图{num}" in key or f"配图0{num}" in key:
                return f'<img src="{url}" alt="{desc}" style="max-width:100%;height:auto;display:block;margin:16px auto;border-radius:8px"/>'
        # 未找到匹配图片，保留原文
        return m.group(0)

    html = re.sub(
        r'\[截图：(\d+)\s*[-—]\s*([^\]]+)\]',
        replace_match,
        html
    )
    return html


# ===== 替换封面图占位 =====
def handle_cover(html: str, cover_mid: str, cover_url: str) -> str:
    """
    封面图只做微信 thumb_media_id，正文中删除封面占位
    不把封面图插入正文开头
    """
    # 直接删除封面占位块（封面图只用于thumb，不在正文展示）
    html = re.sub(
        r'<!--\s*封面图占位\s*-->.*?</div>\s*</div>\s*',
        '',
        html,
        count=1,
        flags=re.DOTALL
    )
    return html


# ===== 主流程 =====
def main():
    parser = ArgumentParser(description="微信公众号 HTML 文章推送到草稿箱")
    parser.add_argument("folder", help="文章文件夹路径")
    parser.add_argument("--title", help="文章标题（默认从HTML提取）")
    parser.add_argument("--author", default="阿超AI", help="作者名")
    parser.add_argument("--digest", help="文章摘要（默认自动截取）")
    parser.add_argument("--no-clean", action="store_true", help="跳过HTML清理")
    args = parser.parse_args()

    folder = Path(args.folder)
    if not folder.is_dir():
        print(f"❌ 文件夹不存在: {folder}")
        sys.exit(1)

    # 1. 查找 HTML 文件（优先 _wx.html）
    html_files = list(folder.glob("*_wx.html")) + list(folder.glob("*.html"))
    html_files = [f for f in html_files if not f.name.endswith("_配图") and "inline" not in f.name.lower()]
    if not html_files:
        print("❌ 未找到 HTML 文件")
        sys.exit(1)
    html_path = html_files[0]
    print(f"📄 文章: {html_path.name}")

    # 2. 查找图片文件
    image_files = sorted(folder.glob("*.png")) + sorted(folder.glob("*.jpg")) + sorted(folder.glob("*.jpeg"))
    print(f"🖼️  配图: {len(image_files)} 张")

    # 3. 读取 HTML
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 4. 提取标题
    title = args.title
    if not title:
        m = re.search(r'<title>(.*?)</title>', html)
        if m:
            title = m.group(1)
        else:
            title = folder.name
    print(f"📝 标题: {title}")

    # 5. 提取摘要
    digest = args.digest
    if not digest:
        # 从正文第一段提取
        m = re.search(r'<p[^>]*>([^<]{20,120})</p>', html)
        if m:
            digest = m.group(1).strip()[:120]
        else:
            digest = title
    print(f"📋 摘要: {digest[:60]}...")

    # 6. 获取 Token
    print("\n--- 获取 Token ---")
    token = get_access_token()
    print(f"✅ Token: {token[:20]}...")

    # 7. 上传图片
    print("\n--- 上传配图 ---")
    images = {}
    for img_path in image_files:
        mid, url = upload_image(token, str(img_path))
        if mid:
            images[img_path.stem] = (mid, url)

    if not images:
        print("❌ 没有成功上传的图片")
        sys.exit(1)

    # 8. 确定封面图（优先配图01，否则第一张）
    cover_key = None
    for key in images:
        if "01" in key or "配图1" in key:
            cover_key = key
            break
    if not cover_key:
        cover_key = list(images.keys())[0]
    cover_mid, cover_url = images[cover_key]
    print(f"\n🎨 封面图: {cover_key}")

    # 9. 清理 HTML
    if not args.no_clean:
        print("\n--- 清理 HTML 重复元素 ---")
        html = clean_html_for_wechat(html, title)
        print("✅ 已移除: header / 重复H1 / 标签行 / footer")

    # 10. 替换占位符
    print("\n--- 替换截图占位符 ---")
    html = replace_screenshots(html, images)
    # 替换封面占位
    html = handle_cover(html, cover_mid, cover_url)

    # 11. 创建草稿
    print("\n--- 推送草稿箱 ---")
    draft_data = {
        "articles": [{
            "article_type": "news",
            "title": title,
            "author": args.author,
            "digest": digest,
            "content": html,
            "content_source_url": "",
            "thumb_media_id": cover_mid,
            "need_open_comment": 1,
            "only_fans_can_comment": 0,
        }]
    }

    draft_url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    draft_body = json.dumps(draft_data, ensure_ascii=False).encode()
    req = urllib.request.Request(draft_url, data=draft_body, method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"❌ 推草失败: {e.read().decode()}")
        sys.exit(1)

    if "media_id" not in result:
        print(f"❌ 推草失败: {result}")
        sys.exit(1)

    draft_mid = result.get("media_id", "?")
    print(f"✅ 草稿创建成功")
    print(f"   media_id: {draft_mid}")

    print("\n" + "=" * 50)
    print("✅ 完成！去公众号后台查看：")
    print("   https://mp.weixin.qq.com → 图文素材")
    print("=" * 50)


if __name__ == "__main__":
    main()
