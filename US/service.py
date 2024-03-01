import infrastructure


def fetchArea(dic):
    data = infrastructure.fetch("area",dic)
    state = infrastructure.filterState(data)
    county = infrastructure.filterCounty(data)
    return [state,county]

def fetchProduction(dic):
    data =  infrastructure.fetch("production",dic)
    state = infrastructure.filterState(data)
    county = infrastructure.filterCounty(data)
    return [state,county]


def merge(areaDF, prodDF, level):
    infrastructure.merge(areaDF, prodDF, level)
