import requests
import lzma
import json
import os


def main():
    # 下载并解压index文件
    index_url = "https://origin.warframe.com/PublicExport/index_zh.txt.lzma"
    manifest_base = "http://content.warframe.com/PublicExport/Manifest/"

    print("正在下载索引文件...")
    try:
        response = requests.get(index_url)
        response.raise_for_status()

        # 解压LZMA文件
        decompressed = lzma.decompress(response.content)
        lines = decompressed.decode("utf-8").splitlines()
    except Exception as e:
        print(f"下载或解压失败: {e}")
        return

    # 创建下载目录
    os.makedirs("warframe_public_export", exist_ok=True)

    # 遍历所有行并下载文件
    for line in lines:
        if not line.strip():
            continue

        # 解析文件名和完整哈希
        try:
            filename, hash_str = line.split("!", 1)
            file_url = f"{manifest_base}{line}"
        except ValueError:
            print(f"跳过无效行: {line}")
            continue

        # 下载文件
        print(f"正在下载 {filename}...")
        try:
            response = requests.get(file_url)
            response.raise_for_status()

            # 尝试解析JSON
            try:
                data = response.json()
                # 保存格式化JSON
                save_path = os.path.join("warframe_public_export", filename)
                with open(save_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            except json.JSONDecodeError:
                # 直接保存原始内容
                save_path = os.path.join("warframe_public_export", filename)
                with open(save_path, "wb") as f:
                    f.write(response.content)

            print(f"成功保存到 {save_path}")

        except requests.RequestException as e:
            print(f"下载失败: {e}")
        except Exception as e:
            print(f"处理文件时出错: {e}")


if __name__ == "__main__":
    main()