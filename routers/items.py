from typing import Optional
from models.item import Item, ItemDocument
from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    Request,
    Query,
    Depends
)
from beanie import PydanticObjectId
from dependencies import is_authenticated, current_user

router = APIRouter(
    prefix='/items',
    dependencies=[Depends(is_authenticated), Depends(current_user)]
)


@router.get('/search')
async def search(request: Request, q: Optional[str] = Query(None)):
    results = await ItemDocument.find({'user_id': PydanticObjectId(request.state.current_user['id']), 'name': {'$regex': q}}).to_list()
    return results


@router.get("/{item_id}", response_model=ItemDocument)
async def get_item(request: Request, item_id: PydanticObjectId):
    if not request.state.is_authenticated:
        raise HTTPException(status_code=401)
    item = await ItemDocument.find_one({
        '_id': PydanticObjectId(item_id),
        'user_id': PydanticObjectId(request.state.current_user['id'])
    })
    if item is None:
        raise HTTPException(status_code=404, detail={
                            'message': 'Item not found'})
    return item


@router.get('')
async def get_items(request: Request):
    return await ItemDocument.find_many({'user_id': PydanticObjectId(request.state.current_user['id'])}).to_list()


@router.put('/{item_id}')
async def update_item(item_id: PydanticObjectId, item: Item, request: Request):
    if not request.state.is_authenticated:
        raise HTTPException(status_code=401)
    exisiting_item = await ItemDocument.find_one({'_id': PydanticObjectId(item_id), 'user_id': PydanticObjectId(request.state.current_user['id'])})
    if exisiting_item is None:
        raise HTTPException(status_code=404)
    await exisiting_item.set(item.dict())
    return exisiting_item


@router.post('', response_model=ItemDocument, status_code=201)
async def create_item(request: Request, item: Item):
    created_item = ItemDocument(
        **item.dict(), user_id=request.state.current_user['id'])
    await created_item.insert()
    return created_item


@router.delete('/{item_id}')
async def delete_item(request: Request, item_id: PydanticObjectId):
    item = await ItemDocument.find_one({'_id': item_id, 'user_id': PydanticObjectId(request.state.current_user['id'])})
    if not item:
        raise HTTPException(status_code=404)
    await item.delete()
    return item
