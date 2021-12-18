from modules.migration.pathfinder import Pathfinder
from modules.migration.hamal import Hamal
from modules.migration.recorder import Recorder

sources = 'H:\影视'
target = 'G:\影视'

Pathfinder(sources, target).pathfinding()