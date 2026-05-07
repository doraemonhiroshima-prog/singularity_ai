import os
import re


def clean_line(line):
    # コメント削除
    if "#" in line:
        line = line.split("#")[0]

    # 明らかなゴミだけ除去（弱めにする）
    if re.search(r"[�]{2,}", line):
        return ""

    return line


def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        new_lines = []

        for line in lines:
            cleaned = clean_line(line)

            # ★ 空行だけ除外（コードは残す）
            if cleaned.strip() != "":
                new_lines.append(cleaned + "\n")

        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        print(f"✔ FIXED: {filepath}")

    except Exception as e:
        print(f"❌ ERROR: {filepath} -> {e}")


def main():
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                process_file(os.path.join(root, file))


if __name__ == "__main__":
    main()
