# -*- coding: utf-8 -*-
"""Script to export and import shaders by Fabien Meyran."""

import maya.cmds as cmds
import os

class ImportShaders (object):
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # function to select folder
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    def folderSelection():

        scenePath = cmds.fileDialog2(fileMode=3, caption="Shaders folder")
        cmds.textField(folderNameBox ,e=True,it=str(scenePath[0]))

        scenesList = ','.join(os.listdir(scenePath[0])).replace(".ma", "")
        cmds.textField(scenesListBox ,e=True,it=scenesList)

    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # function to apply shaders
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    def applyShaders(rfrsh,only,scenesList):

        scenePath = cmds.textField(folderNameBox ,q=True,tx=True)

        for sceneName in scenesList:

            if only == 0:

                try:

                    cmds.delete(sceneName+':*')
                    cmds.namespace(rm=sceneName)


                except:
                    pass

                print sceneName

                shaderNamespace = sceneName
                cmds.file(scenePath+'/'+sceneName+'.ma',i=True,ignoreVersion=True,mergeNamespacesOnClash=False,namespace=shaderNamespace,options="v=0;p=17;f=0",pr=True)

            if only == 1:


                shaderNamespace = sceneName+'ImpOnly'

                cmds.file(scenePath+'/'+sceneName+'.ma',i=True,ignoreVersion=True,mergeNamespacesOnClash=False,namespace=shaderNamespace,options="v=0;p=17;f=0",pr=True)

                selection = cmds.select(shaderNamespace+'*:shadersAssignmentInfo',r=True)
                shaderNamespace = cmds.ls(sl=True)[0].split(':')[0]

            saInfoAttrs = cmds.listAttr(shaderNamespace+':shadersAssignmentInfo')

            #getting the values from the assignmentInfo and operating them

            shaderInfoAttrList = []
            missingObjects = []
            missingObjShader = []

            #we extract each attribut "shaderInfo" name from the assignmentInfo

            for attribut in saInfoAttrs:

                attributName = attribut.split('shaderInfo')

                if len(attributName) == 2:

                    shaderInfoAttrList.append(attribut)

            #we get the info from each shading info attribut

            for attribut in shaderInfoAttrList:

                shaderInfo = cmds.getAttr(shaderNamespace+':shadersAssignmentInfo.'+attribut).split(',')[0].split(' = ')


                if len(shaderInfo) == 2:

                    vtxID = cmds.getAttr(shaderNamespace+':shadersAssignmentInfo.'+attribut).split(',')[1].split(' = ')[1]

                    #if the object has the lambert1 shader (initialShadingGroup), then select the existing initialShadingGroup

                    if shaderInfo[1] == 'initialShadingGroup':

                        cmds.select('initialShadingGroup',ne=True,r=True)

                    else:

                        cmds.select(shaderNamespace+':'+shaderInfo[1],ne=True,r=True)


                    shadingGroup = cmds.ls(sl=True)

                    try:

                        cmds.select(cmds.listRelatives('*:*'+shaderInfo[0],parent=True, fullPath=True),r=True)

                    except:

                        try:

                            cmds.select(cmds.listRelatives(shaderInfo[0],parent=True, fullPath=True),r=True)

                        except:

                            missingObjects.append(shaderInfo[0])
                            missingObjShader.append(' shadered with : '+shaderInfo[1])



                    if len(cmds.ls(sl=True)) > 1:

                        multiple = 1

                    else:

                        multiple = 0

                    objectToCheck = []

                    if multiple == 0:

                        if only == 0:

                            cmds.sets(e=True,forceElement=shadingGroup[0])

                    if multiple == 1:

                        allNodes = cmds.ls(ap=True,type='mesh')

                        for node in allNodes:

                            if len(node.split(shaderInfo[0])) > 1:

                                objectToCheck.append(node)

                        for object in objectToCheck:

                            numberOfVertices = cmds.polyEvaluate(object,v=True)

                            if str(numberOfVertices) == str(vtxID):

                                if only == 0:
                                    cmds.select(object,r=True)
                                    cmds.sets(e=True,forceElement=shadingGroup[0])

            if cmds.checkBox(mustDeleteBox,q=True,v=True):

                cmds.delete(shaderNamespace+':shadersAssignmentInfo')

        #if object are missing

        if len(missingObjects) > 0:

            objectListString = '\n'.join(missingObjects)
            shaderListString = '\n'.join(missingObjShader)

            if (cmds.window('warningWindow', exists=True)):

                cmds.deleteUI('warningWindow')

            cmds.window('warningWindow',title="Warning", titleBarMenu=True)
            cmds.columnLayout(cal='center',width=440,rowSpacing=10,columnAttach=('left', 40))
            cmds.separator(height=15,style='none')
            cmds.text(label='Following objects were missing, or have a different name in the shader scene :', al='left')
            cmds.rowColumnLayout(numberOfColumns=4,columnWidth=[(1,10), (2, 180), (3, 300), (4, 10)])
            cmds.text(label='',al='left')
            cmds.text(label=objectListString, al='left')
            cmds.text(label=shaderListString, al='left',en=False)
            cmds.text(label='',al='left')
            cmds.separator(height=20,style='none')
            cmds.showWindow()

        #end of the "else apply" function

        cmds.select(cl=True)
        cmds.deleteUI('shaderImportWindow')

    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # function to check user interface data
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    def checking():

        importAssign = cmds.radioButton(importAssignBox,q=True,sl=1)
        importOnly = cmds.radioButton(importOnlyBox,q=True,sl=1)

        scenesList = cmds.textField(scenesListBox,q=True,tx=True).replace(' ','').split(',')

        existingShadersList = []


        for sceneName in scenesList:

            if cmds.namespace(exists=sceneName):

                existingShadersList.append(sceneName)

            else:

                pass

        if len(existingShadersList) > 0:

            if importOnly == 1:

                if cmds.namespace(exists=sceneName):

                    confirmRefresh = cmds.confirmDialog(title='Import only', ma='center',message='The shaders your trying to import already exist in the scene. To avoid clashing names, they will have an "import only" namespace.', button=['Okay'])

                applyShaders(1,1,scenesList)

            else:

                confirmRefresh = cmds.confirmDialog(title='Refresh shaders', ma='center',message='The following shaders already exist in the scene : '+','.join(existingShadersList).replace(".ma", "")+'.\nWould you like to refresh them ? (this will delete the shaders and import them again.)', button=['Yes','No'])

                if confirmRefresh == 'Yes':

                    if importAssign:

                        applyShaders(1,0,scenesList)

                    else:

                        applyShaders(1,1,scenesList)

                if confirmRefresh == 'No':

                    pass

        #else, we execute the apply function

        else:


            if importAssign == True:

                applyShaders(0,0,scenesList)

            else:

                applyShaders(0,1,scenesList)

    #end of the input function

    @staticmethod
    def launch():
        #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # interface
        #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

        if (cmds.window('shaderImportWindow', exists=True)):

            cmds.deleteUI('shaderImportWindow')

        cmds.window('shaderImportWindow',title="Import shaders", titleBarMenu=True)
        cmds.columnLayout()
        cmds.separator( height=13, style ='none' )

        cmds.rowColumnLayout(numberOfColumns=4,columnWidth=[(1,10), (2, 140),(3, 380),(4,35)])
        cmds.text(label='', al='left')
        cmds.text(label='Shaders folder : ', al='left')
        folderNameBox = cmds.textField()
        cmds.symbolButton( image='folder-open.png',command ='folderSelection()')
        cmds.setParent('..')
        cmds.separator( height=8, style ='none' )

        cmds.rowColumnLayout(numberOfColumns=4,columnWidth=[(1,10), (2, 140),(3, 380),(4,35)])
        cmds.text(label='', al='left')
        cmds.text(label='Shaders to import : ', al='left')
        scenesListBox = cmds.textField()
        cmds.setParent('..')
        cmds.separator( height=5, style ='none' )

        cmds.rowColumnLayout(numberOfColumns=2,columnWidth=[(1,150), (2, 350)])
        cmds.text(label='', al='left')
        cmds.text(label='Names must be separate with a "," and whitespaces are not allowed.', al='left',en=False)
        cmds.setParent('..')
        cmds.separator( height=20, style ='none' )

        cmds.rowColumnLayout(numberOfColumns=3,columnWidth=[(1,150), (2, 150),(3, 150)])
        cmds.text(label='', al='left')
        cmds.radioCollection()
        importAssignBox = cmds.radioButton( label='Import and assign',sl=True)
        importOnlyBox = cmds.radioButton( label='Import shaders only')
        cmds.setParent('..')
        cmds.separator( height=13, style ='none')

        cmds.rowColumnLayout(numberOfColumns=2,columnWidth=[(1,150), (2, 280)])
        cmds.text(label='', al='left')
        mustDeleteBox = cmds.checkBox(label='Delete Assignator info nodes after import', value=1)
        cmds.setParent('..')
        cmds.separator( height=20, style ='none')

        cmds.rowColumnLayout(numberOfColumns=3,columnWidth=[(1,188), (2, 188),(3, 191)])
        cmds.text(label='', al='left')
        cmds.button(label='Import shaders',align='center',height=45,command='checking()')
        cmds.text(label='', al='left')
        cmds.separator(height=13, style ='none' )

        cmds.showWindow()