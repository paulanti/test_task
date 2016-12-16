import sys
import os
import json
import xml.etree.ElementTree


def import_items_names_from_xml(filename):

    """
    >>> items = import_items_names_from_xml('ItemsNames.xml')
    >>> items['810026']['item_id']
    '810026'
    >>> items['810026']['item_name']
    'Зат.Glock-17|Затвор от пистолета Glock-17'
    """

    items = {}

    tree = xml.etree.ElementTree.parse(filename)

    for element in tree.findall('.'):
        for item in element:
            data = {}
            data['item_id'] = item.tag[14:]
            data['item_name'] = item.text
            items[data['item_id']] = data
    return items


def import_quests_from_xml(filename):

    """
    >>> quests = import_quests_from_xml('Quests.xml')
    >>> quests['1143']['item_id']
    '1143'
    >>> quests['1143']['quest_title']
    ['Купить витамины']
    """
    items_id = []
    quests_titles = []
    quests = {}

    tree = xml.etree.ElementTree.parse(filename)

    for element in tree.findall('./quest/Reward'):
        for item in element:
            if item.tag == "TypeOfItems":
                if item.text is None:
                    item.text = 'None'
                items_id.append(item.text.split(','))

    for element in tree.findall('./quest/QuestInformation'):
        for quest in element:
            if quest.tag == "Title":
                if quest.text is None:
                    quest.text = "No Title"
                quests_titles.append(quest.text)

    for i in range(len(items_id)):
        for j in range(len(items_id[i])):
            id_quests = {}
            id_quests['item_id'] = items_id[i][j]
            id_quests['quest_title'] = [quests_titles[i]]
            if id_quests['item_id'] not in quests:
                quests[id_quests['item_id']] = id_quests
            else:
                quests[id_quests['item_id']]['quest_title'].append(id_quests['quest_title'][0])
    
    return quests                   


def import_traders_barters_from_xml(filename):

    """
    >>> traders = import_traders_barters_from_xml('TradeList.xml')
    >>> barters = import_traders_barters_from_xml('BarterList.xml')
    >>> traders['1139']['item_id']
    '1139'
    >>> traders['1139']['trader']
    ['CFTLoot_level_1', 'Vokzal_Doktor01', 'DK_Doktor01', 'Gurman_Doktor01', 'Laba_Skience01']
    >>> barters['118']['item_id']
    '118'
    >>> barters['118']['barter']
    ['Shtopor_barter', 'Item_Converter_barter']
    """
    barters_list = []
    barters = {}

    tree = xml.etree.ElementTree.parse(filename)

    if filename.endswith('TradeList.xml'): 
        tree_path = './{0}/ItemsList/Item/Type'
        npc = 'trader'
    if filename.endswith('BarterList.xml'): 
        tree_path = './{0}/ItemsList/List/ObtainedItemType'
        npc = 'barter'

    for element in tree.findall('.'):
        for barter in element:
            barters_list.append(barter.tag)

    for barter in barters_list:
        for item_id in tree.findall(tree_path.format(barter)):
            item_barters = {}
            item_id = item_id.text.strip()
            item_barters['item_id'] = item_id
            item_barters[npc] = [barter]
            if item_id not in barters:
                barters[item_barters['item_id']] = item_barters
            elif barter not in barters[item_barters['item_id']][npc]:
                barters[item_barters['item_id']][npc].append(item_barters[npc][0])
            else:
                pass

    return barters


def import_from_json(filename):

    """
    >>> blackboxs = import_from_json('blackboxs.json')
    >>> containers = import_from_json('containers.json')
    >>> blackboxs['856']['item_id']
    '856'
    >>> blackboxs['856']['blackbox']
    ['firstBox', 'Black_Box3']
    >>> containers['810009']['item_id']
    '810009'
    >>> containers['810009']['container']
    ['vez_forest_free', 'vez_novikovo']
    """

    with open(filename) as data_file:
        data = json.load(data_file)

    if filename.endswith('blackboxs.json'): box = "blackbox"
    if filename.endswith('containers.json'): box = "container"
    
    blackboxs = {}

    for i in range(len(data)):
        for k in range(len(data[i]['groups'])):
            for j in range(len(data[i]['groups'][k]['items'])):
                item_id = data[i]['groups'][k]['items'][j]['itemID'].strip()
                blackbox = data[i]['Name']
                item_blackboxs = {}
                item_blackboxs['item_id'] = item_id
                item_blackboxs[box] = [blackbox]
                if item_id not in blackboxs:
                    blackboxs[item_id] = item_blackboxs
                elif blackbox not in blackboxs[item_blackboxs['item_id']][box]:
                    blackboxs[item_id][box].append(item_blackboxs[box][0])
                else:
                    pass

    return blackboxs


