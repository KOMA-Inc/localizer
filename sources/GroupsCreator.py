from collections import defaultdict
from hashlib import md5
from pathlib import Path
from LocalizationGroup import LocalizationGroup

class GroupsCreator:

    def __init__(self):
        pass

    def get_groups(self, entities):
        dictionary = defaultdict(list)
        for entity in entities:
            url = Path(entity.file.path).parents[1]
            group_key = f"{url}{entity.file.name}"
            dictionary[group_key].append(entity)

        groups = []
        for key, value in dictionary.items():
            if value:
                first = value[0]
                grouping_value = md5(key.encode()).hexdigest()
                name = first.file.name.split('.')[0]
                group = LocalizationGroup(name, first.file.kind, value, grouping_value)
                groups.append(group)

        return sorted(groups, key=lambda x: x.name)
