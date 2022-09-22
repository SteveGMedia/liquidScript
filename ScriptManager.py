from os import listdir, path
from ScriptObject import ScriptObject
import sys

class ScriptManager:
    SCRIPT_DIR = "Scripts"
    INSTANCES = {}

    """
        Script Templating

        RequiredAttrs - In order to be classified as a script that the manager can read, we want to make sure
        that it contains some standard variables.

        RequiredFuncs - Similar to RequiredAttrs, these are the minimal functions a script must contain because
        we want to be able to cleanly load, and unload plugins with no garbage in memory.

        We can refactor this to use config files later.
    """
    RequiredAttrs = ['Author', 'Description', 'eventHooks']
    RequiredFuncs = ['onLoad', 'onUnload']

    """
        Returns a list of python file from self.SCRIPT_DIR
    """
    def _scanScripts(self):
        return [path.splitext(f)[0] for f in listdir(self.SCRIPT_DIR) if f.endswith('.py') and not f.startswith("__")]

    """
        Checks to see if a specific script exists in self.SCRIPT_DIR
    """
    def _hasScript(self, name):
        return name in self._scanScripts()

    """
        Any functions starting with __ and ending with __ are typically built-in python functions.
        As such, unless required for more sophisticated/advanced usage, we can simply ignore these.
    """
    def _mapAttrs(self, obj):
        return [_attr for _attr in obj.__dict__.keys() if not _attr.startswith('__')]

    """
        Checks to make sure a script contains the minimal requirements for variables and functions
        as per self.RequiredAttrs and self.RequiredFuncs. Fails check if either are false.
    """
    def _validScript(self, funcs, vars):
        hasMinFuncs = set(self.RequiredAttrs).issubset(vars)
        hasMinVars = set(self.RequiredFuncs).issubset(funcs)
        
        return (hasMinFuncs and hasMinVars)

    """
        See if the script is already loaded.
        Alternatively, we could also check sys.modules
    """
    def _isLoaded(self, scriptName):
        if scriptName in self.INSTANCES.keys():
            return True
        return False

    """
        Used to pass variables from the main application to the script.

        instance    -> Instance of class from the script.
        newAttrName -> Name of the variable in the plugin class you want to inject.
        attrValue   -> Value of the new variable.
    """
    def _inject(self, instance, newAttrName, attrValue):
        if not hasattr(instance, newAttrName):
            print("Injected: {0} = {1} on {2}".format(newAttrName, attrValue, instance))
            setattr(instance, newAttrName, attrValue)

    """
        This is used to call a registered function FROM a remote module, using hooks.
        Event is the event name to call within the plugin.
    """
    def _trigger_event(self, event, *args, **kwargs):
        for scriptName in self.INSTANCES.keys():
            self.INSTANCES[scriptName]._trigger_event(event, *args, **kwargs)
        
    def _unLoadScript(self, scriptName):
        if self._isLoaded(scriptName):
            """
                First call shutdown logic from the plugin to give it time to shut down gracefully.
            """
            self.INSTANCES[scriptName].INSTANCE.onUnload()

            """
                Kill any remnants of other imports that the script imported.
            """
            for _import in self.INSTANCES[scriptName].ClassImports:
                if _import in sys.modules:
                    del sys.modules[_import]

            """
                Finally get rid of the actual module, and lastly, the script instance itself.
            """
            scriptFullname = "{0}.{1}".format(self.SCRIPT_DIR, scriptName)

            if scriptFullname in sys.modules:
                del sys.modules[scriptFullname]
    
            del self.INSTANCES[scriptName]

    def _loadScript(self, scriptName):
        
        if self._hasScript(scriptName):
            lib = __import__("{0}.{1}".format(self.SCRIPT_DIR, scriptName))
            modules = self._mapAttrs(lib)
            
            importList = []

            for obj in modules:
                """
                    As a dumb hack to find the correct module, we can use scriptName and compare it to
                    the imported module to root out any other module that is imported as a result of
                    the script's dependencies. There are probably better ways of checking this.
                """
                if scriptName != obj:
                    continue
                
                print("Found Module: ", obj)

                if hasattr(lib, obj):
                    print("{0}: {1}".format(obj, lib))
                    scriptClass = getattr(lib, obj)
                    classes = self._mapAttrs(scriptClass)

                    for _class in classes:
                        
                        classObj = getattr(scriptClass, _class)
                        classAttrs = self._mapAttrs(classObj)
                        
                        classFuncs = [_attr for _attr in classAttrs if callable(getattr(classObj, _attr))]
                        classVars = list(set(classAttrs) ^ set(classFuncs))

                        isValid = self._validScript(classFuncs, classVars)

                        if isValid:
                            sob = ScriptObject(obj, _class, classFuncs, classVars, isValid, classObj(), classes)

                            if not self._isLoaded(obj):
                                self.INSTANCES[obj] = sob
                                self.INSTANCES[obj].INSTANCE.onLoad()
                            else:
                                print("Script seems to already be loaded. Try re-loading or unloading.")