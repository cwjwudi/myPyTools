from opcua import Client
import time


class OPCUAClient:
    def __init__(self, server_url="opc.tcp://localhost:4840/freeopcua/server/"):
        self.server_url = server_url
        self.client = Client(server_url)
        self.connected = False

    def connect(self):
        if not self.connected:
            self.client.connect()
            self.connected = True
            print("连接成功")

    def disconnect(self):
        if self.connected:
            self.client.disconnect()
            self.connected = False
            print("已断开连接")

    def read_node(self, node_id):
        if not self.connected:
            raise Exception("客户端未连接，请先连接到服务器。")

        # 获取节点
        node = self.client.get_node(node_id)
        # 读取节点的值
        value = node.get_value()
        return value


# 示例用法
if __name__ == "__main__":
    node_id = "ns=6;s=::AsGlobalPV:gActLoadPosition"
    opcua_client = OPCUAClient()

    try:
        opcua_client.connect()  # 连接到服务器
        while True:
            value = opcua_client.read_node(node_id)  # 读取节点值
            print(f"当前值: {value}")
            time.sleep(1)  # 每秒读取一次

    except Exception as e:
        print(f"发生错误: {e}")

    finally:
        opcua_client.disconnect()  # 断开连接
