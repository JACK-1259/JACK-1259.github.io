import time

class WiFiNetwork:
    def __init__(self, connected=True):
        self.connected = connected

    def is_connected(self):
        return self.connected

class IoTDevice1:  # 조명
    def process_command(self, command):
        if command['action'] == 'light':
            print("[조명] 상태:", "ON" if command['on'] else "OFF")
            if 'timer' in command:
                print(f"[조명] {command['timer']}초 후 자동 OFF 설정됨.")
            return {"status": "success", "device": "light"}
        return {"status": "fail"}

class IoTDevice2:  # 에어컨
    def process_command(self, command):
        if command['action'] == 'ac':
            print("[에어컨] 상태:", "ON" if command['on'] else "OFF")
            print("[에어컨] 모드:", command.get('mode', 'N/A'))
            if 'timer' in command:
                print(f"[에어컨] {command['timer']}초 후 자동 OFF 설정됨.")
            return {"status": "success", "device": "ac"}
        return {"status": "fail"}

class Server:
    def __init__(self):
        self.device1 = IoTDevice1()
        self.device2 = IoTDevice2()

    def handle_request(self, command):
        if command['action'] == 'light':
            return self.device1.process_command(command)
        elif command['action'] == 'ac':
            return self.device2.process_command(command)
        else:
            return {"status": "unknown command"}

class App:
    def __init__(self, wifi, server):
        self.wifi = wifi
        self.server = server

    def send_command(self, command):
        print("[앱] 명령 전송 요청:", command)
        if not self.wifi.is_connected():
            print("[앱] 같은 Wi-Fi 네트워크에 연결해주세요.")
            return

        response = self.server.handle_request(command)
        print("[앱] 처리 결과:", response)

# 시뮬레이션 실행
wifi = WiFiNetwork(connected=True)  # 연결 여부 설정
server = Server()
app = App(wifi, server)

# 사용자 -> 앱: 조명 명령
command_light = {
    "action": "light",
    "on": True,
    "timer": 5
}
app.send_command(command_light)

print("\n---\n")

# 사용자 -> 앱: 에어컨 명령
command_ac = {
    "action": "ac",
    "on": True,
    "mode": "cool",
    "timer": 10
}
app.send_command(command_ac)

print("\n--- 네트워크 연결 실패 상황 ---\n")
# 연결 끊긴 상태에서 요청
wifi_off = WiFiNetwork(connected=False)
app_offline = App(wifi_off, server)
app_offline.send_command(command_light)
