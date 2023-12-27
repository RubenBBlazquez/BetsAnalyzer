from fastapi import APIRouter

from src.common.schemas import GETResponseModel
from src.sport_monks_client.models import SportMonksClient

router = APIRouter()


@router.get("/get_players", response_model=GETResponseModel)
async def get_players():
    players = SportMonksClient().get_players()

    return GETResponseModel(
        data=players, message="Players were successfully fetched", status_code=200
    )
