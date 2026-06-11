import math
from dataclasses import dataclass

@dataclass
class Planet:
    id:int
    owner:int
    x:float
    y:float
    radius:float
    ships:int
    production:int

def parse_planets(obs):
    # 返回planet的数据
    raw_planets=obs.get("planets",[]) if isinstance(obs,dict) else obs.planets
    return [Planet(*p) for p in raw_planets]

def get_player(obs):
    return obs.get('player',0) if isinstance(obs,dict) else obs.player

def distance(a:Planet,b:Planet)->float:
    # 计算欧几里得距离
    return math.hypot(a.x - b.x, a.y - b.y)

def angle_to(a:Planet,b:Planet)->float:
    # 计算从点a到点b到方向角，即arctan(dy/dx)
    return math.atan2(b.y-a.y,b.x-a.x)

def reserve_ships(p:Planet)->int:
    """
    Keep some ships at home.
    This prevents the bot from emptying its planets.
    """
    return max(5,int(2*p.production),int(0.25*p.ships))

def neutral_score(src:Planet,tgt:Planet)->float:
    # 给中立星球打分，我们希望高production，short distance，low defenders的星球分数更高
    d=distance(src,tgt)
    return (25*tgt.production+1.5*tgt.radius-2.5*tgt.ships-0.05*d)

def agent(obs):
    player=get_player(obs)
    planets=parse_planets(obs)
    my_planets=[p for p in planets if p.owner==player]
    neutral_planets = [p for p in planets if p.owner == -1]
    moves=[]
    candidates=[]
    for src in my_planets:
        reserve = reserve_ships(src)
        available = src.ships - reserve

        if available <= 0:
            continue

        for tgt in neutral_planets:
            # Need enough ships to beat neutral defenders.
            # Add a small safety margin.
            required = int(tgt.ships + 2)

            if available < required:
                continue

            score = neutral_score(src, tgt)
            candidates.append((score, src, tgt, required))
    candidates.sort(key=lambda x: x[0], reverse=True)

    used_sources = set()
    used_targets = set()
    # 限制launch次数最多为3次
    max_moves=3
    for score,src,tgt,ships in candidates:
        if len(moves)>=max_moves:
            break
        if score<=0:
            continue
        if src.id in used_sources:
            continue
        if tgt.id in used_targets:
            continue
        angle=angle_to(src,tgt)
        moves.append([src.id, angle, ships])

        used_sources.add(src.id)
        used_targets.add(tgt.id)

    return moves