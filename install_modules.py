import subprocess
with open ("requirements.txt","r") as f:
    modules=f.read().split("\n")
modules=list(set(modules))
modules = filter(None, modules)

def install(module):
    subprocess.call(['pip', 'install', module])
    
for mod in modules:
    install(str(mod))

subprocess.call(['apt-get', 'install', 'libglib2.0-0'])
subprocess.call(['apt-get', 'install', 'libxrender-dev'])