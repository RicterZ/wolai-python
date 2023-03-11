from wolai.constants import WOLAI_URL, API_VERSION_V1
from wolai.types.block import Block
from wolai.encoder import to_json
from wolai.types.resp import BlockFormat


BLOCK_API_URL = f'{WOLAI_URL}/{API_VERSION_V1}/blocks'


def create_block(ctx: callable, parent_id: str, blocks: list[Block] | Block) -> str:
    resp = None
    if isinstance(blocks, (list, set, )) and len(blocks) > 20:
        for i in range(0, len(blocks), 20):
            resp = create_block(ctx, parent_id, blocks[i:i+20])

        return resp

    data = to_json({
        'parent_id': parent_id,
        'blocks': blocks,
    })

    resp = ctx(BLOCK_API_URL, data)['data']
    block_id = resp.split('/')[-1]

    # page_id or block_id
    if '#' in block_id:
        block_id = block_id.split('#')[-1]

    return block_id


def get_block(ctx: callable, block_id: str) -> BlockFormat:
    url = f'{BLOCK_API_URL}/{block_id}'
    resp = ctx(url, method='get')['data']

    return BlockFormat(**resp)


def get_block_children(ctx: callable, block_id: str, start_cursor: str = '', page_size: int = 200) -> \
        (list[BlockFormat], bool, str):
    url = f'{BLOCK_API_URL}/{block_id}/children'
    resp = ctx(url, method='get', params={'start_cursor': start_cursor, 'page_size': page_size})

    # TODO: no next_cursor returned
    return [BlockFormat(**children) for children in resp.get('data', [])], \
        resp.get('has_more', False), resp.get('next_cursor')
