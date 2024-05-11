from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from calc_optimal_equipment import optimal_equipment_combination_per_season
from consts import summer_month_numbers, winter_month_numbers, offSeason_month_numbers
from mainOld import year_task
from turbines.get_collection_point_new import get_collection_point
from turbines.turbine_hop_new import calc_turbine_hop
from turbines.turbine_shop_hop_new import calc_turbines_shop_hop

turbineRouter = APIRouter(
    prefix="/turbines",
    tags=["Турбины"]
)


class TurbineData(BaseModel):
    """
    Информация об одном котле

    :param station_number: станционный номер.
    :param mark: Марка турбины.
    :param electricity_power: установленная электрическая мощность.
    :param thermal_power: тепловая мощность гкал/ч.
    :param power_generation: выработка электроэнергии в отчётном.
    """
    station_number: int
    mark: str
    electricity_power: int
    thermal_power: int
    power_generation: float


@turbineRouter.post("/get-optimal")
def get_turbines_optimal(
        turbines: List[TurbineData]
):
    """
    Получение оптимального состава турбин на каждый сезон года.

    :param turbines: Состав турбинного оборудования, имеющийся на станции.
    :return: Объект с оптимальным составом оборудования по сезонам года
    """
    turbines = [turbine.dict() for turbine in turbines]

    summer_turbines_combination = optimal_equipment_combination_per_season(year_task, turbines, summer_month_numbers,
                                                                           'turbines')
    winter_turbines_combination = optimal_equipment_combination_per_season(year_task, turbines, winter_month_numbers,
                                                                           'turbines')
    offSeason_turbines_combination = optimal_equipment_combination_per_season(year_task, turbines,
                                                                              offSeason_month_numbers, 'turbines')
    return ({
        'summerTurbines': summer_turbines_combination,
        'winterTurbines': winter_turbines_combination,
        'offSeasonTurbines': offSeason_turbines_combination
    })


class TurbineSteamConsumption(BaseModel):
    """
    Данные о расходной характеристике турбины

    :param turbine_mark: Марка турбины
    :param: steam_consumption характеристика расхода пара турбины
    """
    turbine_mark: str
    steam_consumption: List[float]


class TurbineDataForHop(TurbineSteamConsumption):
    """
    Данные для расчёта ХОП отдельной турбины. Интерфейс наследует TurbineSteamConsumption

    :param season - сезон года, для которого считается ХОП
    """
    season: str


@turbineRouter.post("/turbine-hop")
def get_turbine_hop(
        turbine_data: TurbineDataForHop
):
    """
    Расчёт ХОП отдельной турбины.

    :param turbine_data: информация расхода пара для турбины и её марка
    :return: turbines_hop Объект содержащий ХОП турбины
    """
    steam_consuption = get_collection_point(turbine_data.steam_consumption, turbine_data.season)

    turbines_hop = calc_turbine_hop(turbine_data.turbine_mark, steam_consuption)

    return turbines_hop


class TurbinesShopHopData(BaseModel):
    turbines_data: List[TurbineSteamConsumption]
    season: str


@turbineRouter.post("/turbine-shop-hop")
def get_turbines_shop_hop(
        data: TurbinesShopHopData
):
    """
    Расчёт ХОП турбинного цеха.

    :param data: информация расхода пара для турбин и их марки
    :return: flow_char расходная характеристика турбинного цеха,
             turbines_shop_hop ХОП турбинного цеха
    """
    turbines = [turbine.dict() for turbine in data.turbines_data]

    flow_char, turbines_shop_hop = calc_turbines_shop_hop(turbines, data.season)

    return {'flow_char': flow_char, 'turbines_shop_hop': turbines_shop_hop}
