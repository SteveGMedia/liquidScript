from Hooks import Hooks, Hook

"""
    By default, as per:

    RequiredAttrs = ['Author', 'Description', 'eventHooks']
    RequiredFuncs = ['onLoad', 'onUnload']

    in ScriptManager.py, this is bare minimum, what a plugin
    should look like. This may change in the future.
"""

class MyFirstPlugin:
    Author = "Seung"
    Description = "Just a test plugin. Nothing Special!"
    eventHooks = Hooks() 
    
    def __init__(self):
        pass
    
    def onLoad(self):
        print("Plugin Loaded!")

    def onUnload(self):
        print("Plugin Unloaded!")

    @eventHooks.Register("!help")
    def testFunc(self, *args, **kwargs):
        print("Called !help function.")
        print("Parameter Keys: ", list(kwargs.keys()))
        print("Parameter Values: ", list(kwargs.values()))