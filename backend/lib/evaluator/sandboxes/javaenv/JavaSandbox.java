package sandbox_env; // Adds class to package

import java.util.LinkedList;
import java.util.List;
import java.lang.*;
import java.util.concurrent.TimeUnit;

import net.datenwerke.sandbox.*;

public class JavaSandbox{

    public String myValue;

    public JavaSandbox(String usercode) {
        this.myValue = usercode;
    }

    public void sayHello(){
        System.out.println("Hello World from Java Sandbox");
    }

    // run sandbox
    public String run()
    {
        /* init and get SandboxService */
        SandboxService sandboxService = SandboxServiceImpl.getInstance();

        SandboxedEnvironment<String> c = new SandboxedEnvironment<String>() {
            @Override
            public String execute() throws Exception
            {
                /* run untrusted code */
                System.out.println(myValue);

                /* return some value */
                return "This is the result";
            }
        };

        /* configure context */
        SandboxContext context = new SandboxContext();

        context.addClassForApplicationLoader(getClass().getName());
        // context.addClassForApplicationLoader("Test");

        // context.setMaximumRunTime(2, TimeUnit.SECONDS, SandboxContext.RuntimeMode.ABSOLUTE_TIME);

        // context.addClassPermission(SandboxContext.AccessType.PERMIT, "Test");
        // context.addClassPermission(SandboxContext.AccessType.PERMIT,UntrustedCode.class.getName());
        context.addClassPermission(SandboxContext.AccessType.DENY, "java.lang.System");
        context.addClassPermission(SandboxContext.AccessType.PERMIT, "java.io.PrintStream");

        /* run code in sandbox */
        SandboxedCallResult<String> result = sandboxService.runSandboxed(c.getClass(), context); // one more arg "this"
        //  SandboxedCallResult<List<String>> result = sandboxService.runSandboxed(UntrustedCode.class, context);

        /* output result */
        return result.get();

    }
}

// see for help:
// https://stackoverflow.com/questions/27524636/java-sandbox-api-denying-access-in-a-used-class
// https://stackoverflow.com/questions/18449528/java-sandbox-example-throwing-java-lang-noclassdeffounderror
/*
    public static void main(String[] args)
    {
    SandboxService sandboxService = new SandboxServiceImpl.getInstance(); // Enable sandbox service and install security manager
    SandboxServiceImpl.initLocalSandboxService();

    // Invoke Sandbox with custom ClassLoader
    SandboxedEnvironment<Object> c = new SandboxedEnvironment<Object>() {
        @Override
        public Object execute() throws Exception{
        // run untrusted code

        // return some value
        return null;
        }

    SandboxContext context = new SandboxContext();
    SandboxCallResult<Object> result = sandboxService.runSandboxed(c.getClass(), context);
    */


/* The runSandboxed methods accept a SandboxedEnvironment and a SandboxContext as input
* The context defines the permissions and configuration of the sandbox.
*
*/

/* Configuration of Sandbox
1. Class-level permissions
2. Package-level permissions
3. Filesystem permissions
4. Security permissions
5. ClassLoader guidance
6. Sandbox specific options



 Class Level Permission
e.g. allow access to java.lang (while). Deny access to java.lang.system
addClassPermission(AccessType, Mode, String)
AccessType - whitelist or blacklist
Mode - normal or prefix
String - the classname
addClassPermission(ClassPermission)


Sandbox Specific Options
setMaximumRunTime(long)
setMaximumStackDepth(int)

*/