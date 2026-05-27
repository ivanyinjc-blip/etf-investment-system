#!/usr/bin/env python3
"""
微信公众号图片草稿箱推送脚本
功能：上传本地图片 → 保留源格式 → 创建图片消息草稿（小绿书/newspic）
API文档：https://developers.weixin.qq.com/doc/subscription/api/draftbox/draftmanage/api_draft_add.html

用法：
    python3 wx_draft_image.py <图片路径> [标题]
    
示例：
    python3 wx_draft_image.py cover.png "DeepSeek V4 + CC Switch 封面图"
"""

import sys
import json
import time
import os
import urllib.request
import urllib.error
from pathlib import Path

# ===== 配置区 =====
# 从环境变量或命令行参数读取
WX_APP_ID = os.environ.get("WX_APP_ID", "")
WX_APP_SECRET = os.environ.get("WX_APP_SECRET", "")

# Token 缓存文件（避免频繁获取，token有效期2小时）
TOKEN_CACHE = os.path.expanduser("~/.hermes/cache/wx_access_token.json")

# ===== Token 管理 =====
def get_access_token(app_id: str, app_secret: str) -> str:
    """获取微信公众号 access_token，带缓存"""
    # 检查缓存
    if os.path.exists(TOKEN_CACHE):
        with open(TOKEN_CACHE) as f:
            cache = json.load(f)
            if cache.get("app_id") == app_id and cache.get("expires_at", 0) > time.time():
                return cache["access_token"]

    # 重新获取
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"❌ 获取 access_token 失败: {e}")
        sys.exit(1)

    if "access_token" not in data:
        print(f"❌ 获取 access_token 失败: {data}")
        sys.exit(1)

    token = data["access_token"]
    expires_in = data.get("expires_in", 7200)

    # 写入缓存
    os.makedirs(os.path.dirname(TOKEN_CACHE), exist_ok=True)
    with open(TOKEN_CACHE, "w") as f:
        json.dump({
            "app_id": app_id,
            "access_token": token,
            "expires_at": time.time() + expires_in - 300,  # 提前5分钟刷新
        }, f)

    print(f"✅ Token 获取成功 (有效期 {expires_in}s)")
    return token


# ===== 上传永久图片素材 =====
def upload_permanent_image(token: str, image_path: str) -> str:
    """
    上传图片到微信永久素材库
    返回 media_id
    注意：永久素材必须用 multipart/form-data 上传
    """
    image_path = Path(image_path)
    if not image_path.exists():
        print(f"❌ 图片不存在: {image_path}")
        sys.exit(1)

    # 检查文件格式
    ext = image_path.suffix.lower()
    if ext not in (".jpg", ".jpeg", ".png", ".gif", ".bmp"):
        print(f"⚠️  警告: 文件格式 {ext} 可能不被微信支持，继续尝试...")

    file_size = image_path.stat().st_size
    file_size_mb = file_size / (1024 * 1024)
    print(f"📷 图片: {image_path.name} ({file_size_mb:.2f} MB)")

    if file_size > 10 * 1024 * 1024:
        print(f"❌ 图片过大 ({file_size_mb:.2f} MB)，微信限制 ≤10MB")
        sys.exit(1)

    # 构建 multipart/form-data
    boundary = "----WebKitFormBoundary" + os.urandom(16).hex()
    
    with open(image_path, "rb") as f:
        image_data = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="{image_path.name}"\r\n'
        f"Content-Type: image/{ext.lstrip('.')}\r\n\r\n"
    ).encode() + image_data + f"\r\n--{boundary}--\r\n".encode()

    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    req.add_header("Content-Length", str(len(body)))

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print(f"❌ 上传失败 (HTTP {e.code}): {err_body}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 上传失败: {e}")
        sys.exit(1)

    if "media_id" not in data:
        print(f"❌ 上传失败: {data}")
        sys.exit(1)

    media_id = data["media_id"]
    url_on_wx = data.get("url", "无")
    print(f"✅ 上传成功")
    print(f"   media_id: {media_id}")
    print(f"   微信URL:  {url_on_wx}")
    return media_id


# ===== 创建图片消息草稿 =====
def create_image_draft(token: str, media_id: str, title: str = "图片消息") -> dict:
    """
    创建图片消息草稿（小绿书/newspic）
    图片保留源格式，直接推送到草稿箱
    """
    # 图片消息结构
    draft_data = {
        "articles": [{
            "article_type": "newspic",
            "title": title,
            "content": "",
            "image_info": {
                "image_list": [
                    {"image_media_id": media_id}
                ]
            }
        }]
    }

    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    body = json.dumps(draft_data, ensure_ascii=False).encode()

    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print(f"❌ 创建草稿失败 (HTTP {e.code}): {err_body}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 创建草稿失败: {e}")
        sys.exit(1)

    if data.get("errcode", -1) != 0:
        print(f"❌ 创建草稿失败: {data}")
        sys.exit(1)

    media_id_draft = data.get("media_id", "未知")
    print(f"✅ 草稿创建成功")
    print(f"   草稿 media_id: {media_id_draft}")
    return data


# ===== 列出草稿（可选）=====
def list_drafts(token: str, count: int = 5):
    """列出最近的草稿"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={token}"
    body = json.dumps({"offset": 0, "count": count, "no_content": 1}).encode()

    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"⚠️  获取草稿列表失败: {e}")
        return

    items = data.get("item", [])
    print(f"\n📋 最近 {len(items)} 篇草稿:")
    for item in items:
        media_id = item.get("media_id", "?")
        update_time = item.get("update_time", 0)
        content = item.get("content", {})
        news_items = content.get("news_item", [])
        for ni in news_items:
            article_type = ni.get("article_type", "news")
            title = ni.get("title", "无标题")
            type_label = "🖼️ 图片" if article_type == "newspic" else "📄 图文"
            print(f"  {type_label} [{media_id}] {title}")


# ===== 主流程 =====
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n环境变量：")
        print("  WX_APP_ID      微信公众号 AppID")
        print("  WX_APP_SECRET  微信公众号 AppSecret")
        sys.exit(1)

    image_path = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else Path(image_path).stem

    # 验证配置
    app_id = WX_APP_ID
    app_secret = WX_APP_SECRET

    if not app_id or not app_secret:
        print("❌ 请设置环境变量 WX_APP_ID 和 WX_APP_SECRET")
        print("   或修改脚本顶部的 WX_APP_ID / WX_APP_SECRET")
        sys.exit(1)

    print("=" * 50)
    print("📤 微信公众号图片草稿箱推送")
    print("=" * 50)
    print(f"   图片: {image_path}")
    print(f"   标题: {title}")
    print(f"   AppID: {app_id[:8]}...")
    print()

    # Step 1: 获取 token
    print("--- Step 1: 获取 access_token ---")
    token = get_access_token(app_id, app_secret)

    # Step 2: 上传图片
    print("\n--- Step 2: 上传图片到永久素材库 ---")
    media_id = upload_permanent_image(token, image_path)

    # Step 3: 创建草稿
    print("\n--- Step 3: 创建图片消息草稿 ---")
    create_image_draft(token, media_id, title)

    # Step 4: 展示草稿列表
    print("\n--- Step 4: 草稿箱列表 ---")
    list_drafts(token)

    print("\n" + "=" * 50)
    print("✅ 完成！请到公众号后台草稿箱查看")
    print("   https://mp.weixin.qq.com")
    print("=" * 50)


if __name__ == "__main__":
    main()
