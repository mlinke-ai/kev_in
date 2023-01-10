# Unit Test Java Sandbox

This unit test is written in pseudocode as the class `ExecuteJava` 
isn't deployed yet. The unit test is similarly structured to the
unit test in `test_pysandbox.py`, that tests the class `ExecutePython`.
The main difference between both sandboxes is, that we need to set up a
socket in `ExecuteJava` class, which is done with the `Py4J API`. 
This socket allows us to connect to the Java Virtual Machine (JVM) and 
call any method defined on the Java side in Python. Before we can access 
the Java side, we create a subprocess, which creates a Gateway on the Java
side from a Java-file called `SandboxEntryPoint` and afterwards we will create
a Gateway in Python. With the set upped connection to the JVM we can access
our Java sandbox class and push the untrusted user code to the corresponding
member function. The member function of the Java sandbox class will execute
the untrusted user code and give feedback to the Python backend. Subsequently,
the `ExecuteJava` class will kill the subprocess, that executes the mentioned
Java-file, and return the result to the `Evaluator` class.

#### Unit Test Pseudocode

> ***class TestJavaSandbox(unittest.TestCase):*** <br>
> > 
> > **def setUp(self) -> None:**<br>
> >       &emsp; """" Automatically call for every single test we run. """ <br>
> >       &emsp; self.jvmsandbox_instance = ExecuteJava() <br>
> ___
>
> > **def test_init_constructor(self) -> None:**<br>
> >      &emsp; """ Tests correct initialization of an instance of the ExecuteJava class. <br>
> >      &emsp; and check JVM connection""" <br>
> >      &emsp; self.assertIsNotNone(self.jvmsandbox_instance) <br> 
> ___
>
> > **def test_jvm_connection(self) -> None:**<br>
> >      &emsp; """ Test if JVM connection is present. """ <br>
> >      &emsp; self.assertTrue(self.jvmsandbox_instance.connectToJVM()) <br>
> ___
> 
> > @parameterized.expand([[someInput_1], [someInput_2], ..., [someInput_n]]) <br>
> > **def test_correct_user_code(self, test_input) -> None:** <br>
> >     &emsp; """ Tests user code which is correct. So all expected results are met. """ <br>
> >     &emsp; self.assertEqual(self.jvmsandbox_instance.exec_untrusted_code(test_input), EXPECTED RESULT) <br>
> ___
> 
> > @parameterized.expand([[someInput_1], [someInput_2], ..., [someInput_n]]) <br>
> > **def test_wrong_user_code(self, test_input) -> None:**<br>
> >     &emsp; """ Tests user code which is wrong. So at least one expected result is not met. """ <br>
> >     &emsp; self.assertNotEqual(self.jvmsandbox_instance.exec_untrusted_code(test_input), NOT EXPECTED RESULT) <br>
> ___
> 
> > @parameterized.expand([[infinite_loop]]) <br>
> > **def test_timeout(self, test_input) -> None:**<br>
> >     &emsp; """ Tests long execution time in user code. For example an infinite loop should result in a TimeoutError. """ <br>
> >     &emsp; self.assertEqual(self.jvmsandbox_instance.exec_untrusted_code(test_input), EXPECTED TIMEOUT) <br>
> ___
>
> > @parameterized.expand([[not_compilable]]) <br>
> > **def test_not_compilable(self, test_input) -> None:**<br>
> >     &emsp; """ Tests user code is not compilable -> COMPILER ERROR. For example SyntaxError. """ <br>
> >     &emsp; resultLog = self.jvmsandbox_instance.exec_untrusted_code(test_input) <br>
> >     &emsp; self.assertIs(resultLog, EXPECTED COMPILERERROR) <br>
> ___
> 
> > @parameterized.expand([[not_executable]]) <br>
> > **def test_not_executable(self, test_input) -> None:**<br>
> >     &emsp; """ Tests user code is not executable -> EXECUTE ERROR. For example ImportError. """ <br>
> >     &emsp; resultLog = self.jvmsandbox_instance.exec_untrusted_code(test_input) <br>
> >     &emsp; self.assertIs(resultLog, EXPECTED EXECUTEERROR) <br>
> ___
> 
> **if `__name__` == `'__main__'`:** <br>
>       &emsp; unittest.main()