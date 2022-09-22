from ScriptManager import ScriptManager

mgr = ScriptManager()

if __name__ == "__main__":
    scriptList = mgr._scanScripts()
    print("Available Scripts: ", scriptList)

    if len(scriptList) > 0:
        test = scriptList[0] # First script should be the test module
        mgr._loadScript(test)

        """
            We can inject new variables into our plugins as needed to pass data to them.
            The following example shows a string being injected and accessed.

            We will inject a new variable with the name "mystring", and the same value as
            tempData.
        """
        tempData = "This is a test string to be injected."

        testInstance = mgr.INSTANCES[test].INSTANCE
        mgr._inject(testInstance, "mystring", tempData)

        print(mgr.INSTANCES[test].INSTANCE.mystring)

        """
            Fires the event !help, and passes arbitrary data in this case.
        """
        mgr._trigger_event("!help", data={ "Hello" : "World" }, testString="This is a test string.")

        """
            Unloads the script and removes traces of it from sys.modules.
        """
        mgr._unLoadScript(test)
    else:
        print("No Scripts found!")