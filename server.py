# server.py
import pathlib
import shlex
import subprocess

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Wechat-Moments")


def run_osascript(script, text):
    quoted_script = shlex.quote(script)
    command = ['osascript', quoted_script, text]  # 使用列表形式，避免shell注入
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return result.stdout.strip()


@mcp.tool()
def send_moments(text: str) -> str:
    script_path = pathlib.Path(__file__).parent / "wechat.scpt"
    try:
        run_osascript(script_path.__str__(), text)
        return "Send OK"
    except subprocess.CalledProcessError as e:
        return f"Failed: {e.stderr}"
    except Exception as e:
        return f"Failed: {e}"


def main():
    mcp.run()
