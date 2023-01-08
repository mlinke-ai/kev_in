// package py4j.examples; // Adds class to package
package sandbox_env; // Adds class to package

import py4j.GatewayServer;

import java.util.LinkedList;
import java.util.List;
import java.lang.*;

public class SandboxEntryPoint {
    private JavaSandbox mySandbox;
    private int anyNumber;
    private static GatewayServer server;

    public SandboxEntryPoint() {
        anyNumber = 5;
        mySandbox = new JavaSandbox("This is some usercode");
        server = null;
    }

    public JavaSandbox getSandbox() {
        return mySandbox;
    }

    public int getNumber() {
        return this.anyNumber;
    }

    // Then, you create a main method. This main method could be located in another class.
    // The first thing you do in the main method is to initialize a GatewayServer and link it to an entry point
    public static void main (String[] args) {
    server = new GatewayServer(new SandboxEntryPoint()); // Port 25333
    // Start gateway to accept incoming Python requests.
    server.start();
    System.out.println("Gateway Server Started");
    }
}