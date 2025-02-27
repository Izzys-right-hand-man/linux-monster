import sys
import subprocess

try:
  process = subprocess.run(['git', 'pull', 'origin', 'main'],text = True, capture_output = True, check = True)
  if process.stdout:
    print(process.stdout)
    sys.exit()
  

except subprocess.CalledProcessError as e:
  print(e.stderr)