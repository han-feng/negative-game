"""
v1.0
小游戏“负数过过过”，参考名侦探学院游戏规则
教孩子学编程用版本，所以没有采用面向对象的写法，也没有拆分模块，并且选择字符界面库rich，简单友好。
"""
import random

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt


def get_card_value(card):
    return card["value"]


def get_content(card):
    s = ""
    owner_no = card["owner"]
    if(owner_no >= 0):
        player = players[owner_no]
        s = f"\n[yellow]{player['name']}"
    return f"[b][red]{card['value']}[/b]" + s


def generate_panels():
    return Columns([Panel(get_content(card), border_style="red", expand=True) for card in cards])


def display_cards():
    """显示负数牌列表"""
    console.print(generate_panels())


def get_player_content(player):
    values = []
    previous = 0
    result = player["pass"]
    for card in player["cards"]:
        value = card["value"]
        if value == previous-1:
            s = "[white]" + str(value) + "[/white]"
        else:
            s = str(value)
            result = result + value
        values.append(s)
        previous = value
    s = ",".join(values)
    return f"[b]{player['name']}  [green]{player['pass']}\n[red]{s}\n\n[yellow on red]得分：{result}"


def get_desktop_content():
    values = []
    for card in desktop_cards:
        values.append(str(card["value"]))
    s = ",".join(values)
    return f"[b]桌面  [green]{desktop_pass_count}\n[red]{s}"


def display_players():
    """显示玩家列表"""
    console.print(
        Columns([Panel(get_player_content(player), style="yellow") for player in players]))


def display_desktop():
    """显示桌面数据"""
    console.print(Panel(get_desktop_content(), style="white"))


def convert(n):
    """card 序号(cards下标)与 card value 转换函数"""
    return -n-3


def draw_card():
    """抽牌"""
    global current_card
    l = len(desktop_cards)
    i = random.randint(0, l-1)
    current_card = desktop_cards[i]
    desktop_cards.remove(current_card)  # 从桌面移除该负数牌
    """显示抽中的牌"""
    console.print("玩家 [yellow]%s[/yellow] 正在抽牌……" % current_player["name"], Panel.fit(
        str(current_card["value"]), title="抽出的牌", style="yellow on red"))


def next_player():
    """切换下一个玩家"""
    global current_player_no, current_player
    i = current_player_no + 1
    current_player_no = i % player_count
    current_player = players[current_player_no]


def on_accepted():
    """接受后的处理"""
    global desktop_pass_count, current_card
    current_player["cards"].append(current_card)
    current_player["cards"].sort(key=get_card_value, reverse=True)
    current_card["owner"] = current_player_no
    current_player["pass"] = current_player["pass"] + desktop_pass_count
    desktop_pass_count = 0
    current_card = None
    console.print("玩家 [yellow]%s[/yellow] 接受这张牌" % current_player["name"])


def on_passed():
    """pass 处理"""
    global desktop_pass_count
    current_player["pass"] = current_player["pass"] - 1
    desktop_pass_count = desktop_pass_count + 1
    console.print("玩家 [yellow]%s[/yellow] 使用[red][b]Pass[/b][/red]卡" %
                  current_player["name"])


console = Console()

"""
打印游戏说明
"""
readme = """
......
"""
console.print(Panel(readme, title="游戏说明", style="white on blue"))

"""
输入玩家数量
player_count: 玩家数量
"""
player_count = 0
while(player_count < 2 or player_count > 8):
    player_count = IntPrompt.ask("请输入玩家数量[violet][2~8]")

"""
输入玩家昵称
players: 玩家集合，每个玩家有三个属性: name,pass,cards
    name: 玩家昵称
    pass: 玩家拥有的 pass 牌数量
    cards: 玩家拥有的负数牌集合
"""
players = []
for i in range(player_count):
    name = Prompt.ask("请输入玩家 [yellow]%d[/yellow] 的昵称" % (i+1))
    players.append({"name": name, "pass": 9, "cards": []})

"""
cards: 负数牌集合, 每张牌有两个属性: value 和 owner
    value: 牌值，取值范围是 -35 ~ -3
    owner: 牌的拥有者序号，无拥有者时 owner=-1
    card 序号(cards下标)与 card value 的换算关系：n=-v-3, v=-n-3
"""
cards = []


"""
初始化 cards
"""
for i in range(33):
    cards.append({"value": convert(i), "owner": -1})

"""
desktop_cards: 桌面负数牌集合
"""
desktop_cards = []
for card in cards:
    desktop_cards.append(card)

"""
desktop_pass_count: 桌面 pass 牌数量
"""
desktop_pass_count = 0

"""
current_player_no: 当前玩家序号，该序号等于该玩家在 players 集合中的下标
current_player: 当前玩家
"""
current_player_no = 0
current_player = players[current_player_no]

"""
current_card: 当前抽到的负数牌
"""
current_card = None


"""
开始游戏
"""
while(len(desktop_cards) > 30):
    console.clear()
    display_cards()
    display_players()
    display_desktop()
    """抽牌"""
    draw_card()
    accepted = False
    while(not accepted):
        """"判断当前玩家是否具备 pass 资格"""
        if current_player["pass"] > 0:
            """请当前玩家做出选择"""
            accepted = Confirm.ask(
                "玩家 [yellow]%s[/yellow] 是否接受这张牌" % current_player["name"])
        else:
            accepted = True
            console.print("玩家 [yellow]%s[/yellow] 自动接受这张牌" %
                          current_player["name"])

        if accepted:
            on_accepted()
        else:
            on_passed()
            display_players()
            display_desktop()

        next_player()

console.clear()
display_cards()
display_players()

"""游戏结束"""
