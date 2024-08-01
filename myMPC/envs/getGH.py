import numpy as np
from scipy.linalg import expm

# 定义参数
M = 10.4720
m = 5.0186
b = 0.1
g = 9.8
L = 0.3

I = 1/3 * m * (2*L)**2

# 计算常量 p
p = I * (m + M) + m * M * L**2

# 定义连续时间状态空间矩阵 A 和 B
A = np.array([[0, 1, 0, 0],
              [0, -(I + M * L**2) * b / p, (M**2 * g * L**2) / p, 0],
              [0, 0, 0, 1],
              [0, -(M * L * b) / p, M * g * L * (m + M) / p, 0]])

B = np.array([[0],
              [(I + M * L**2) / p],
              [0],
              [M * L / p]])

# 定义采样时间
Ts = 0.005  # 采样时间为 0.005 秒

# 计算离散时间状态空间矩阵 G
G = expm(A * Ts)  # 离散化后的 A 矩阵

# 计算离散化后的 B 矩阵 H
try:
    A_inv = np.linalg.inv(A)
except:
    A_inv = np.linalg.pinv(A)


H = np.dot(A_inv, (G - np.eye(A.shape[0]))).dot(B)


# 将 G 和 H 写入文本文件
np.savetxt('G.txt', G, delimiter=' ')
np.savetxt('H.txt', H, delimiter=' ')

# 输出结果
print("离散化后的 A 矩阵 G:")
print(G)
print("离散化后的 B 矩阵 H:")
print(H)
