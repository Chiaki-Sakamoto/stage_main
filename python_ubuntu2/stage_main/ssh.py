import paramiko


class Ssh():
    def __init__(self, master=None):
        super().__init__()
        self.IP = "192.168.2.4"
        self.User_name = "pi"
        self.Password = "laserplasma"

    def ssh_connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(
            paramiko.WarningPolicy())  # known_hosts がなくても処理実行
        self.client.load_system_host_keys()  # ./ssh/known_hosts の読み込み
        self.client.connect(self.IP, username=self.User_name,
                            password=self.Password, timeout=5.0)  # ssh 接続
        print("ラズパイにssh 接続しました")

    def get_volt(self):
        self.stdin, self.stdout, self.stderr = self.client.exec_command(
            "/home/pi/ ; python3 pressure.py")  # stdout に処理結果
        cmd_result = ""  # 結果を入れる変数
        for line in self.stdout:  # stdout の結果をcmd_result に入れる
            cmd_result += line
        volt = float(cmd_result[:-2])
        return volt

    def ssh_close(self):
        self.client.close()
        del self.client, self.stdin, self.stdout, self.stderr
        print("ssh disconnected")
        # A = int(cmd_result[:-2])
        # print(A*2)


def main():
    app = Ssh()  # Ssh をインスタンス化
    app.ssh_connect()
    volt = app.get_volt()
    print("V=", volt, "V")
    print("P=", (volt-0.590)/3.975, "MPa")
    app.ssh_close()


if __name__ == "__main__":  # python3 ssh.py で実行したら
    main()  # main 関数を実行
