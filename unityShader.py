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
except ImportError:
    from . import helper



oList="""[[["float"], "float(tex1D)", "HLSLSupport.cginc", 143, 0], [["float"], "float(tex2D)", "HLSLSupport.cginc", 144, 0], [["float"], "float(tex3D)", "HLSLSupport.cginc", 145, 0], [["float"], "float(texCUBE)", "HLSLSupport.cginc", 146, 0], [["float"], "float(tex1Dbias)", "HLSLSupport.cginc", 148, 0], [["float"], "float(tex2Dbias)", "HLSLSupport.cginc", 149, 0], [["float"], "float(tex3Dbias)", "HLSLSupport.cginc", 150, 0], [["float"], "float(texCUBEbias)", "HLSLSupport.cginc", 151, 0], [["float"], "float(tex1Dlod)", "HLSLSupport.cginc", 153, 0], [["float"], "float(tex2Dlod)", "HLSLSupport.cginc", 154, 0], [["float"], "float(tex3Dlod)", "HLSLSupport.cginc", 155, 0], [["float"], "float(texCUBElod)", "HLSLSupport.cginc", 156, 0], [["float"], "float(tex1Dgrad)", "HLSLSupport.cginc", 158, 0], [["float"], "float(tex2Dgrad)", "HLSLSupport.cginc", 159, 0], [["float"], "float(tex3Dgrad)", "HLSLSupport.cginc", 160, 0], [["float"], "float(texCUBEgrad)", "HLSLSupport.cginc", 161, 0], [["float"], "float(tex1Dproj)", "HLSLSupport.cginc", 163, 0], [["float"], "float(tex1Dproj)", "HLSLSupport.cginc", 164, 0], [["float"], "float(tex2Dproj)", "HLSLSupport.cginc", 165, 0], [["float"], "float(tex2Dproj)", "HLSLSupport.cginc", 166, 0], [["float"], "float(tex3Dproj)", "HLSLSupport.cginc", 167, 0], [["float"], "float(texCUBEproj)", "HLSLSupport.cginc", 168, 0], [["float"], "float(tex2Dproj)", "HLSLSupport.cginc", 172, 0], [["float"], "float(tex2Dproj)", "HLSLSupport.cginc", 178, 0], [["fixed"], "fixed(TerrainWaveGrass)", "TerrainEngine.cginc", 75, 0], [["float"], "float(SmoothCurve)", "TerrainEngine.cginc", 287, 0], [["float"], "float(TriangleWave)", "TerrainEngine.cginc", 290, 0], [["float"], "float(SmoothTriangleWave)", "TerrainEngine.cginc", 293, 0], [["float"], "float(UnityCalcDistanceTessFactor)", "Tessellation.cginc", 8, 0], [["float"], "float(UnityCalcTriEdgeTessFactors)", "Tessellation.cginc", 16, 0], [["float"], "float(UnityCalcEdgeTessFactor)", "Tessellation.cginc", 26, 0], [["float"], "float(UnityDistanceFromPlane)", "Tessellation.cginc", 37, 0], [["float"], "float(UnityDistanceBasedTess)", "Tessellation.cginc", 79, 0], [["float"], "float(UnityEdgeLengthBasedTess)", "Tessellation.cginc", 92, 0], [["float"], "float(UnityEdgeLengthBasedTessCull)", "Tessellation.cginc", 108, 0], [["float"], "float(ShadeVertexLights)", "UnityCG.cginc", 175, 0], [["half"], "half(ShadeSH9)", "UnityCG.cginc", 192, 0], [["float"], "float(MultiplyUV)", "UnityCG.cginc", 280, 0]]"""

vlist="""[[["FastSinCos"], "FastSinCos(float4val, outfloat4s, outfloat4c)", "TerrainEngine.cginc", 51, 0], [["TerrainBillboardGrass"], "TerrainBillboardGrass(inoutfloat4pos, float2offset)", "TerrainEngine.cginc", 122, 0], [["WavingGrassVert"], "WavingGrassVert(inoutappdata_fullv)", "TerrainEngine.cginc", 138, 0], [["WavingGrassBillboardVert"], "WavingGrassBillboardVert(inoutappdata_fullv)", "TerrainEngine.cginc", 147, 0], [["TerrainAnimateTree"], "TerrainAnimateTree(inoutfloat4pos, floatalpha)", "TerrainEngine.cginc", 183, 0], [["TerrainBillboardTree"], "TerrainBillboardTree(inoutfloat4pos, float2offset, floatoffsetz)", "TerrainEngine.cginc", 196, 0], [["TreeVertBark"], "TreeVertBark(inoutappdata_fullv)", "TerrainEngine.cginc", 336, 0], [["TreeVertLeaf"], "TreeVertLeaf(inoutappdata_fullv)", "TerrainEngine.cginc", 348, 0]]"""

