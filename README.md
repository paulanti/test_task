Cуть задания: в приложении архив с файлами. Каждый файл представляет из себя xml или json файл со списком сущностей. Нужно особым образом парсить эти файлы и выдавать обработанную информацию по ним. Содержимое файлов:
BarterList.xml - содержимое списков обмена НПЦ
TradeList.xm - содержимое списков торговли НПЦ
containers.json - содержимое контейнеров и итем спавнеров
blackboxs.json - содержимое черных ящиков со случайным выпадением вещи
Quests.xml - содержимое квестов (нужно искать по наградам за выполнение, ID предмета <Reward> <TypeOfItems></TypeOfItems> и их количество <NumOfItems></NumOfItems> )
Creatures - папка с параметрами монстров
Anomalies - содержимое аномалий
Items.py - список всех предметов с ID и параметрами
ItemsNames.xml - названия предметов в зависимости от ID 

Задача: необходимо вывести на экран в интерактивном режиме все возможные пути получения определенной вещи. То есть, к примеру, предмет с ID 1 - Пистолет Макарова - это выбрал пользователь. В ответ нужно выдать - этот предмет может быть получен выполнением квеста AAA или BBB, убийством моба Паук уровня C, бартером с персонажем XXX, торговлей с персонажами YYY и ZZZ, а также выпадением из аномалии "Дробилка" или черного ящика с именем KKK.

Пояснение. При поиске соответствия между ID итемов, следует понимать, что уникальный ID итема содержится в файле Items.py, в каждом разделе под именем TypeID. В BarterList - ObtainedItemType. В blackboxs - itemID. В папке Creatures лежат параметры монстров, выпадающие из них предметы нужно искать в разделе "loot, by level", где сначала идет ID предмета, а потом шанс выпадения. В папке Anomalies лежат параметры аномалий, выпадающий лут из аномалии лежит в разделе artifacts.

Примечание. Скорость работы программы должна быть максимально возможной.
