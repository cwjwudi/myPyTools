import mujoco
import numpy as np

# 加载模型
model = mujoco.MjModel.from_xml_path('inverted_pendulum.xml')
data = mujoco.MjData(model)

# 更新模型状态（可选，取决于你的需求）
mujoco.mj_step(model, data)


# 获取部位质量
def get_body_mass(model, body_name):
    # 获取部位索引
    body_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, body_name)
    if body_id < 0:
        raise ValueError(f"Body '{body_name}' not found in the model.")

    # 获取部位的质量
    mass = model.body_mass[body_id]
    return mass


# 示例：获取特定部位的质量
body_name = 'pole'  # 替换为你想要查询的部位名称
try:
    mass = get_body_mass(model, body_name)
    print(f"部位 '{body_name}' 的质量: {mass:.4f} kg")
except ValueError as e:
    print(e)