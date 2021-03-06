from utils.AcountModels import *


class deleteData:

    @classmethod
    def userDelete(cls, username, groupname):
        user = User.get(username=username)
        group = Group.get(name=groupname)
        if len(UserGroup.get_ug_by_user_id(user_id=user.id)) != 1:
            UserGroup.delete_user_from_group(user_id=user.id, group_id=group.id)
        else:
            UserGroup.delete_user_from_group(user_id=user.id, group_id=group.id)
            user.delete_instance()

    @classmethod
    def deleteGroup(cls, groupname, member):
        usersname = [str(x) for x in member.split(',')]
        group = Group.get(name=groupname)
        if usersname == ['']:
            group.delete_instance()
        else:
            for username in usersname:
                user = User.get(username=username)
                if len(UserGroup.get_groups_of_user(user_id=user.id)) == 1:
                    UserGroup.delete_user_from_group(user_id=user.id, group_id=group.id)
                    user.delete_instance()
                UserGroup.delete_user_from_group(user_id=user.id, group_id=group.id)
            group.delete_instance()


class selectData:

    @classmethod
    def selectGroupID(cls, name):
        gops = Group.select().where(Group.name == name)
        for gop in gops:
            return gop.id

    @classmethod
    def selectOperation(cls, name):
        gops = Operation.select().where(Operation.name == name)
        for gop in gops:
            return gop.id

    @classmethod
    def selectOperationGroup(cls, id):
        groupOpera = (Operation
                      .select()
                      .join(GroupOperatePermission)
                      .join(Group)
                      .where(Group.id == id))
        return groupOpera
