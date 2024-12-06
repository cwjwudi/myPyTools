# -*- coding: utf-8 -*-
"""
文件描述：生成ST文件
作者：Wenjie Cui
创建日期：2024.10.12
最后修改日期：2024.10.12
"""

from datetime import datetime


def generate_area_ID(base_name, number):
    number_str = str(int(number))
    zero_str = ''
    if int(number/10) == 0:
        zero_str = '00'
    elif int(number/100) == 0:
        zero_str = '0'
    # 组合字符串
    area_name = f"{base_name}{zero_str}{number_str}"
    return area_name


"""
2024.10.9
生成区域定义程序，并保存成文件
"""
def generate_navigation_definition(rectangles):
    # 打开一个文本文件以写入
    with open('actCfgArea.st', 'w', encoding="GB2312") as f:
        # 生成当前日期
        current_date = datetime.now().strftime("%Y年%m月%d日")

        # 文件内容
        head_content = f"""(* 
          文件名: actCfgArea.st
          描述: 自动生成的点位定义程序
          日期: {current_date}

          说明:
          - 该程序为自动生成，正确性需要自行判断
          - 请查看输出图形区域定义是否符合要求
        *) \nACTION actCfgArea: \n\n"""

        f.write(head_content)  # 写入程序头

        for rectangle in rectangles:
            area_index = int(rectangle['index'])
            AreaID = generate_area_ID(rectangle['name'] , rectangle['index'])
            Vaild = 'TRUE'
            StationID = int(rectangle['station_id'])
            BottomLeft_X = rectangle['bottom_left_x']
            BottomLeft_Y = rectangle['bottom_left_y']
            TopRight_X = rectangle['top_right_x']
            TopRight_Y = rectangle['top_right_y']

            f.write(f"gArea[{area_index}].Cfg.AreaID := '{AreaID}';\n")
            f.write(f"gArea[{area_index}].Cfg.Vaild := {Vaild};\n")
            f.write(f"gArea[{area_index}].Cfg.StationID := {StationID};\n")
            f.write(f"gArea[{area_index}].Cfg.BottomLeft.X := {BottomLeft_X:.3f};\n")
            f.write(f"gArea[{area_index}].Cfg.BottomLeft.Y := {BottomLeft_Y:.3f};\n")
            f.write(f"gArea[{area_index}].Cfg.TopRight.X := {TopRight_X:.3f};\n")
            f.write(f"gArea[{area_index}].Cfg.TopRight.Y := {TopRight_Y:.3f};\n\n")

        f.write("END_ACTION")

    print("数据已成功保存到 actCfgArea.st")


"""
2024.10.12
生成MoveAssembles定义程序，并保存成文件
"""
def generate_move_assembles_definition(rectangles):
    # 打开一个文本文件以写入
    with open('actAreaSet.st', 'w', encoding="GB2312") as f:
        # 生成当前日期
        current_date = datetime.now().strftime("%Y年%m月%d日")

        # 文件内容
        head_content = f"""(* 
          文件名: actAreaSet.st
          描述: 自动生成的Assemble定义程序
          日期: {current_date}

          说明:
          - 该程序为自动生成，正确性需要自行判断
          - 请查看输出图形区域定义是否符合要求
        *) \nACTION actAreaSet:  \n FOR i:= 1 TO ACP6D_MAX_SHUTTLES DO \n \n"""

        f.write(head_content)  # 写入程序头

        for rectangle in rectangles:
            AssembleName = rectangle['name'][:-4]  # 数组切片，去除Area
            AssembleAcc = ''
            AssembleVel = ''
            TargetPosX = rectangle['move_assemble_x']
            TargetPosY = rectangle['move_assemble_y']
            if 'Connect2' in AssembleName:
                AssembleName = AssembleName[0:-1] + 'Pos2'
                AssembleAcc = 'GO_TO_CONNECT_POS_ACC'
                AssembleVel = 'GO_TO_CONNECT_POS_VEL'
            elif 'Connect' in AssembleName:
                AssembleName = AssembleName + 'Pos'
                AssembleAcc = 'GO_TO_CONNECT_POS_ACC'
                AssembleVel = 'GO_TO_CONNECT_POS_VEL'
            elif 'Buffer' in AssembleName:
                AssembleAcc = 'GO_TO_BUFFER_POS_ACC'
                AssembleVel = 'GO_TO_BUFFER_POS_VEL'
            elif 'Process' in AssembleName:
                AssembleAcc = 'GO_TO_PROCESS_POS_ACC'
                AssembleVel = 'GO_TO_PROCESS_POS_VEL'
            elif 'ReadyPos' in AssembleName:
                AssembleName = AssembleName
                AssembleAcc = 'GO_TO_READY_POS_ACC'
                AssembleVel = 'GO_TO_READY_POS_VEL'
            elif 'Ready' in AssembleName:
                AssembleName = AssembleName + 'Pos'
                AssembleAcc = 'GO_TO_READY_POS_ACC'
                AssembleVel = 'GO_TO_READY_POS_VEL'
            elif 'BackPos'  in AssembleName:
                AssembleName = AssembleName
                AssembleAcc = 'GO_TO_BACK_POS_ACC'
                AssembleVel = 'GO_TO_BACK_POS_VEL'
            elif 'Back'  in AssembleName:
                AssembleName = AssembleName + 'Pos'
                AssembleAcc = 'GO_TO_BACK_POS_ACC'
                AssembleVel = 'GO_TO_BACK_POS_VEL'
            elif 'Test' in AssembleName:
                AssembleName = AssembleName + 'Pos'
                AssembleAcc = 'GO_TO_TEST_POS_ACC'
                AssembleVel = 'GO_TO_TEST_POS_VEL'
            else:
                AssembleAcc = '0'
                AssembleVel = '0'

            f.write(f"gShuttleMoveAssemblesIf[i].Goto{AssembleName}.Par.TargetPos.X := {TargetPosX:.3f};\n")
            f.write(f"gShuttleMoveAssemblesIf[i].Goto{AssembleName}.Par.TargetPos.Y := {TargetPosY:.3f};\n")
            f.write(f"gShuttleMoveAssemblesIf[i].Goto{AssembleName}.Par.Acc         := {AssembleAcc};\n")
            f.write(f"gShuttleMoveAssemblesIf[i].Goto{AssembleName}.Par.Vel         := {AssembleVel};\n\n")

        f.write("END_FOR\nEND_ACTION")

    print("数据已成功保存到 actAreaSet.st")