inlist="""[[["unitySampleShadow"], "unitySampleShadow(float4shadowCoord)", "AutoLight.cginc", 25, 0], [["unitySampleShadow"], "unitySampleShadow(float4shadowCoord)", "AutoLight.cginc", 49, 0], [["unitySampleShadow"], "unitySampleShadow(float4shadowCoord)", "AutoLight.cginc", 73, 0], [["SampleCubeDistance"], "SampleCubeDistance(float3vec)", "AutoLight.cginc", 131, 0], [["unityCubeShadow"], "unityCubeShadow(float3vec)", "AutoLight.cginc", 136, 0], [["UnitySpotCookie"], "UnitySpotCookie(float4LightCoord)", "AutoLight.cginc", 196, 0], [["UnitySpotAttenuate"], "UnitySpotAttenuate(float3LightCoord)", "AutoLight.cginc", 200, 0], [["DirLightmapDiffuse"], "DirLightmapDiffuse(inhalf3x3dirBasis, fixed4color, fixed4scale, half3normal, boolsurfFuncWritesNormal, outhalf3scalePerBasisVector)", "Lighting.cginc", 38, 0], [["LightingLambert"], "LightingLambert(SurfaceOutputs, fixed3lightDir, fixedatten)", "Lighting.cginc", 60, 0], [["LightingLambert_PrePass"], "LightingLambert_PrePass(SurfaceOutputs, half4light)", "Lighting.cginc", 71, 0], [["LightingLambert_DirLightmap"], "LightingLambert_DirLightmap(SurfaceOutputs, fixed4color, fixed4scale, boolsurfFuncWritesNormal)", "Lighting.cginc", 79, 0], [["LightingBlinnPhong"], "LightingBlinnPhong(SurfaceOutputs, fixed3lightDir, half3viewDir, fixedatten)", "Lighting.cginc", 92, 0], [["LightingBlinnPhong_PrePass"], "LightingBlinnPhong_PrePass(SurfaceOutputs, half4light)", "Lighting.cginc", 107, 0], [["LightingBlinnPhong_DirLightmap"], "LightingBlinnPhong_DirLightmap(SurfaceOutputs, fixed4color, fixed4scale, half3viewDir, boolsurfFuncWritesNormal, outhalf3specColor)", "Lighting.cginc", 117, 0], [["Squash"], "Squash(infloat4pos)", "TerrainEngine.cginc", 159, 0], [["ExpandBillboard"], "ExpandBillboard(infloat4x4mat, inoutfloat4pos, inoutfloat3normal, inoutfloat4tangent)", "TerrainEngine.cginc", 271, 0], [["AnimateVertex"], "AnimateVertex(float4pos, float3normal, float4animParams)", "TerrainEngine.cginc", 298, 0], [["WorldSpaceLightDir"], "WorldSpaceLightDir(infloat4v)", "UnityCG.cginc", 89, 0], [["ObjSpaceLightDir"], "ObjSpaceLightDir(infloat4v)", "UnityCG.cginc", 104, 0], [["WorldSpaceViewDir"], "WorldSpaceViewDir(infloat4v)", "UnityCG.cginc", 119, 0], [["ObjSpaceViewDir"], "ObjSpaceViewDir(infloat4v)", "UnityCG.cginc", 125, 0], [["VertexLight"], "VertexLight(v2f_vertex_liti, sampler2DmainTex)", "UnityCG.cginc", 227, 0], [["ParallaxOffset"], "ParallaxOffset(halfh, halfheight, half3viewDir)", "UnityCG.cginc", 238, 0], [["Luminance"], "Luminance(fixed3c)", "UnityCG.cginc", 248, 0], [["DecodeLightmap"], "DecodeLightmap(fixed4color)", "UnityCG.cginc", 256, 0], [["EncodeFloatRGBA"], "EncodeFloatRGBA(floatv)", "UnityCG.cginc", 296, 0], [["DecodeFloatRGBA"], "DecodeFloatRGBA(float4enc)", "UnityCG.cginc", 305, 0], [["EncodeFloatRG"], "EncodeFloatRG(floatv)", "UnityCG.cginc", 312, 0], [["DecodeFloatRG"], "DecodeFloatRG(float2enc)", "UnityCG.cginc", 321, 0], [["EncodeViewNormalStereo"], "EncodeViewNormalStereo(float3n)", "UnityCG.cginc", 329, 0], [["DecodeViewNormalStereo"], "DecodeViewNormalStereo(float4enc4)", "UnityCG.cginc", 338, 0], [["EncodeDepthNormal"], "EncodeDepthNormal(floatdepth, float3normal)", "UnityCG.cginc", 349, 0], [["DecodeDepthNormal"], "DecodeDepthNormal(float4enc, outfloatdepth, outfloat3normal)", "UnityCG.cginc", 357, 0], [["UnpackNormalDXT5nm"], "UnpackNormalDXT5nm(fixed4packednormal)", "UnityCG.cginc", 363, 0], [["UnpackNormal"], "UnpackNormal(fixed4packednormal)", "UnityCG.cginc", 376, 0], [["Linear01Depth"], "Linear01Depth(floatz)", "UnityCG.cginc", 387, 0], [["LinearEyeDepth"], "LinearEyeDepth(floatz)", "UnityCG.cginc", 392, 0], [["ComputeScreenPos"], "ComputeScreenPos(float4pos)", "UnityCG.cginc", 418, 0], [["ComputeGrabScreenPos"], "ComputeGrabScreenPos(float4pos)", "UnityCG.cginc", 434, 0], [["UnityPixelSnap"], "UnityPixelSnap(float4pos)", "UnityCG.cginc", 447, 0], [["TransformViewToProjection"], "TransformViewToProjection(float2v)", "UnityCG.cginc", 460, 0], [["TransformViewToProjection"], "TransformViewToProjection(float3v)", "UnityCG.cginc", 464, 0]]"""

DEFINITION_LIST=[]

def init():
    global DEFINITION_LIST

    temp1 =json.loads(inlist)
    temp2 =json.loads(oList)
    temp3 =json.loads(vlist)
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
        print("---- %s" % sel)
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
        print("is endble!!")
        return helper.checkFileExt(self.view.file_name(),"shader")

    def is_visible(self):
        return self.is_enabled()

def plugin_loaded():
    sublime.set_timeout(init, 200)

# st2
if not helper.isST3():
    init()