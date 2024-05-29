import mmap

# 打开文件并映射到内存
with open("shared_memory.bin", "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)

    # 写入数据到共享内存
    data = b"123"
    mm.write(data)  # 写入数据 "123"

    # 关闭映射
    mm.close()
