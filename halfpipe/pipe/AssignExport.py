# -*- coding: utf-8 -*-
"""Script to export and import shaders by Fabien Meyran."""

import maya.cmds as cmds

class ExportShaders (object):
    # shaderExportFunction for HalfPipe - version 1.2 - 26/01/2018

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # function to export shaders
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    def output():

        selection = cmds.ls(sl=True)

        #ask the user where to export the shader scene file

        shaderSceneFile = cmds.fileDialog2(fileMode=0,caption="Export shaders",ff='Maya ASCII(*.ma)')
        allShds = cmds.radioButton(allShdsBox,q=True,sl=1)
        selShds = cmds.radioButton(selShdsBox,q=True,sl=1)

        try:
            cmds.delete('shadersAssignmentInfo')

        except:

            pass

        #exctracting the scene name defined by the user

        scenePathList = shaderSceneFile[0].split('/')
        sceneName = scenePathList[-1].split('.ma')

        #creating the assignementInfo node

        saInfo = cmds.createNode("geometryVarGroup", name='shadersAssignmentInfo')
        cmds.setAttr(saInfo+'.tx', lock=True ,keyable=False ,channelBox=False)
        cmds.setAttr(saInfo+'.ty', lock=True ,keyable=False ,channelBox=False)
        cmds.setAttr(saInfo+'.tz', lock=True ,keyable=False ,channelBox=False)
        cmds.setAttr(saInfo+'.rx', lock=True ,keyable=False ,channelBox=False)
        cmds.setAttr(saInfo+'.ry', lock=True ,keyable=False ,channelBox=False)
        cmds.setAttr(saInfo+'.rz', lock=True ,keyable=False ,channelBox=False)
        cmds.setAttr(saInfo+'.sx', lock=True ,keyable=False ,channelBox=False)
        cmds.setAttr(saInfo+'.sy', lock=True ,keyable=False ,channelBox=False)
        cmds.setAttr(saInfo+'.sz', lock=True ,keyable=False ,channelBox=False)
        cmds.setAttr(saInfo+'.v', lock=True ,keyable=False ,channelBox=False)


        n = 0

        shaderList = []

        #if the user asked for selection only, we take the selection as the list to proceed with

        if selShds:

            objectList = selection

        #else, we list all the type mesh objects from the scene

        if allShds:

            objectList = cmds.ls(typ='mesh')

        #Getting each shader for each object, and stocking the information as a string in the assingment info, as a "shaderInfo" attribut

        for object in objectList:

            shader = cmds.listConnections(cmds.listHistory(object,f=1),type='shadingEngine')
            numberOfVertices = cmds.polyEvaluate(object,v=True)
            shaderList.append(shader)
            cmds.addAttr(saInfo,ln='shaderInfo'+str(n),dt='string')

            objectNameList = object.split(':')


            #extract the name of the object if a namespace exists

            if len(objectNameList) > 1:

                objectName = objectNameList[-1]

            else:

                objectName = objectNameList[0]

            #if the object has no shader, then we just fill the attribut with text "has no shader"

            if not shader:

                cmds.setAttr(saInfo+'.shaderInfo'+str(n),object+' has no shader',type='string')

            else:

                cmds.setAttr(saInfo+'.shaderInfo'+str(n),objectName+' = '+shader[0]+ ', vtxID = '+str(numberOfVertices),type='string')

            n = n + 1



        if cmds.checkBox(includeBox,q=True,v=True):

            shadingEngines = cmds.ls(type='shadingEngine')

            for shader in shadingEngines:

                if shader != 'initialShadingGroup':

                    cmds.addAttr(saInfo,ln='shaderInfo'+str(n),dt='string')

                    cmds.setAttr(saInfo+'.shaderInfo'+str(n),shader+' is an unassigned shader',type='string')

                    shaderList.append(shader)

                    n = n + 1


        #selecting assignementInfo and shaders ready to export

        cmds.select(saInfo,r=True)

        for shader in shaderList:

            cmds.select(shader,ne=True,add=True)

        #export the files

        cmds.file(shaderSceneFile,op="v=0;p=17;f=0",typ="mayaAscii",es=True)

        #cleaning stuff

        cmds.select(cl=True)
        cmds.delete(saInfo)
        cmds.deleteUI('shaderAssignatorWindow')

    @staticmethod
    def launch():



        #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # interface
        #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


        if (cmds.window('shaderAssignatorWindow', exists=True)):

            cmds.deleteUI('shaderAssignatorWindow')

        cmds.window('shaderAssignatorWindow',title="Shader Assignator", titleBarMenu=True)

        cmds.columnLayout(cal='center',width=300,rowSpacing=10,columnAttach=('left', 65))
        cmds.separator(height=15,style='none')
        cmds.radioCollection()
        allShdsBox = cmds.radioButton( label='Export all shaders from scene',sl=True)
        selShdsBox = cmds.radioButton( label='Export shaders from selection')
        cmds.separator(height=5,style='none')
        includeBox = cmds.checkBox(label=' Include unassigned shaders',v=False)
        cmds.separator(height=1,style='none')
        cmds.button(label='Export shaders',align='center',height=50,width=170,command='output()')
        cmds.separator(height=5,style='none')
        cmds.setParent( '..' )

        cmds.showWindow()
