from trello import TrelloClient


def send_to_trello(api_key, token, text, board):
    client = TrelloClient(
        api_key=api_key,
        token=token,
    )

    firstList = client.get_board(board).all_lists()[0]
    newCard = firstList.add_card(text)
    return newCard.url
