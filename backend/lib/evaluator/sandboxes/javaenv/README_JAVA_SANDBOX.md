# My notes: Java Sandbox API
So far only tested on Linux. 

TODO:
- Test java sandbox in Windows (subprocess)
- Implement untrusted code execution

DONE:
- local network socket python<->jvm

## py4j

py4j allows Python programs to communicate with JVM through a local network socket. 
Java program/JVM should run BEFORE trying to connect to the socket from Python program, otherwise the 
connection fails. 

## interpret with javac
Make sure interpreted java class files (package "sandbox_env") are present. If not:
- `javac -d ./backend/lib/sandbox/javaenv/ -cp ./backend/lib/sandbox/javaenv/py4j0.10.9.7.jar:./backend/lib/sandbox/javaenv/javaSandbox03.jar ./backend/lib/sandbox/javaenv/*.java`

## execute gateway java side
from JavaSandboxEnv directory
- `java sandbox_environment.SandboxEntryPoint` 

### subprocess
- capture_output sends stdout to javaEnv and not to console 
- text convert the stdout to string 
- shell=True is necessary for windows user 
- check=True Python throw an error if subprocess fails