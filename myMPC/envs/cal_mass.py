import math


def capsule_volume(radius, height):
    # 计算圆柱体体积
    V_cylinder = math.pi * (radius ** 2) * height

    # 计算两个半球体积
    V_hemisphere = (2 / 3) * math.pi * (radius ** 3)

    # 总体积
    V_total = V_cylinder + V_hemisphere
    return V_total


def capsule_mass(radius, height, density):
    volume = capsule_volume(radius, height)
    mass = volume * density
    return mass


# pole参数
# <geom fromto="0 0 0 0.001 0 0.6" name="cpole" rgba="0 0.7 0.7 1" size="0.049 0.3" type="capsule"/>
radius = 0.049  # 半径 (米)
height = 0.6  # 高度 (米)
density = 1000  # 密度 (kg/m^3)

# 计算体积和质量
pole_volume = capsule_volume(radius, height)
pole_mass = capsule_mass(radius, height, density)

print(f"杆的体积: {pole_volume:.6f} m^3")
print(f"杆的质量: {pole_mass:.2f} kg")


# cart参数
# <geom name="cart" pos="0 0 0" quat="0.707 0 0.707 0" size="0.1 0.1" type="capsule"/>

radius = 0.1  # 半径 (米)
height = 0.2  # 高度 (米)
density = 1000  # 密度 (kg/m^3)

# 计算体积和质量
volume = capsule_volume(radius, height)
mass = capsule_mass(radius, height, density)

print(f"小车的体积: {volume:.6f} m^3")
print(f"小车的质量: {mass:.2f} kg")
