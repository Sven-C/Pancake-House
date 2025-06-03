#!/usr/bin/exec-suid -- /usr/local/bin/python3

import os
import pathlib
import secrets
import shutil
import subprocess
import sys

FLAG_FILE = pathlib.Path('/flag')
ADMIN_PIN_PATH = pathlib.Path('/challenge/admin_pin')
CHECK_ADMIN_PIN_PATH = pathlib.Path('/challenge/check-admin-pin')

def check_existence_flag():
    if not FLAG_FILE.exists():
        print(f'file {FLAG_FILE} not found', file=sys.stderr)
        sys.exit(1)

def fake_content(content):
    start_idx = content.index('{')
    end_idx = content.index('}')
    return 'pwm.college{' + ((end_idx-start_idx-1) * '_') + '}\n'

def hide_flag():
    content = FLAG_FILE.read_text()
    file_names = [f'flag{i}' for i in range(16)]
    root_dir = pathlib.Path('/tmp/treasury')
    if root_dir.exists():
        shutil.rmtree(root_dir)
    root_dir.mkdir()
    root_dir.chmod(0o700)
    real_file = secrets.choice(file_names)
    for file_name in file_names:
        path = root_dir / file_name
        if file_name == real_file:
            path.write_text(content)
        else:
            path.write_text(fake_content(content))
    FLAG_FILE.unlink()

def generate_admin_pin():
    new_admin_pin = os.urandom(16).hex()
    ADMIN_PIN_PATH.write_text(new_admin_pin)

def do_setup():
    check_existence_flag()
    hide_flag()
    generate_admin_pin()

def run_challenge():
    admin_pin = sys.stdin.buffer.read(1024)
    result = subprocess.run([CHECK_ADMIN_PIN_PATH],
                                env={'ADMIN_PIN_PATH': ADMIN_PIN_PATH},
                                input=admin_pin,
                                capture_output=True,)
    if result.returncode != 0:
        stderr = result.stderr.strip()
        print('You are not an admin')
    else:
        print('You are an admin!')

def main():
    do_setup()
    run_challenge()

if __name__ == '__main__':
    main()
