from utils.WorkModels import NetworkConfig, PointGroup, PointModel


class getListData:

    @classmethod
    def getNtworkConfigData(cls):
        lis = []
        configs = NetworkConfig.select().distinct()
        row = 1
        for i in configs:
            lis.append([row, i.name, i.desc, i.ip, str(i.port)])
            row += 1
        return lis

    @classmethod
    def create_group(cls, name):
        try:
            PointGroup.get(group_name=name)
        except:
            points = PointModel.all_points()
            PointGroup.create_group(group_name=name, points=points)

    @classmethod
    def search_NetworkConfig(cls, text):
        lis = []
        configs = NetworkConfig.select().where(
            (NetworkConfig.slot.contains(text)) |
            (NetworkConfig.description.contains(text))
        )
        if len(configs):
            for config in configs:
                lis.append([config.id, config.slot, config.description, config.uri])
        return lis

