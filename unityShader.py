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
# from xml.etree import ElementTree as ET
# from urllib import urlopen
try:
    import helper
    import defaultdefine
except ImportError:
    from . import helper
    from . import defaultdefine

DEFINITION_LIST=[]
U_Version =4

def init():
    global DEFINITION_LIST
    global U_Version 
    checkUnityVersion()
    temp1 =json.loads(defaultdefine.inlist)
    temp2 =json.loads(defaultdefine.olist)
    temp3 =json.loads(defaultdefine.vlist)
    temp4 =json.loads(defaultdefine.otherslist)
    
    if(U_Version == 5):
        temp5 =json.loads(defaultdefine.ulist)
        temp6 =json.loads(defaultdefine.uvlist)
        DEFINITION_LIST += temp4
        DEFINITION_LIST += temp5
        DEFINITION_LIST += temp6
    else:
        DEFINITION_LIST=temp1 +temp2+temp3 +temp4


def checkUnityVersion():
    global U_Version 
    settings = helper.loadSettings("UnityShader")
    SUnity_Version = settings.get("Unity_Version", "")
    if( len(SUnity_Version) == 0  ):
        U_Version =4
    elif "U4" in SUnity_Version:
        U_Version =4
    elif "U5" in SUnity_Version:
        U_Version =5

def checkUnityShaderRoot():
    global U_Version 
    settings = helper.loadSettings("UnityShader")
    Shader_path = settings.get("Shader_path", "")


    if U_Version== 5:
        U5_path =settings.get("U5_Shader_path", "")
        if len(U5_path)==0:
            sublime.error_message("U5_Shader_path no set")
            return False
        else:
            return U5_path 
    else:
        if len(Shader_path)==0 :
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
        # print("ShaderGotoDefinitionCommand")
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
        # print("matchList")
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
        # print("ShaderGotoDefinitionCommand-1")
       # print("----- item %s" %(item))
        definitionType=item[4]
        filepath=item[2]
        shader_root = checkUnityShaderRoot()
       # print("shader_root  %s" % shader_root)
        if shader_root != "":
           
            filepath=os.path.join(shader_root,filepath)
       # print("filepath  %s" % filepath)
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
