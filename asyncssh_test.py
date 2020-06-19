import asyncio
import asyncssh
import sys
import os

# AsyncSSHの個人的な使い方
# AsyncSSH: Asynchronous SSH for Python
# https://asyncssh.readthedocs.io/en/latest/


# HOSTのIPを指定
HOST = "localhost"

# LOGINするユーザー名
USERNAME = "USER"

# RASキーをフルパスで指定 他の種類のキーでも行けるかも?(未確認)
CLIENT_KEY = r"RSA_KEY"


async def run_client():
    """HOSTにSSHで接続してlsコマンドを実行した結果をターミナルに表示
    """
    async with asyncssh.connect(HOST, username=USERNAME, client_keys=[CLIENT_KEY]) as conn:
        result = await conn.run("ls -l", check=True)
        print(result.stdout, end="")


async def run_client2():
    """HOSTにSSHで接続してbcコマンドを実行してプログラムを起動
        bcに数値を入力した戻り値を取得して結果をターミナルに表示
    """
    async with asyncssh.connect(HOST, username=USERNAME, client_keys=[CLIENT_KEY]) as conn:
        async with conn.create_process("bc") as process:
            for op in ["2+2", "1*2*3*4", "2^32"]:
                process.stdin.write(op + "\n")
                result = await process.stdout.readline()
                print(op, "=", result, end="")


async def run_client3():
    """HOSTにSSHで接続してip addrコマンドを実行し、その後ls コマンドを実行した結果を取得
        conn.runに引数としてcheck=Trueを追加するとコマンドが正常終了しなかった場合にraiseする
        check=Trueを指定しない場合はraiseせずそのまま次のコマンドを実行する
    """
    async with asyncssh.connect(HOST, username=USERNAME, client_keys=[CLIENT_KEY]) as conn:
        results = []
        results.append(await conn.run("/usr/sbin/ip addr", check=True))
        results.append(await conn.run("ls -l"))

        for result in results:
            print(result.stdout, end="")


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(run_client3())
    except (OSError, asyncssh.Error) as exc:
        sys.exit("SSH connection failed: " + str(exc))
