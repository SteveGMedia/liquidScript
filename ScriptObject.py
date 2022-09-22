class ScriptObject:

    def __init__(self, scriptName, script, functions, variables, integrity, classInstance, classImports):
        self.ScriptName = scriptName
        self.ClassRef = script
        self.ClassImports = classImports
        self.Functions = functions
        self.Variables = variables
        self.Integrity = integrity
        self.INSTANCE = classInstance

    def _scriptInfo(self):
        print("[~] Script File: ", self.ScriptName)
        print("[~] Script Class: ", self.ClassRef)
        print("[~] Class Imports: ", self.ClassImports)
        print("[~] Functions: ", self.Functions)
        print("[~] Variables", self.Variables)
        print("[~] Verified Valid: ", self.Integrity)
        print("[~] Instance: ", self.INSTANCE)

    """
        This triggers a specific event inside of a script. 
        We inject self as scriptObject into kwargs because the script needs to be able to reference itself
        from within decorator functions since the scope changes (See: Hooks.Register())
    """
    def _trigger_event(self, event, *args, **kwargs):
        if self.INSTANCE.eventHooks.HasHook(event):
            kwargs['scriptObject'] = self 
            self.INSTANCE.eventHooks[event].Fire(*args, **kwargs)

    """
        Can be used to inject variables into the script. Or anything really.
    """
    def _inject(self, instance, newAttrName, attrValue):
        if not hasattr(instance, newAttrName):
            print("Injected: {0} = {1} on {2}".format(newAttrName, attrValue, instance))
            setattr(instance, newAttrName, attrValue)