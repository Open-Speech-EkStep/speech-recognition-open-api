from src.monitoring import monitor


@monitor
def tryThis():
    tryThisToo()
    print('function called try this')


@monitor
def tryThisToo():
    print('function called try this too')


if __name__ == '__main__':
    tryThis()
