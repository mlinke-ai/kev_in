import os
import subprocess

from pathlib import Path
from py4j.java_gateway import JavaGateway, GatewayParameters, GatewayClient

__all__ = ["ExecuteJava"]

class ExecuteJava:
    pass

    # def __init__(self):
    #     self.javaEnvProcess = None
    #
    # def kill_subprocess(self):
    #     # if self.javaEnvProcess is not None:
    #     #     self.javaEnvProcess.kill()
    #     # return
    #
    #     try:
    #         self.javaEnvProcess.communicate(timeout=5)
    #     except:
    #         print("kill process")
    #         self.javaEnvProcess.kill()
    #     # print(self.javaEnvProcess.communicate()) # Get output buffer (stdout, stderr)
    #
    # def build_java_gateway(self):
    #     abPathDirJavaSandbox = Path(os.path.dirname(__file__))
    #
    #     abPathSandboxJar = os.path.join(abPathDirJavaSandbox, 'javaSandbox03.jar')
    #     abPathPy4JJar = os.path.join(abPathDirJavaSandbox, 'py4j0.10.9.7.jar')
    #
    #     # execute java program
    #     self.javaEnvProcess = subprocess.Popen(
    #         ['java', '-cp', '{0}:{1}:{2}'.format(abPathPy4JJar, abPathSandboxJar, abPathDirJavaSandbox),
    #          'sandbox_env.SandboxEntryPoint'], shell=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #
    #     print(self.javaEnvProcess.stdout.readline())  # Gateway Server Started "DEBUG"
    #
    # def do_stack_operation(self):
    #     gateway = JavaGateway()
    #     mySandbox = gateway.entry_point.getSandbox()
    #     print(mySandbox)
    #     print(gateway.entry_point.getNumber())
    #     try:
    #         print(mySandbox.run())
    #     except Exception:
    #         gateway.shutdown()
    #         self.kill_subprocess()
    #     gateway.shutdown()

        # input() # wait

        # self.gateway = JavaGateway()
        # self.mySandbox = self.gateway.entry_point

        # from py4j.java_gateway import (
        #     JavaGateway, CallbackServerParameters, GatewayParameters,
        #     launch_gateway)
        # # launch Java side with dynamic port and get back the port on which the
        # # server was bound to.
        # port = launch_gateway()
        #
        # # connect python side to Java side with Java dynamic port and start python
        # # callback server with a dynamic port
        # gateway = JavaGateway(
        #     gateway_parameters=GatewayParameters(port=port),
        #     callback_server_parameters=CallbackServerParameters(port=0))
        #
        # # retrieve the port on which the python callback server was bound to.
        # python_port = gateway.get_callback_server().get_listening_port()
        #
        # # tell the Java side to connect to the python callback server with the new
        # # python port. Note that we use the java_gateway_server attribute that
        # # retrieves the GatewayServer instance.
        # gateway.java_gateway_server.resetCallbackClient(
        #     gateway.java_gateway_server.getCallbackClient().getAddress(),
        #     python_port)
        #
        # # Test that callbacks work
        # from py4j.tests.java_callback_test import IHelloImpl
        # hello = IHelloImpl()
        # example = gateway.jvm.py4j.examples.ExampleClass()
        # example.callHello(hello)
