import re
import os
import sys

def fix_md_image_path(md_file_path):
    """
    修复MD文件中的图片路径：将![desc](../dir/img.png) 改为 ![desc](../images/dir/img.png)
    :param md_file_path: MD文件的绝对/相对路径
    """
    # 校验文件是否存在
    if not os.path.exists(md_file_path):
        print(f"❌ 错误：文件 {md_file_path} 不存在！")
        return
    # 校验是否是md文件
    if not md_file_path.endswith(".md"):
        print(f"❌ 错误：{md_file_path} 不是Markdown文件（后缀非.md）！")
        return

    # 步骤1：备份原文件（加.bak后缀，防止修改出错）
    bak_file_path = md_file_path + ".bak"
    with open(md_file_path, "r", encoding="utf-8") as f_read, open(bak_file_path, "w", encoding="utf-8") as f_write:
        f_write.write(f_read.read())
    print(f"✅ 已备份原文件至：{bak_file_path}")

    # 步骤2：定义正则表达式，匹配MD图片语法
    # 匹配规则：![描述](../目录/图片.格式)，分组捕获【描述】、【原路径】、【图片格式】
    pattern = re.compile(
        r'!\[(.*?)\]\((\.\./.+?\.(png|jpg|jpeg|gif|bmp))\)',
        re.IGNORECASE  # 忽略图片格式的大小写（如PNG/Png都匹配）
    )

    # 步骤3：读取MD文件内容
    with open(md_file_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # 步骤4：定义替换回调函数，处理每个匹配的图片链接
    fix_count = 0  # 统计修改的图片数量

    def replace_func(match):
        nonlocal fix_count
        desc = match.group(1)  # 图片描述（可能为空）
        old_path = match.group(2)  # 原路径，如 ../公交车系统攻击事件排查/1.png
        # 跳过已含images的路径，避免重复修改
        if "/images/" in old_path:
            return match.group(0)
        # 分割原路径：../目录/图片.png → 分割为 ["..", "目录", "图片.png"]
        path_parts = old_path.split("/")
        # 拼接新路径：../images/目录/图片.png
        new_path = f"../images/{'/'.join(path_parts[1:])}"
        # 重组新的图片链接：![描述](新路径)
        new_img = f"![{desc}]({new_path})"
        fix_count += 1
        print(f"🔧 替换：{match.group(0)} → {new_img}")
        return new_img

    # 执行替换
    new_md_content = pattern.sub(replace_func, md_content)

    # 步骤5：将修改后的内容写回MD文件
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(new_md_content)

    # 输出最终结果
    if fix_count > 0:
        print(f"\n🎉 处理完成！共修改 {fix_count} 处图片路径")
    else:
        print(f"\nℹ️  未修改任何图片路径（无匹配项/所有路径已含images）")

if __name__ == "__main__":
    # 支持两种运行方式：1.命令行传参（python md_image_path_fix.py 你的文件.md） 2.手动输入文件路径
    if len(sys.argv) == 2:
        md_file = sys.argv[1]
        fix_md_image_path(md_file)
    else:
        print("===== MD图片路径自动修复工具 =====")
        md_file = input("请输入MD文件的路径（如：./bt1.md 或 C:/笔记/公交车系统攻击事件排查.md）：")
        fix_md_image_path(md_file)