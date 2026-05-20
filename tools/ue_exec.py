"""
外部 Python -> UE 远程执行桥
用法：
    python ue_exec.py "import unreal; unreal.log('hello')"
    python ue_exec.py @path/to/script.py
"""
import sys
import os
import time

# 把 Epic 自带的 remote_execution 加进 path
UE_PYTHON_PATH = r"D:\Program Files\Epic Games\UE_5.5\Engine\Plugins\Experimental\PythonScriptPlugin\Content\Python"
sys.path.insert(0, UE_PYTHON_PATH)
import remote_execution as re_mod

def run(code):
    cfg = re_mod.RemoteExecutionConfig()
    cfg.multicast_group_endpoint = ('239.0.0.1', 6766)
    cfg.multicast_bind_address = '127.0.0.1'
    cfg.multicast_ttl = 0

    re = re_mod.RemoteExecution(cfg)
    re.start()
    # 等 UE 节点广播自己
    for _ in range(50):
        if re.remote_nodes:
            break
        time.sleep(0.1)
    if not re.remote_nodes:
        print("ERROR: no UE node found. Is editor running with bRemoteExecution=true?")
        print("       Check Config/DefaultEngine.ini and restart UE.")
        re.stop()
        sys.exit(2)

    node_id = re.remote_nodes[0]['node_id']
    print(f"connecting to UE node: {node_id}", file=sys.stderr)
    re.open_command_connection(node_id)
    try:
        result = re.run_command(code, unattended=True, exec_mode='ExecuteFile', raise_on_failure=False)
        print("--- success ---" if result['success'] else "--- failed ---", file=sys.stderr)
        if result.get('output'):
            for entry in result['output']:
                t = entry.get('type', '')
                o = entry.get('output', '')
                print(f"[{t}] {o}")
        if not result['success']:
            print(f"RESULT={result.get('result', '')}", file=sys.stderr)
    finally:
        re.close_command_connection()
        re.stop()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python ue_exec.py <code-string>   OR   python ue_exec.py @script.py")
        sys.exit(1)
    arg = sys.argv[1]
    if arg.startswith("@"):
        with open(arg[1:], 'r', encoding='utf-8') as f:
            code = f.read()
    else:
        code = arg
    run(code)
