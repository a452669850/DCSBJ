from utils.core import jsonPath
import json
import os

jsonPath = jsonPath

def writeJson(projectPath):
    print(jsonPath)
    if os.path.exists(jsonPath):
        with open(jsonPath, 'r', encoding='utf-8') as f1:
            loadDict = json.load(f1)
            projectList = loadDict['last_project_list']
            if projectList == []:
                loadDict['last_project_list'] = [projectPath]
            else:
                newList = projectList
                newList.append(projectPath)
                loadDict['last_project_list'] = list(set(newList))
            loadDict['last_project'] = projectPath
            loadDict['user_name'] = 'admin'

        with open(jsonPath, 'w', encoding='utf-8') as f2:
            json.dump(loadDict, f2)
    else:
        loadDict = {}
        loadDict['last_project_list'] = [projectPath]
        loadDict['user_name'] = 'admin'
        loadDict['last_project'] = projectPath
        with open(jsonPath, 'w', encoding='utf-8') as f2:
            json.dump(loadDict, f2)

def rewriteJson(value):
    if os.path.exists(jsonPath):
        with open(jsonPath, 'r', encoding='utf-8') as f1:
            loadDict = json.load(f1)
            loadDict['admin'] = value
        with open(jsonPath, 'w', encoding='utf-8') as f2:
            json.dump(loadDict, f2)
    else:
        newDict = {'admin' : value}
        with open(jsonPath, 'w', encoding='utf-8') as f3:
            newDict['last_project_list'] = []
            json.dump(newDict, f3)

def getProjectPath():
    # 获取最后一次打开的工程
	if os.path.exists(jsonPath):
		with open(jsonPath, 'r', encoding='utf-8') as f:
			loadDict = json.load(f)
			return loadDict['last_project']
	else:
		return None

def getProjectList():
    # 获取最近打开的工程列表
    if os.path.exists(jsonPath):
        with open(jsonPath, 'r', encoding='utf-8') as f:
            loadDict = json.load(f)
            return [x for x in loadDict['last_project_list']  if x]
    else:
        return []

def getProjectName(projectPath):
    # 根据工程路径获取工程名
	if projectPath:
		if os.path.exists(projectPath):
			with open(os.path.join(projectPath, 'projectDate.json'), 'r', encoding='utf-8') as f:
				loadDict = json.load(f)
				return loadDict['project_name']
		else:
			return None
	else:
		return None

def getLastUser():
    # 获取最后一次打开的工程用户名
    print(jsonPath)
    if os.path.exists(jsonPath):
        with open(jsonPath, 'r', encoding='utf-8') as f:
            loadDict = json.load(f)
            return loadDict['user_name']
    else:
        return None


def createProTree(projectPath):
    # 获取软件静态文件目录中JSON文件的规程树结构
    a = {
    "name" : "规程列表",
    "children" : [{"name" : "调试规程",
                    "children" : [{
                    "name" : "工艺",
                    "children" : []
                },
                {
                    "name" : "机械",
                    "children" : []
                },
                {
                    "name" : "电气",
                    "children" : []
                },
                {
                    "name" : "仪控",
                    "children" : [{
                                    "name" : "安全级",
                                    "children" : [{
                                                    "name" : "RRP15",
                                                    "children" : []
                                                },
                                                {
                                                    "name" : "RRP14",
                                                    "children" : []
                                                },]
                                },
                                {
                                    "name" : "非安全级",
                                    "children" : [
                                                {
                                                    "name" : "RCS09",
                                                    "children" : []
                                                },
                                                {
                                                    "name" : "RCS10",
                                                    "children" : []
                                                }
                                                ]
                                },]
                },]},
                {"name" : "其他规程",
                "children" : [
                            {
                            "name" : "采购",
                            "children" : []
                            },
                            {
                            "name" : "设计",
                            "children" : []
                            },
                ]}]
    }
    # proJsonPath = os.path.join(os.getcwd(), 'static', 'Pro.json')
    proJsonPath = os.path.join(projectPath, '.userdata', 'Pro.json')
    with open(proJsonPath, 'w', encoding='utf-8') as f:
        json.dump(a, f)

def getProTree(projectPath):
    proJsonPath = os.path.join(projectPath, '.userdata', 'Pro.json')
    with open(proJsonPath, 'r', encoding='utf-8') as f:
        loadDict = json.load(f)
    return loadDict

