#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import functools
import os
import json
import re
import subprocess
import sys
import time
import codecs
from xml.etree import ElementTree as ET
from urllib import urlopen
try:
    import helper
    import defaultdefine
except ImportError:
    from . import helper
    from . import defaultdefine

DEFINITION_LIST=[]

def init():
    global DEFINITION_LIST
    temp1 =json.loads(defaultdefine.inlist)
    temp2 =json.loads(defaultdefine.oList)
    temp3 =json.loads(defaultdefine.vlist)
    DEFINITION_LIST=temp1 +temp2+temp3

def checkUnityShaderRoot():
    settings = helper.loadSettings("Unity3D-Shader")
    Shader_path = settings.get("Shader_path", "")
    if len(Shader_path)==0:
        sublime.error_message("Shader_path no set")
        return False
    return Shader_path


# build file definition when save file
class ShaderListener(sublime_plugin.EventListener):
    def __init__(self):
        self.lastTime=0

    def on_post_save(self, view):
        
        filename=view.file_name()
        if not filename:
            return
        if not helper.checkFileExt(filename,"shader"):
            return

class ShaderGotoDefinitionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # select text
        
        sel=self.view.substr(self.view.sel()[0])
        if len(sel)==0:
            # extend to the `word` under cursor
            sel=self.view.substr(self.view.word(self.view.sel()[0]))
        # find all match file
        # print("---- %s" % sel)
        matchList=[]
        showList=[]
        for item in DEFINITION_LIST:
            for key in item[0]:
                if key==sel:
                    matchList.append(item)
                    showList.append(item[1])

        if len(matchList)==0:
            sublime.status_message("Can not find definition '%s'"%(sel))
        elif len(matchList)==1:
            self.gotoDefinition(matchList[0])
        else:
            # multi match
            self.matchList=matchList
            on_done = functools.partial(self.on_done)
            self.view.window().show_quick_panel(showList,on_done)
        
    def on_done(self,index):
        if index==-1:
            return
        item=self.matchList[index]
        self.gotoDefinition(item)
    
    def gotoDefinition(self,item):
        definitionType=item[4]
        filepath=item[2]
        shader_root = checkUnityShaderRoot()
        print("shader_root  %s" % shader_root)
        if shader_root != "":
           
            filepath=os.path.join(shader_root,filepath)
        print("filepath  %s" % filepath)
        if os.path.exists(filepath):
            self.view.window().open_file(filepath+":"+str(item[3]),sublime.ENCODED_POSITION)
        else:
            sublime.status_message("%s not exists"%(filepath))

    def is_enabled(self):
        return helper.checkFileExt(self.view.file_name(),"shader")

    def is_visible(self):
        return self.is_enabled()

def plugin_loaded():
    sublime.set_timeout(init, 200)

# st2
if not helper.isST3():
    init()