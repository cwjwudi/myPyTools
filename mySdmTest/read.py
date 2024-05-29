import mmap

# 打开文件并映射到内存
with open("shared_memory.bin", "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)

    # 从共享内存读取数据
    data = mm[:4]  # 读取前4个字节

    print("Data read from shared memory:", data)

    # 关闭映射
    mm.close()