def import_json_from_dir(path):

    """
    >>> creatures = import_json_from_dir('./Creatures/')
    >>> anomalies = import_json_from_dir('./Anomalies/')
    >>> creatures['839']['item_id']
    '839'
    >>> sorted(creatures['839']['creature'])
    ['Vedun 3 level', 'Vedun 30 level']
    >>> anomalies['210002']['item_id']
    '210002'
    >>> anomalies['210002']['anomaly']
    ['2Arrester', '2Drobilka', '2Katapulta', '2Microwave', '2Mikrovolnovka', '2Razryadnik', '2Zelenaya_gnil']
    """
    filenames = [filename for filename in os.listdir(path)]
    for filename in filenames:
        if filename.startswith('__') or filename.startswith('Test'):
            filenames.remove(filename)

    loot = 'loot, bylevel'

    creatures = {}

    for filename in filenames:
        with open((path + '{0}').format(filename)) as data_file:
            data = json.load(data_file)
        try:
            for level in data[loot]:
                for item_id in data[loot][level]:
                    id_creatures = {}
                    lvl = filename.replace('.json', '') + ' ' + level.strip('lvl_all, override') + ' level'
                    id_creatures['item_id'] = item_id
                    id_creatures['creature'] = [lvl]
                    if item_id not in creatures:
                        creatures[item_id] = id_creatures
                    else:
                        creatures[item_id]['creature'].append(id_creatures['creature'][0])
        except KeyError:
            try:
                for anomaly in data['artifacts']:
                    anomaly = str(anomaly)
                    id_anomalies = {}
                    id_anomalies['item_id'] = anomaly
                    id_anomalies['anomaly'] = [filename.replace('.json', '')]
                    if anomaly not in creatures:
                        creatures[anomaly] = id_anomalies
                    else:
                        creatures[anomaly]['anomaly'].append(id_anomalies['anomaly'][0])
            except KeyError:
                pass

    return creatures


def main(): 
    items = import_items_names_from_xml('ItemsNames.xml')
    quests = import_quests_from_xml('Quests.xml')
    traders = import_traders_barters_from_xml('TradeList.xml')
    barters = import_traders_barters_from_xml('BarterList.xml')
    blackboxs = import_from_json('blackboxs.json')
    containers = import_from_json('containers.json')
    creatures = import_json_from_dir('./Creatures/')
    anomalies = import_json_from_dir('./Anomalies/')


    for i in items.keys():
        if i in quests:
            items[i].update(quests[i])
        if i in traders:
            items[i].update(traders[i])
        if i in barters:
            items[i].update(barters[i])
        if i in blackboxs:
            items[i].update(blackboxs[i])
        if i in containers:
            items[i].update(containers[i])
        if i in creatures:
            items[i].update(creatures[i])
        if i in anomalies:
            items[i].update(anomalies[i])

    item_id = True

    while item_id:
        try:
            item_id = input("Введите ID предмета, чтобы выйти введите 'q' или 'quit': ")
            if item_id == 'q' or item_id == 'quit':
                item_id = False
            print("Предмет {0} может быть получен".format(items[item_id]['item_name']), end=" ")
            if 'quest_title' in items[item_id]:
                print("выполнением квестов: {0}".format(items[item_id]['quest_title']), end=", ")
            if 'creature' in items[item_id]:
                print("убийством мобов: {0}".format(items[item_id]['creature']), end=", ")
            if 'barter' in items[item_id]:
                print("бартером с персонажами: {0}".format(items[item_id]['barter']), end=", ")
            if 'trader' in items[item_id]:
                print("торговлей с персонажами: {0}".format(items[item_id]['trader']), end=", ")
            if 'anomaly' in items[item_id]:
                print("выпадением из аномалии: {0}".format(items[item_id]['anomaly']), end=", ")
            if 'blackbox' in items[item_id]:
                print("выпадением из черного ящика: {0}".format(items[item_id]['blackbox']), end=", ")
            if 'container' in items[item_id]:
                print("а также выпадением из контейнера: {0}.".format(items[item_id]['container']))
        except KeyError:
            print("Такого ID нет.")
            pass


def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _test()
    main()